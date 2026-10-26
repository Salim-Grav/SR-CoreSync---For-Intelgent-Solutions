const fs = require('fs');
const path = require('path');

const enPath = path.resolve(__dirname, '../en/index.html');
let enHtml = fs.readFileSync(enPath, 'utf8');

// Replace the call-opt-row for phone and whatsapp with Salim and Raed in en/index.html
const startIdx = enHtml.indexOf('<a href="tel:+31618111116" class="call-opt-row">');
const endMarker = '<a href="mailto:info@sr-coresync.com" class="call-opt-row">';
const endIdx = enHtml.indexOf(endMarker);

if (startIdx !== -1 && endIdx !== -1) {
  const replacement = `<a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row mb-2">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 32 32" width="22" height="22" fill="#10b981"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                    <div>
                        <div class="fw-bold">Mohammad Salim Aziza <span style="background:rgba(16,185,129,0.15);color:#10b981;padding:2px 8px;border-radius:4px;font-size:11px;">CTO</span></div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">+31 6 1811 1116 (WhatsApp / Call)</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">Direct Contact ←</span>
            </a>

            <a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row mb-2">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 32 32" width="22" height="22" fill="#c5a880"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                    <div>
                        <div class="fw-bold">Mohammad Raed Kaakeh <span style="background:rgba(197,168,128,0.15);color:#c5a880;padding:2px 8px;border-radius:4px;font-size:11px;">CFO</span></div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">+31 6 1811 1116 (WhatsApp / Call)</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">Direct Contact ←</span>
            </a>\n\n            `;

  enHtml = enHtml.substring(0, startIdx) + replacement + enHtml.substring(endIdx);
  fs.writeFileSync(enPath, enHtml, 'utf8');
  console.log('✅ Successfully updated directCallModal in en/index.html');
} else {
  console.log('Indices:', startIdx, endIdx);
}
