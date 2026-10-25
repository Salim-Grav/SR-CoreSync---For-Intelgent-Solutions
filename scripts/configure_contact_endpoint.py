#!/usr/bin/env python3
"""Configure the contact form endpoint for all pages.

Primary  : https://api.sr-coresync.com/lead   (Cloudflare Worker, public + CORS)
Fallback : the n8n webhook (only useful when that host is publicly reachable)
Final    : mailto to info@sr-coresync.com so a lead is never lost

The Worker expects `clientName` plus `email` or `phone`; the other form fields
are folded into `notes` because the Worker whitelists a fixed field set.
Replaces the older `/* sr-contact-webhook */` block, so it is idempotent.
"""
import io
import os
import re

WORKER_ENDPOINT = "https://sr-lead-capture.sr-coresync.workers.dev/lead"
N8N_ENDPOINT = "http://localhost:5678/webhook/Contact"
MARK = "/* sr-contact-endpoint v2 */"

BLOCK = """<script>
%s
window.__SR_CONTACT_ENDPOINT__ = %r;
window.__SR_CONTACT_FALLBACK__ = %r;

window.submitContactForm = async function (event) {
    if (event && event.preventDefault) event.preventDefault();
    var form = (event && event.target) || document.querySelector('form.form-cta');
    if (!form) return;

    var btn = form.querySelector('button[type="submit"], input[type="submit"]');
    var label = btn ? (btn.innerHTML || btn.value) : '';
    if (btn) btn.disabled = true;

    function val(id, name) {
        var el = document.getElementById(id) || form.querySelector('[name="' + name + '"]');
        return el ? String(el.value || '').trim() : '';
    }

    var raw = {
        name: val('contact-name', 'name'),
        email: val('contact-email', 'email'),
        country: val('contact-country', 'country'),
        phone: val('contact-phone', 'phone'),
        service: val('contact-service', 'service'),
        budget: val('contact-budget', 'budget'),
        message: val('contact-details', 'details') || val('', 'message'),
        lang: document.documentElement.lang || 'ar',
        sourceUrl: location.href
    };

    // Worker schema (whitelisted fields).
    var workerPayload = {
        clientName: raw.name,
        email: raw.email,
        phone: raw.phone,
        companyName: raw.country,
        language: (raw.lang || 'ar').slice(0, 8),
        channel: 'contact-form',
        sourceUrl: raw.sourceUrl,
        notes: [
            raw.service ? ('Service: ' + raw.service) : '',
            raw.budget ? ('Budget: ' + raw.budget) : '',
            raw.message ? ('Details: ' + raw.message) : ''
        ].filter(Boolean).join(' | '),
        website: ''
    };

    async function post(url, body) {
        var res = await fetch(url, {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res;
    }

    var sent = false;
    try {
        await post(window.__SR_CONTACT_ENDPOINT__, workerPayload);
        sent = true;
    } catch (primaryError) {
        console.warn('Primary contact endpoint failed:', primaryError.message);
        try {
            await post(window.__SR_CONTACT_FALLBACK__, raw);
            sent = true;
        } catch (fallbackError) {
            console.error('Contact endpoints unavailable:', fallbackError.message);
        }
    }

    if (btn) { btn.disabled = false; if (btn.tagName === 'BUTTON') btn.innerHTML = label; else btn.value = label; }

    if (sent) {
        alert('\\u0634\\u0643\\u0631\\u0627\\u064b \\u0644\\u062a\\u0648\\u0627\\u0635\\u0644\\u0643 \\u0645\\u0639 S&R CoreSync For Intelligent Solutions! \\u062a\\u0645 \\u0627\\u0633\\u062a\\u0644\\u0627\\u0645 \\u0637\\u0644\\u0628\\u0643 \\u0648\\u0633\\u064a\\u062a\\u0648\\u0627\\u0635\\u0644 \\u0645\\u0639\\u0643 \\u0627\\u0644\\u0634\\u0631\\u064a\\u0643\\u0627\\u0646 \\u0627\\u0644\\u0645\\u0624\\u0633\\u0633\\u0627\\u0646 \\u0642\\u0631\\u064a\\u0628\\u0627\\u064b.');
        form.reset();
    } else {
        var line = [
            '\\u0627\\u0644\\u0627\\u0633\\u0645: ' + raw.name,
            '\\u0627\\u0644\\u0628\\u0631\\u064a\\u062f: ' + raw.email,
            '\\u0627\\u0644\\u0647\\u0627\\u062a\\u0641: ' + raw.phone,
            '\\u0627\\u0644\\u062f\\u0648\\u0644\\u0629: ' + raw.country,
            '\\u0627\\u0644\\u062e\\u062f\\u0645\\u0629: ' + raw.service,
            '\\u0627\\u0644\\u0645\\u064a\\u0632\\u0627\\u0646\\u064a\\u0629: ' + raw.budget,
            '\\u0627\\u0644\\u062a\\u0641\\u0627\\u0635\\u064a\\u0644: ' + raw.message
        ].join('\\n');
        window.location.href = 'mailto:info@sr-coresync.com?subject=' +
            encodeURIComponent('S&R CoreSync contact request') +
            '&body=' + encodeURIComponent(line);
    }
};

if (typeof window.openPublishSoftwareModal !== 'function') {
    window.openPublishSoftwareModal = function () {
        if (typeof window.sendDirectInfoEmail === 'function') {
            window.sendDirectInfoEmail('\\u0646\\u0634\\u0631 \\u0627\\u0644\\u0628\\u0631\\u0645\\u062c\\u064a\\u0627\\u062a \\u0639\\u0628\\u0631 S&R CoreSync');
        } else {
            window.location.href = 'mailto:info@sr-coresync.com?subject=' +
                encodeURIComponent('Publish software with S&R CoreSync');
        }
    };
}
</script>
""" % (MARK, WORKER_ENDPOINT, N8N_ENDPOINT)

OLD_MARK = "/* sr-contact-webhook */"

paths = ["index.html"]
for d in sorted(os.listdir(".")):
    if re.match(r"^[a-z]{2,3}$", d) and os.path.isfile(os.path.join(d, "index.html")):
        paths.append(os.path.join(d, "index.html"))

changed = 0
for path in paths:
    html = io.open(path, encoding="utf-8", errors="ignore").read()
    original = html

    # Repair stray text that an older script glued onto the form tag.
    html = re.sub(
        r'(onsubmit="submitContactForm\(event\)")\s*[^>]*?(?=data-success-msg=)',
        r"\1 ",
        html,
    )

    # Drop every previously injected variant of the block.
    html = re.sub(
        r"<script>\s*/\* sr-contact-(?:webhook|endpoint v2) \*/.*?</script>\s*",
        "",
        html,
        flags=re.S,
    )

    if "</body>" in html:
        html = html.replace("</body>", BLOCK + "</body>", 1)
    else:
        html += BLOCK

    if html != original:
        io.open(path, "w", encoding="utf-8", newline="").write(html)
        changed += 1
        print("updated", path)

print("pages updated:", changed)
