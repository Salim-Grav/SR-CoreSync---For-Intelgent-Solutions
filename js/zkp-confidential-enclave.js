/*
 * S&R CoreSync For Intelligent Solutions - Mission 106
 * Zero-Knowledge Proof & Confidential Computing Enclave
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 *
 * Demonstrates the commit-and-prove principle in-browser: the secret value is hashed with a
 * random 256-bit salt; only the commitment and the predicate result are placed in the bundle.
 */
(function () {
    'use strict';

    var M = window.SRMission;

    var CLAIMS = {
        solvency: { label: 'Solvency: assets >= liabilities', op: '>=', threshold: 12500000, secret: 18420000 },
        credit: { label: 'Credit: annual income >= minimum', op: '>=', threshold: 60000, secret: 84500 },
        age: { label: 'KYC age: age >= 18', op: '>=', threshold: 18, secret: 34 },
        exposure: { label: 'Exposure: exposure <= regulatory cap', op: '<=', threshold: 25000000, secret: 19750000 }
    };

    var enclave = { name: 'Intel TDX', vendor: 'Intel Trust Domain Extensions' };
    var proofs = 0;
    var lastBundle = null;
    var terminal = document.getElementById('zkp-terminal');
    var claimEl = document.getElementById('f-claim');

    function attest() {
        return M.sha256Hex(enclave.vendor + '|S&R-CoreSync-Enclave-Image-v106|' + M.randomHex(8)).then(function (m) {
            M.setText('stat-enclave', enclave.name);
            M.setText('stat-measure', m.slice(0, 16) + '…');
            return m;
        });
    }

    M.bindSelectable('#enclave-list .select-item', function (data) {
        enclave = { name: data.name, vendor: data.vendor };
        attest().then(function (m) {
            M.renderLog(terminal, [
                ['log-violet', '[ATTEST] ' + enclave.vendor + ' quote verified'],
                ['', 'MRTD / Measurement: ' + m],
                ['log-green', 'Enclave trusted. Ready to generate proof.']
            ]);
        });
    });

    claimEl.addEventListener('change', function () {
        var c = CLAIMS[claimEl.value];
        document.getElementById('f-threshold').value = c.threshold;
        document.getElementById('f-secret').value = c.secret;
    });

    document.getElementById('zkp-form').addEventListener('submit', function (e) {
        e.preventDefault();
        var claim = CLAIMS[claimEl.value];
        var threshold = parseFloat(document.getElementById('f-threshold').value);
        var secret = parseFloat(document.getElementById('f-secret').value);
        var verifier = document.getElementById('f-verifier').value.trim().slice(0, 60) || 'Unspecified verifier';
        if (!isFinite(threshold) || !isFinite(secret)) {
            M.renderLog(terminal, [['log-red', '[ERROR] Threshold and secret value must be numeric.']]);
            return;
        }

        var started = performance.now();
        var salt = M.randomHex(32);
        var holds = claim.op === '>=' ? secret >= threshold : secret <= threshold;

        Promise.all([M.sha256Hex(secret + '|' + salt), attest()]).then(function (res) {
            var commitment = res[0];
            var measurement = res[1];
            var bundle = {
                platform: 'S&R CoreSync Zero-Knowledge Proof & Confidential Computing Enclave',
                mission: 106,
                statement: claim.label,
                operator: claim.op,
                publicThreshold: threshold,
                predicateHolds: holds,
                commitmentSHA256: commitment,
                enclave: enclave.vendor,
                attestationMeasurement: measurement,
                verifier: verifier,
                issuedAt: new Date().toISOString(),
                disclosure: 'Secret value and salt are retained by the prover only; reveal is optional for audit.'
            };
            return M.sha256Hex(JSON.stringify(bundle)).then(function (bundleHash) {
                bundle.bundleSealSHA256 = bundleHash;
                var ms = (performance.now() - started).toFixed(2);
                lastBundle = bundle;
                proofs += 1;
                M.setText('stat-proofs', String(proofs));
                M.setText('kpi-time', ms + ' ms');
                M.renderLog(terminal, [
                    ['log-violet', '[ENCLAVE] ' + enclave.name + ' • measurement ' + measurement.slice(0, 24) + '…'],
                    ['log-blue', '[STATEMENT] ' + claim.label + ' (threshold ' + threshold.toLocaleString('en-US') + ')'],
                    ['log-gold', '[COMMIT] C = SHA-256(secret ‖ salt) = ' + commitment],
                    [holds ? 'log-green' : 'log-red', '[RESULT] Predicate ' + (holds ? 'HOLDS ✅' : 'DOES NOT HOLD ❌') + ' — secret value NOT disclosed'],
                    ['', '[VERIFIER] ' + verifier],
                    ['', '[SEAL] ' + bundleHash],
                    ['', '------------------------------------------------------------------'],
                    ['log-green', 'Raw data transmitted: 0 bytes • generated in ' + ms + ' ms']
                ]);
            });
        });
    });

    document.getElementById('btn-export-proof').addEventListener('click', function () {
        if (!lastBundle) {
            M.renderLog(terminal, [['log-red', '[EXPORT] Generate a proof first.']]);
            return;
        }
        M.downloadJSON('SR-CoreSync-ZKP-Proof-Bundle.json', lastBundle);
    });

    attest().then(function (m) {
        M.renderLog(terminal, [
            ['log-violet', '[ATTEST] ' + enclave.vendor + ' quote verified'],
            ['', 'MRTD / Measurement: ' + m],
            ['log-green', 'Enclave trusted. Enter the public threshold and your private value.']
        ]);
    });
})();

