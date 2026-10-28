/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 *
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

(function () {
    'use strict';

    const records = [
        {
            date: '2026-10-03', supplier: 'Northwind Cloud BV', invoice: 'INV-2601',
            framework: 'IFRS', net: 1000, vat: 210, vatRate: 21, expectedVatRate: 21,
            debit: 1210, credit: 1210, document: true, shariaContract: '', shariaReview: ''
        },
        {
            date: '2026-10-07', supplier: 'Amanah Trade Cooperative', invoice: 'AM-1048',
            framework: 'AAOIFI', net: 4800, vat: 0, vatRate: 0, expectedVatRate: 0,
            debit: 4800, credit: 4800, document: false, shariaContract: 'Murabaha', shariaReview: 'pending'
        },
        {
            date: '2026-10-11', supplier: 'Delta Office Supplies', invoice: 'INV-2604',
            framework: 'IFRS', net: 320, vat: 28.8, vatRate: 9, expectedVatRate: 21,
            debit: 387.2, credit: 387.2, document: true, shariaContract: '', shariaReview: ''
        },
        {
            date: '2026-10-12', supplier: 'Northwind Cloud BV', invoice: 'INV-2601',
            framework: 'IFRS', net: 1000, vat: 210, vatRate: 21, expectedVatRate: 21,
            debit: 1210, credit: 1210, document: true, shariaContract: '', shariaReview: ''
        },
        {
            date: '2026-10-18', supplier: 'Meridian Facilities', invoice: 'MF-8892',
            framework: 'IFRS', net: 750, vat: 157.5, vatRate: 21, expectedVatRate: 21,
            debit: 907.5, credit: 900, document: true, shariaContract: '', shariaReview: ''
        },
        {
            date: '2026-10-22', supplier: 'Rihla Capital Services', invoice: 'RC-3301',
            framework: 'AAOIFI', net: 2100, vat: 0, vatRate: 0, expectedVatRate: 0,
            debit: 2100, credit: 2100, document: true, shariaContract: '', shariaReview: ''
        }
    ];

    const elements = {
        body: document.getElementById('records-body'),
        findings: document.getElementById('findings-list'),
        standard: document.getElementById('standard-filter'),
        search: document.getElementById('search-input'),
        state: document.getElementById('run-state'),
        announcer: document.getElementById('announcer'),
        metrics: {
            records: document.getElementById('metric-records'),
            findings: document.getElementById('metric-findings'),
            balanced: document.getElementById('metric-balanced'),
            net: document.getElementById('metric-net')
        }
    };

    const money = new Intl.NumberFormat('nl-NL', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const number = new Intl.NumberFormat('nl-NL', { maximumFractionDigits: 2 });
    let activeResults = [];

    function escapeHTML(value) {
        return String(value).replace(/[&<>"']/g, function (char) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char];
        });
    }

    function buildInvoiceLink(record) {
        return 'erp-operations-crm.html?invoice=' + encodeURIComponent(record.invoice) +
            '&supplier=' + encodeURIComponent(record.supplier) +
            '&net=' + encodeURIComponent(record.net) +
            '&vat=' + encodeURIComponent(record.vat);
    }

    function selectedRecords() {
        const standard = elements.standard.value;
        const query = elements.search.value.trim().toLocaleLowerCase();
        return records.filter(function (record) {
            const matchesStandard = standard === 'all' || record.framework === standard;
            const matchesQuery = !query || (record.supplier + ' ' + record.invoice).toLocaleLowerCase().includes(query);
            return matchesStandard && matchesQuery;
        });
    }

    function analyze(selected) {
        const duplicates = new Set();
        const seen = new Set();
        selected.forEach(function (record) {
            const key = (record.supplier + '|' + record.invoice).toLocaleLowerCase();
            if (seen.has(key)) duplicates.add(key);
            seen.add(key);
        });

        return selected.map(function (record) {
            const issues = [];
            const duplicateKey = (record.supplier + '|' + record.invoice).toLocaleLowerCase();
            if (Math.abs(record.debit - record.credit) > 0.01) issues.push('فرق مدين/دائن');
            if (!record.document) issues.push('مرجع المستند مفقود');
            if (duplicates.has(duplicateKey)) issues.push('احتمال تكرار فاتورة المورد');
            if (record.expectedVatRate !== null && Math.abs(record.vat - (record.net * record.expectedVatRate / 100)) > 0.02) {
                issues.push('قيمة الضريبة لا تطابق الإعداد المتوقع');
            }
            if (record.framework === 'AAOIFI' && (!record.shariaContract || record.shariaReview !== 'approved')) {
                issues.push('تصنيف/مراجعة AAOIFI بحاجة إلى استكمال');
            }
            return { record: record, issues: issues };
        });
    }

    function render() {
        const selected = selectedRecords();
        activeResults = analyze(selected);
        const findingCount = activeResults.reduce(function (sum, result) { return sum + result.issues.length; }, 0);
        const balancedCount = activeResults.filter(function (result) {
            return Math.abs(result.record.debit - result.record.credit) <= 0.01;
        }).length;
        const netTotal = selected.reduce(function (sum, record) { return sum + record.net; }, 0);

        elements.metrics.records.textContent = number.format(selected.length);
        elements.metrics.findings.textContent = number.format(findingCount);
        elements.metrics.balanced.textContent = number.format(balancedCount);
        elements.metrics.net.textContent = money.format(netTotal);
        elements.body.innerHTML = activeResults.length ? activeResults.map(function (result) {
            const record = result.record;
            const statusClass = result.issues.length ? 'flagged' : 'clear';
            const statusText = result.issues.length ? result.issues.length + ' ملاحظات' : 'مطابقة أولية';
            const invUrl = buildInvoiceLink(record);
            return '<tr>' +
                '<td><span class="mono">' + escapeHTML(record.date) + '</span><br>' +
                '<a class="inv-link mono" href="' + invUrl + '">📜 ' + escapeHTML(record.invoice) + ' ↗</a></td>' +
                '<td>' + escapeHTML(record.supplier) + '</td>' +
                '<td><span class="mono">' + escapeHTML(record.framework) + '</span></td>' +
                '<td><span class="mono">€' + money.format(record.net) + '</span><br><small>VAT €' + money.format(record.vat) + ' · ' + number.format(record.vatRate) + '%</small></td>' +
                '<td><span class="mono">€' + money.format(record.debit) + '</span><br><small>€' + money.format(record.credit) + '</small></td>' +
                '<td><span class="status ' + statusClass + '">' + statusText + '</span><br>' +
                '<a class="button sm-btn gold-btn" href="' + invUrl + '">📜 فتح الفاتورة</a> ' +
                '<a class="button sm-btn" href="templates/invoice-quote-email.html">🧾 القالب</a></td></tr>';
        }).join('') : '<tr><td class="empty" colspan="6">لا توجد سجلات تطابق عوامل التصفية.</td></tr>';

        const findings = activeResults.flatMap(function (result) {
            return result.issues.map(function (issue) {
                return {
                    invoice: result.record.invoice,
                    supplier: result.record.supplier,
                    issue: issue,
                    url: buildInvoiceLink(result.record)
                };
            });
        });
        elements.findings.innerHTML = findings.length ? findings.map(function (finding) {
            return '<article class="finding"><strong>' + escapeHTML(finding.issue) + '</strong><span>' +
                escapeHTML(finding.supplier) + ' · <a class="inv-link mono" href="' + finding.url + '">📜 ' + escapeHTML(finding.invoice) + ' ↗</a>' +
                '</span></article>';
        }).join('') : '<article class="finding none"><strong>لا توجد ملاحظات في السجلات المعروضة</strong><span>النتيجة أولية وتخضع للمراجعة البشرية.</span></article>';
    }

    function download(filename, contents, type) {
        const blob = new Blob([contents], { type: type });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    }

    function csvCell(value) {
        return '"' + String(value).replace(/"/g, '""') + '"';
    }

    document.getElementById('run-audit').addEventListener('click', function () {
        render();
        elements.state.textContent = 'اكتملت المطابقة التجريبية';
        elements.announcer.textContent = 'اكتملت المطابقة التجريبية؛ راجع الملاحظات قبل اعتماد أي إجراء.';
    });
    document.getElementById('export-csv').addEventListener('click', function () {
        const header = ['date', 'supplier', 'invoice', 'framework', 'net_eur', 'vat_eur', 'debit_eur', 'credit_eur', 'document_present', 'invoice_link', 'findings'];
        const lines = activeResults.map(function (result) {
            const record = result.record;
            return [
                record.date, record.supplier, record.invoice, record.framework, record.net, record.vat,
                record.debit, record.credit, record.document, buildInvoiceLink(record), result.issues.join('; ')
            ].map(csvCell).join(',');
        });
        download('coresync-audit-sample.csv', '\uFEFF' + [header.join(','), ...lines].join('\r\n'), 'text/csv;charset=utf-8');
        elements.announcer.textContent = 'تم تجهيز ملف CSV من السجلات المعروضة.';
    });
    document.getElementById('export-json').addEventListener('click', function () {
        const report = {
            reportType: 'illustrative-audit-readiness',
            generatedAt: new Date().toISOString(),
            demoDataOnly: true,
            standardsNotice: 'Illustrative checks only; not a compliance opinion or audit certification.',
            filters: { framework: elements.standard.value, search: elements.search.value.trim() },
            summary: {
                records: activeResults.length,
                findings: activeResults.reduce(function (sum, result) { return sum + result.issues.length; }, 0)
            },
            records: activeResults.map(function (result) {
                return Object.assign({}, result.record, {
                    invoicePortalUrl: buildInvoiceLink(result.record),
                    findings: result.issues
                });
            })
        };
        download('coresync-audit-sample.json', JSON.stringify(report, null, 2), 'application/json;charset=utf-8');
        elements.announcer.textContent = 'تم تجهيز حزمة تقرير JSON من السجلات المعروضة.';
    });
    elements.standard.addEventListener('change', render);
    elements.search.addEventListener('input', render);
    render();
}());
