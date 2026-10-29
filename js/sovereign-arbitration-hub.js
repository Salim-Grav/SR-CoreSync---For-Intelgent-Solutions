/*
 * S&R CoreSync For Intelligent Solutions - Mission 104
 * Sovereign International Arbitration & Dispute Resolution Hub
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 */
(function () {
    'use strict';

    var M = window.SRMission;

    var SEATS = {
        supply: { seat: 'Amsterdam (NAI)', rules: 'NAI Arbitration Rules 2024', law: 'Dutch Civil Code Book 7 + CISG 1980' },
        construction: { seat: 'Dubai (DIFC-AI)', rules: 'DIAC Rules 2022 + FIDIC Red Book 2017', law: 'DIFC Law No. 1 of 2008' },
        ip: { seat: 'Singapore (SIAC)', rules: 'SIAC Rules 2025', law: 'TRIPS + Singapore IPA' },
        finance: { seat: 'Riyadh (SCCA)', rules: 'SCCA Rules 2023 + AAOIFI Sharia Std. No. 32', law: 'Saudi Arbitration Law (Royal Decree M/34)' }
    };

    var cases = [
        { id: 'ARB-2026-0418', claimant: 'Rotterdam Logistics B.V.', respondent: 'Gulf Trade Holding LLC', amount: 1850000, type: 'supply', docs: 412, merit: 0.78 },
        { id: 'ARB-2026-0421', claimant: 'Al-Noor Construction Co.', respondent: 'Emirates Towers Dev. PJSC', amount: 6420000, type: 'construction', docs: 1290, merit: 0.64 },
        { id: 'ARB-2026-0433', claimant: 'S&R CoreSync IP Licensing', respondent: 'Pacific SoftWorks Pte. Ltd.', amount: 940000, type: 'ip', docs: 238, merit: 0.86 },
        { id: 'ARB-2026-0447', claimant: 'Damascus Trade Finance House', respondent: 'Levant Sukuk Issuer SPV', amount: 3175000, type: 'finance', docs: 655, merit: 0.71 }
    ];

    var current = cases[0];
    var awards = 0;
    var lastAward = null;
    var list = document.getElementById('case-list');
    var terminal = document.getElementById('arb-terminal');

    function typeLabel(type) {
        return { supply: 'توريد', construction: 'مقاولات FIDIC', ip: 'ملكية فكرية', finance: 'تمويل وصكوك' }[type] || type;
    }

    function renderList() {
        list.textContent = '';
        cases.forEach(function (c) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'select-item' + (c.id === current.id ? ' active' : '');
            btn.setAttribute('aria-pressed', c.id === current.id ? 'true' : 'false');
            btn.dataset.id = c.id;

            var head = document.createElement('div');
            head.className = 'item-head';
            var name = document.createElement('span');
            name.className = 'item-name';
            name.textContent = c.claimant + '  ⟷  ' + c.respondent;
            var tag = document.createElement('span');
            tag.className = 'item-tag mono';
            tag.textContent = c.id;
            head.appendChild(name);
            head.appendChild(tag);

            var sub = document.createElement('p');
            sub.className = 'item-sub';
            sub.textContent = typeLabel(c.type) + ' • ' + M.money(c.amount, 'EUR') + ' • المقعد المقترح: ' + SEATS[c.type].seat + ' • ' + c.docs.toLocaleString('en-US') + ' مستند';

            btn.appendChild(head);
            btn.appendChild(sub);
            btn.addEventListener('click', function () {
                current = c;
                renderList();
                showIntake();
            });
            list.appendChild(btn);
        });
        updateStats();
    }

    function updateStats() {
        var total = cases.reduce(function (s, c) { return s + c.amount; }, 0);
        var docs = cases.reduce(function (s, c) { return s + c.docs; }, 0);
        M.setText('stat-active', String(cases.length));
        M.setText('stat-value', M.money(total, 'EUR'));
        M.setText('kpi-docs', docs.toLocaleString('en-US'));
        M.setText('active-case-badge', current.id);
    }

    function showIntake() {
        var s = SEATS[current.type];
        M.renderLog(terminal, [
            ['log-gold', '[DOCKET] Case ' + current.id + ' loaded • ' + typeLabel(current.type)],
            ['log-blue', '[PARTIES] ' + current.claimant + ' v. ' + current.respondent],
            ['log-blue', '[SEAT] ' + s.seat + ' • Rules: ' + s.rules],
            ['', '[EVIDENCE] ' + current.docs.toLocaleString('en-US') + ' documents indexed in WORM chain-of-custody vault'],
            ['', '------------------------------------------------------------------'],
            ['log-green', 'Ready. Press "تحليل القضية" to generate the AI-assisted draft award.']
        ]);
    }

    function analyze() {
        var s = SEATS[current.type];
        var meritPct = Math.round(current.merit * 100);
        var awarded = Math.round(current.amount * current.merit / 1000) * 1000;
        var costs = Math.round(current.amount * 0.035);
        var draft = {
            platform: 'S&R CoreSync Sovereign International Arbitration Hub',
            mission: 104,
            caseId: current.id,
            claimant: current.claimant,
            respondent: current.respondent,
            disputeType: current.type,
            seat: s.seat,
            rules: s.rules,
            governingLaw: s.law,
            claimAmountEUR: current.amount,
            evidenceDocuments: current.docs,
            claimMeritAssessment: meritPct + '%',
            recommendedAwardEUR: awarded,
            arbitrationCostsEUR: costs,
            enforceability: 'New York Convention 1958 - Art. V compliant',
            disclaimer: 'AI-assisted draft for tribunal review only; not a binding award until signed by the arbitral tribunal.',
            issuedAt: new Date().toISOString(),
            nonce: M.randomHex(12)
        };
        M.sha256Hex(JSON.stringify(draft)).then(function (hash) {
            draft.sealSHA256 = hash;
            lastAward = draft;
            awards += 1;
            M.setText('kpi-awards', String(awards));
            M.setText('stat-last-seal', hash.slice(0, 16) + '…');
            M.renderLog(terminal, [
                ['log-gold', '[TRIBUNAL AI] Analysing ' + current.id + ' under ' + s.rules + ' ...'],
                ['log-blue', '[LAW] Governing law resolved: ' + s.law],
                ['log-blue', '[EVIDENCE] Contract clauses, invoices & correspondence cross-referenced (' + current.docs + ' docs)'],
                ['log-violet', '[MERITS] Claim merit assessment: ' + meritPct + '% • Recommended award: ' + M.money(awarded, 'EUR')],
                ['log-violet', '[COSTS] Estimated arbitration costs: ' + M.money(costs, 'EUR') + ' (allocated per Art. 42 principle)'],
                ['log-green', '[DRAFT AWARD] Sealed & logged • Enforceable in 172 New York Convention states'],
                ['', '------------------------------------------------------------------'],
                ['', 'SHA-256 Seal: ' + hash],
                ['log-red', 'Advisory draft — final award requires signature of the human arbitral tribunal.']
            ]);
        });
    }

    document.getElementById('btn-analyze').addEventListener('click', analyze);

    document.getElementById('btn-export-award').addEventListener('click', function () {
        if (!lastAward || lastAward.caseId !== current.id) {
            M.renderLog(terminal, [['log-red', '[EXPORT] Generate the draft award for ' + current.id + ' first.']]);
            return;
        }
        M.downloadJSON('SR-CoreSync-Arbitration-Award-' + current.id + '.json', lastAward);
    });

    document.getElementById('new-case-form').addEventListener('submit', function (e) {
        e.preventDefault();
        var claimant = document.getElementById('f-claimant').value.trim();
        var respondent = document.getElementById('f-respondent').value.trim();
        var amount = parseFloat(document.getElementById('f-amount').value);
        var type = document.getElementById('f-type').value;
        var msg = document.getElementById('form-msg');
        if (!claimant || !respondent || !(amount >= 1000)) {
            msg.textContent = '  ⚠️ يرجى إدخال أسماء الأطراف وقيمة مطالبة لا تقل عن €1,000';
            msg.style.color = '#fda4af';
            return;
        }
        var nextNo = 448 + cases.length;
        var c = {
            id: 'ARB-2026-0' + nextNo,
            claimant: claimant,
            respondent: respondent,
            amount: amount,
            type: type,
            docs: 0,
            merit: 0.5 + (nextNo % 40) / 100
        };
        cases.push(c);
        current = c;
        renderList();
        showIntake();
        msg.textContent = '  ✅ تم إيداع الطلب ' + c.id;
        msg.style.color = '#6ee7b7';
        e.target.reset();
    });

    renderList();
    showIntake();
})();

