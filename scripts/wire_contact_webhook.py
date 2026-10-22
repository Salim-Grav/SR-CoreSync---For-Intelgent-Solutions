#!/usr/bin/env python3
"""Wire the contact webhook and close the last dead handlers.

Adds to every page:
  * submitContactForm(event)  -> POST JSON to the n8n contact webhook
  * openPublishSoftwareModal  -> real fallback (email) instead of undefined
And loads the software-apps bundle on /ckb/ which was still missing it.
"""
import io
import os
import re

WEBHOOK = "http://localhost:5678/webhook/Contact"

BLOCK_MARK = "/* sr-contact-webhook */"
BLOCK = """<script>
%s
window.submitContactForm = async function (event) {
    if (event && event.preventDefault) event.preventDefault();
    var form = (event && event.target) || document.querySelector('form.form-cta');
    if (!form) return;
    var btn = form.querySelector('button[type="submit"], input[type="submit"]');
    var label = btn ? (btn.innerHTML || btn.value) : '';
    if (btn) { btn.disabled = true; }

    function val(id, name) {
        var el = document.getElementById(id) || form.querySelector('[name="' + name + '"]');
        return el ? el.value : '';
    }

    var payload = {
        name: val('contact-name', 'name'),
        email: val('contact-email', 'email'),
        country: val('contact-country', 'country'),
        phone: val('contact-phone', 'phone'),
        service: val('contact-service', 'service'),
        budget: val('contact-budget', 'budget'),
        message: val('contact-details', 'details') || val('', 'message'),
        source: location.pathname,
        page: document.title,
        lang: document.documentElement.lang || 'ar',
        timestamp: new Date().toISOString()
    };

    try {
        var res = await fetch('%s', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        alert('\\u0634\\u0643\\u0631\\u0627\\u064b \\u0644\\u062a\\u0648\\u0627\\u0635\\u0644\\u0643 \\u0645\\u0639 S&R CoreSync Solutions! \\u062a\\u0645 \\u0627\\u0633\\u062a\\u0644\\u0627\\u0645 \\u0637\\u0644\\u0628\\u0643 \\u0648\\u0633\\u064a\\u062a\\u0648\\u0627\\u0635\\u0644 \\u0645\\u0639\\u0643 \\u0627\\u0644\\u0634\\u0631\\u064a\\u0643\\u0627\\u0646 \\u0627\\u0644\\u0645\\u0624\\u0633\\u0633\\u0627\\u0646 \\u0642\\u0631\\u064a\\u0628\\u0627\\u064b.');
        form.reset();
    } catch (err) {
        console.error('Webhook Error:', err);
        alert('\\u062a\\u0639\\u0630\\u0631 \\u0627\\u0644\\u0627\\u062a\\u0635\\u0627\\u0644 \\u0628\\u0627\\u0644\\u062e\\u0627\\u062f\\u0645. \\u064a\\u0631\\u062c\\u0649 \\u0627\\u0644\\u0645\\u062d\\u0627\\u0648\\u0644\\u0629 \\u0644\\u0627\\u062d\\u0642\\u0627\\u064b \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0648\\u0627\\u0635\\u0644 \\u0639\\u0628\\u0631 info@sr-coresync.com');
    } finally {
        if (btn) { btn.disabled = false; if (btn.tagName === 'BUTTON') btn.innerHTML = label; else btn.value = label; }
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
""" % (BLOCK_MARK, WEBHOOK)

paths = ["index.html"]
for d in sorted(os.listdir(".")):
    if re.match(r"^[a-z]{2}$", d) and os.path.isfile(os.path.join(d, "index.html")):
        paths.append(os.path.join(d, "index.html"))

changed = 0
for path in paths:
    html = io.open(path, encoding="utf-8", errors="ignore").read()
    original = html

    if BLOCK_MARK not in html:
        if not re.search(r"<script>\s*/\* sr-contact-webhook \*/", html):
            if "</body>" in html:
                html = html.replace("</body>", BLOCK + "</body>", 1)
            else:
                html += BLOCK

    if path != "index.html":
        if "js/sr-software-apps.js" not in html:
            html = html.replace(
                "</body>",
                '    <script src="../js/sr-software-apps.js"></script>\n</body>',
                1,
            )
        if "css/sr-software-apps.css" not in html:
            html = html.replace(
                "</head>",
                '    <link rel="stylesheet" href="../css/sr-software-apps.css?v=20261020_center">\n</head>',
                1,
            )

    if html != original:
        io.open(path, "w", encoding="utf-8", newline="").write(html)
        changed += 1
        print("updated", path)

print("pages updated:", changed)
