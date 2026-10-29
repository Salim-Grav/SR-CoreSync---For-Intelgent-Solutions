/*
 * S&R CoreSync For Intelligent Solutions - Sovereign Mission Core Utilities (Missions 104-106)
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training is prohibited.
 *
 * External (non-inline) script: compatible with the strict hash-based CSP without new hashes.
 */
(function (global) {
    'use strict';

    function toHex(buffer) {
        var bytes = new Uint8Array(buffer);
        var out = '';
        for (var i = 0; i < bytes.length; i++) {
            out += ('0' + bytes[i].toString(16)).slice(-2);
        }
        return out;
    }

    /** Real SHA-256 via WebCrypto (falls back to a deterministic FNV digest on insecure origins). */
    function sha256Hex(text) {
        if (global.crypto && global.crypto.subtle && global.TextEncoder) {
            return global.crypto.subtle.digest('SHA-256', new TextEncoder().encode(text)).then(toHex);
        }
        var h = 0x811c9dc5;
        var out = '';
        for (var round = 0; round < 8; round++) {
            for (var i = 0; i < text.length; i++) {
                h ^= text.charCodeAt(i) + round;
                h = (h * 0x01000193) >>> 0;
            }
            out += ('00000000' + h.toString(16)).slice(-8);
        }
        return Promise.resolve(out);
    }

    function randomHex(bytes) {
        var arr = new Uint8Array(bytes);
        if (global.crypto && global.crypto.getRandomValues) {
            global.crypto.getRandomValues(arr);
        } else {
            for (var i = 0; i < bytes; i++) { arr[i] = Math.floor(Math.random() * 256); }
        }
        return toHex(arr.buffer);
    }

    function downloadJSON(filename, payload) {
        var blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(function () { URL.revokeObjectURL(url); }, 0);
    }

    function setText(id, value) {
        var el = document.getElementById(id);
        if (el) { el.textContent = value; }
    }

    /** Renders log lines safely (textContent only - no HTML injection). lines: [[cssClass, text], ...] */
    function renderLog(container, lines) {
        if (!container) { return; }
        container.textContent = '';
        lines.forEach(function (line) {
            var div = document.createElement('div');
            if (line[0]) { div.className = line[0]; }
            div.textContent = line[1];
            container.appendChild(div);
        });
    }

    function money(value, currency) {
        try {
            return new Intl.NumberFormat('en-US', { style: 'currency', currency: currency, maximumFractionDigits: 2 }).format(value);
        } catch (e) {
            return currency + ' ' + Number(value).toLocaleString('en-US', { maximumFractionDigits: 2 });
        }
    }

    /** Activates one item in a group of selectable buttons and returns its dataset. */
    function bindSelectable(selector, onSelect) {
        var items = Array.prototype.slice.call(document.querySelectorAll(selector));
        items.forEach(function (item) {
            item.addEventListener('click', function () {
                items.forEach(function (el) {
                    el.classList.remove('active');
                    el.setAttribute('aria-pressed', 'false');
                });
                item.classList.add('active');
                item.setAttribute('aria-pressed', 'true');
                onSelect(item.dataset, item);
            });
        });
        return items;
    }

    global.SRMission = {
        sha256Hex: sha256Hex,
        randomHex: randomHex,
        downloadJSON: downloadJSON,
        setText: setText,
        renderLog: renderLog,
        money: money,
        bindSelectable: bindSelectable
    };
})(window);
