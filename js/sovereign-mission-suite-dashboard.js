/*
 * S&R CoreSync For Intelligent Solutions - Mission Suite Dashboard (Missions 104-106)
 * Unified KPI aggregation, cross-mission activity log, SHA-256 sealed executive report.
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 */
(function () {
    'use strict';

    var M = window.SRMission;

    // --- Aggregated mission data (mirrors the three mission engines) ---
    var ARB = {
        active: 4,
        value: 1850000 + 6420000 + 940000 + 3175000,
        docs: 412 + 1290 + 238 + 655,
        awards: 0
    };
    var CBDC = {
        currencies: 5,
        settles: 0,
        savings: 0
    };
    var ZKP = {
        enclaves: 3,
        proofs: 4
    };

    var logLines = [];
    var lastReport = null;
    var sealCount = 0;

    var terminal = document.getElementById('suite-terminal');
    var matrixBody = document.getElementById('kpi-matrix-body');

    function now() { return new Date().toISOString().substring(11, 19) + 'Z'; }

    function setUpdated() {
        M.setText('suite-updated', new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC');
    }

    function healthScore() {
        // Simple composite: all three missions active => 100
        var score = 0;
        if (ARB.active > 0) { score += 34; }
        if (CBDC.currencies >= 5) { score += 33; }
        if (ZKP.enclaves >= 3) { score += 33; }
        return Math.min(100, score);
    }

    function renderKpis() {
        M.setText('kpi-arb-cases', String(ARB.active));
        M.setText('kpi-arb-value', M.money(ARB.value, 'EUR'));
        M.setText('kpi-cbdc-settles', String(CBDC.settles));
        M.setText('kpi-cbdc-savings', M.money(CBDC.savings, 'EUR'));
        M.setText('kpi-zkp-enclaves', String(ZKP.enclaves));
        M.setText('kpi-zkp-proofs', String(ZKP.proofs));
        var h = healthScore();
        M.setText('kpi-health', h + '%');
        M.setText('suite-health', h + '%');
    }

    function renderMatrix() {
        if (!matrixBody) { return; }
        matrixBody.textContent = '';
        var rows = [
            ['104 — التحكيم', 'قضايا نشطة', String(ARB.active), 'OK'],
            ['104 — التحكيم', 'قيمة المطالبات', M.money(ARB.value, 'EUR'), 'OK'],
            ['104 — التحكيم', 'مستندات الأدلة', ARB.docs.toLocaleString('en-US'), 'OK'],
            ['104 — التحكيم', 'أحكام مختومة', String(ARB.awards), ARB.awards > 0 ? 'OK' : 'PENDING'],
            ['105 — CBDC', 'عملات رقمية', String(CBDC.currencies), 'OK'],
            ['105 — CBDC', 'تسويات ذرية', String(CBDC.settles), CBDC.settles > 0 ? 'OK' : 'PENDING'],
            ['105 — CBDC', 'توفير مجمّع', M.money(CBDC.savings, 'EUR'), 'OK'],
            ['106 — ZKP', 'بيئات TEE', String(ZKP.enclaves), 'OK'],
            ['106 — ZKP', 'أنواع الإثبات', String(ZKP.proofs), 'OK'],
            ['SUITE', 'Health Score', healthScore() + '%', healthScore() === 100 ? 'OK' : 'WARN']
        ];
        rows.forEach(function (r) {
            var tr = document.createElement('tr');
            r.forEach(function (cell, idx) {
                var td = document.createElement('td');
                if (idx === 2) { td.className = 'mono'; }
                if (idx === 3) {
                    td.className = cell === 'OK' ? 'ok' : (cell === 'WARN' ? 'log-red' : '');
                    td.textContent = cell;
                } else {
                    td.textContent = cell;
                }
                tr.appendChild(td);
            });
            matrixBody.appendChild(tr);
        });
    }

    function pushLog(cls, text) {
        logLines.unshift([cls, '[' + now() + '] ' + text]);
        if (logLines.length > 40) { logLines.pop(); }
        M.renderLog(terminal, logLines);
        M.setText('log-count', String(logLines.length));
    }

    function syncSuite() {
        // Simulate cross-mission sync pulse
        ARB.awards = Math.max(ARB.awards, 1);
        CBDC.settles += 1;
        CBDC.savings += 12500;
        pushLog('log-gold', '[SUITE-SYNC] Cross-mission sync pulse dispatched to 104/105/106');
        pushLog('log-blue', '[104] Arbitration docket re-indexed • ' + ARB.active + ' active cases');
        pushLog('log-blue', '[105] Atomic PvP settlement #' + CBDC.settles + ' • savings ' + M.money(CBDC.savings, 'EUR'));
        pushLog('log-violet', '[106] ZKP TEE attestation refreshed • ' + ZKP.enclaves + ' enclaves');
        pushLog('log-green', '[HEALTH] Suite health score: ' + healthScore() + '%');
        renderKpis();
        renderMatrix();
        setUpdated();
    }

    function sealReport() {
        var report = {
            title: 'S&R CoreSync Sovereign Mission Suite Report (104-106)',
            suite: 'missions-104-106',
            generatedAt: new Date().toISOString(),
            healthScore: healthScore() + '%',
            missions: {
                104: { activeCases: ARB.active, claimValueEUR: ARB.value, evidenceDocs: ARB.docs, sealedAwards: ARB.awards },
                105: { currencies: CBDC.currencies, atomicSettlements: CBDC.settles, aggregateSavingsEUR: CBDC.savings },
                106: { teeEnclaves: ZKP.enclaves, proofTypes: ZKP.proofs }
            },
            log: logLines.map(function (l) { return l[1]; }),
            nonce: M.randomHex(12)
        };
        M.sha256Hex(JSON.stringify(report)).then(function (hash) {
            report.sealSHA256 = hash;
            lastReport = report;
            sealCount += 1;
            M.setText('suite-seal', hash.slice(0, 16) + '…');
            pushLog('log-gold', '[SEAL] Executive report sealed • SHA-256: ' + hash.slice(0, 24) + '…');
            pushLog('log-green', '[EXPORT] Ready for download (JSON) / print (PDF)');
        });
    }

    document.getElementById('btn-sync-suite').addEventListener('click', syncSuite);
    document.getElementById('btn-seal-suite').addEventListener('click', sealReport);
    document.getElementById('btn-export-suite').addEventListener('click', function () {
        if (!lastReport) {
            pushLog('log-red', '[EXPORT] Seal the report first.');
            return;
        }
        M.downloadJSON('SR-CoreSync-Mission-Suite-Report-104-106.json', lastReport);
    });
    document.getElementById('btn-print-suite').addEventListener('click', function () {
        window.print();
    });

    // Initial render
    renderKpis();
    renderMatrix();
    setUpdated();
    pushLog('log-gold', '[SUITE] Mission Suite Dashboard 104-106 online');
    pushLog('log-blue', '[104] Arbitration hub linked • ' + ARB.active + ' active cases');
    pushLog('log-blue', '[105] CBDC bridge linked • ' + CBDC.currencies + ' currencies');
    pushLog('log-violet', '[106] ZKP enclave linked • ' + ZKP.enclaves + ' TEE environments');
    pushLog('log-green', '[HEALTH] Suite health score: ' + healthScore() + '%');

    // Auto-seal on load for a ready-to-export report
    sealReport();
})();
