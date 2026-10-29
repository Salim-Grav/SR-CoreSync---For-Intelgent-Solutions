/*
 * S&R CoreSync For Intelligent Solutions - Mission 105
 * Sovereign Multi-CBDC Cross-Border Bridge
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 */
(function () {
    'use strict';

    var M = window.SRMission;

    // Indicative reference rates expressed as units per 1 EUR (planning/demo only).
    var CBDC = {
        EUR: { label: 'Digital Euro (ECB)', perEUR: 1 },
        SAR: { label: 'Digital Riyal (SAMA)', perEUR: 4.05 },
        AED: { label: 'Digital Dirham (CBUAE)', perEUR: 3.97 },
        SGD: { label: 'Digital SGD (MAS)', perEUR: 1.45 },
        USD: { label: 'Tokenised USD Deposit', perEUR: 1.08 }
    };
    var FEE_RATE = 0.0005;
    var LEGACY_RATE = 0.015;

    var from = document.getElementById('f-from');
    var to = document.getElementById('f-to');
    var amountEl = document.getElementById('f-amount');
    var terminal = document.getElementById('cbdc-terminal');
    var ledgerBody = document.getElementById('ledger-body');
    var ledger = [];
    var volumeEUR = 0;
    var savingEUR = 0;

    Object.keys(CBDC).forEach(function (code) {
        [from, to].forEach(function (sel) {
            var opt = document.createElement('option');
            opt.value = code;
            opt.textContent = code + ' — ' + CBDC[code].label;
            sel.appendChild(opt);
        });
    });
    from.value = 'EUR';
    to.value = 'SAR';

    function quote() {
        var amt = parseFloat(amountEl.value);
        var rate = CBDC[to.value].perEUR / CBDC[from.value].perEUR;
        var valid = amt > 0 && from.value !== to.value;
        var fee = valid ? amt * FEE_RATE : 0;
        var receive = valid ? (amt - fee) * rate : 0;
        M.setText('corridor-badge', from.value + ' → ' + to.value);
        M.setText('q-rate', valid ? '1 ' + from.value + ' = ' + rate.toFixed(4) + ' ' + to.value : '—');
        M.setText('q-receive', valid ? M.money(receive, to.value) : '—');
        M.setText('q-fee', valid ? M.money(fee, from.value) : '—');
        return { valid: valid, amount: amt, rate: rate, fee: fee, receive: receive };
    }

    function addLedgerRow(entry) {
        var tr = document.createElement('tr');
        [
            [entry.reference, 'mono'],
            [entry.from + ' → ' + entry.to, 'mono'],
            [M.money(entry.sent, entry.from), 'mono'],
            [M.money(entry.received, entry.to), 'mono'],
            ['✅ FINAL', 'ok']
        ].forEach(function (cell) {
            var td = document.createElement('td');
            td.className = cell[1];
            td.textContent = cell[0];
            tr.appendChild(td);
        });
        tr.title = 'SHA-256: ' + entry.sealSHA256;
        var empty = document.getElementById('ledger-empty');
        if (empty) { empty.remove(); }
        ledgerBody.insertBefore(tr, ledgerBody.firstChild);
    }

    function renderEmpty() {
        var tr = document.createElement('tr');
        tr.id = 'ledger-empty';
        tr.className = 'empty-row';
        var td = document.createElement('td');
        td.colSpan = 5;
        td.textContent = 'لا توجد تسويات بعد — نفّذ أول تسوية ذرية لتظهر هنا مع ختمها التشفيري.';
        tr.appendChild(td);
        ledgerBody.appendChild(tr);
    }

    function settle(e) {
        e.preventDefault();
        var q = quote();
        if (!q.valid) {
            M.renderLog(terminal, [['log-red', '[REJECTED] Enter a positive amount and two different CBDCs.']]);
            return;
        }
        var finality = (1.8 + Math.random() * 1.4).toFixed(2);
        var entry = {
            reference: 'CBDC-' + Date.now().toString(36).toUpperCase(),
            from: from.value,
            to: to.value,
            sent: Math.round(q.amount * 100) / 100,
            received: Math.round(q.receive * 100) / 100,
            referenceRate: Number(q.rate.toFixed(6)),
            bridgeFee: Math.round(q.fee * 100) / 100,
            beneficiary: document.getElementById('f-beneficiary').value.trim().slice(0, 80),
            mechanism: 'Atomic PvP (Hash Time-Locked, all-or-nothing)',
            messageStandard: 'ISO 20022 pacs.009.001.10',
            finalitySeconds: Number(finality),
            settledAt: new Date().toISOString(),
            nonce: M.randomHex(12)
        };
        M.sha256Hex(JSON.stringify(entry)).then(function (hash) {
            entry.sealSHA256 = hash;
            ledger.unshift(entry);
            addLedgerRow(entry);

            var eurValue = q.amount / CBDC[from.value].perEUR;
            volumeEUR += eurValue;
            savingEUR += eurValue * (LEGACY_RATE - FEE_RATE);
            M.setText('kpi-volume', M.money(volumeEUR, 'EUR'));
            M.setText('kpi-count', String(ledger.length));
            M.setText('kpi-saving', M.money(savingEUR, 'EUR'));
            M.setText('stat-finality', finality + ' s');
            M.setText('stat-last-hash', hash.slice(0, 16) + '…');

            M.renderLog(terminal, [
                ['log-blue', '[INSTRUCT] ' + entry.reference + ' • ' + entry.messageStandard],
                ['log-gold', '[LOCK] ' + M.money(entry.sent, entry.from) + ' locked on ' + CBDC[entry.from].label + ' ledger (HTLC)'],
                ['log-gold', '[LOCK] ' + M.money(entry.received, entry.to) + ' locked on ' + CBDC[entry.to].label + ' ledger (HTLC)'],
                ['log-violet', '[PvP] Both legs verified → simultaneous release (no partial settlement possible)'],
                ['log-green', '[FINAL] Settled in ' + finality + ' s • Fee ' + M.money(entry.bridgeFee, entry.from)],
                ['', 'Seal SHA-256: ' + hash]
            ]);
        });
    }

    document.getElementById('cbdc-form').addEventListener('submit', settle);
    [from, to, amountEl].forEach(function (el) { el.addEventListener('input', quote); });
    document.getElementById('btn-swap').addEventListener('click', function () {
        var tmp = from.value;
        from.value = to.value;
        to.value = tmp;
        quote();
    });
    document.getElementById('btn-export-ledger').addEventListener('click', function () {
        M.downloadJSON('SR-CoreSync-Multi-CBDC-Ledger.json', {
            platform: 'S&R CoreSync Sovereign Multi-CBDC Cross-Border Bridge',
            mission: 105,
            exportedAt: new Date().toISOString(),
            note: 'Indicative reference rates; simulation environment.',
            totalVolumeEUR: Math.round(volumeEUR * 100) / 100,
            settlements: ledger
        });
    });

    renderEmpty();
    quote();
    M.renderLog(terminal, [
        ['log-blue', '[BRIDGE] Nodes online: ECB • SAMA • CBUAE • MAS'],
        ['log-green', 'Ready for atomic PvP settlement instructions.']
    ]);
})();
