const fs = require('fs');
const path = require('path');

// 1. Update index.html directCallModal
const indexPath = path.resolve(__dirname, '../index.html');
let indexHtml = fs.readFileSync(indexPath, 'utf8');

const arOldBlock = `<a href="tel:+31618111116" class="call-opt-row">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    <div>
                        <div class="fw-bold">مكالمة هاتفية دولية</div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">+31 6 1811 1116</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">اتصل الآن ←</span>
            </a>

            <a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 32 32" width="20" height="20" fill="currentColor"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                    <div>
                        <div class="fw-bold">محادثة واتساب فورية</div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">رد خلال دقائق معدودة</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">محادثة ←</span>
            </a>`;

const arNewBlock = `<a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row mb-2">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 32 32" width="22" height="22" fill="#10b981"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                    <div>
                        <div class="fw-bold">م. محمد سليم عزيزة <span class="badge-role-tag" style="background:rgba(16,185,129,0.15);color:#10b981;padding:2px 8px;border-radius:4px;font-size:11px;">CTO</span></div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">+31 6 1811 1116 (واتساب / هاتف)</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">تواصل مباشر ←</span>
            </a>

            <a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row mb-2">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 32 32" width="22" height="22" fill="#c5a880"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                    <div>
                        <div class="fw-bold">أ. محمد رائد كعكة <span class="badge-role-tag" style="background:rgba(197,168,128,0.15);color:#c5a880;padding:2px 8px;border-radius:4px;font-size:11px;">CFO</span></div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">+31 6 1811 1116 (واتساب / هاتف)</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">تواصل مباشر ←</span>
            </a>`;

// Normalize line endings to match file
const normalizedOld = arOldBlock.replace(/\r?\n/g, '\r\n');
const normalizedNew = arNewBlock.replace(/\r?\n/g, '\r\n');

if (indexHtml.includes(normalizedOld)) {
  indexHtml = indexHtml.replace(normalizedOld, normalizedNew);
  fs.writeFileSync(indexPath, indexHtml, 'utf8');
  console.log('✅ Updated directCallModal in index.html (Arabic)');
} else if (indexHtml.includes(arOldBlock)) {
  indexHtml = indexHtml.replace(arOldBlock, arNewBlock);
  fs.writeFileSync(indexPath, indexHtml, 'utf8');
  console.log('✅ Updated directCallModal in index.html (Arabic LF)');
} else {
  console.log('ℹ️ directCallModal in index.html already updated or differs');
}

// 2. Update nl/index.html
const nlPath = path.resolve(__dirname, '../nl/index.html');
let nlHtml = fs.readFileSync(nlPath, 'utf8');

const nlOldBlock = `<a href="tel:+31618111116" class="call-opt-row">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    <div>
                        <div class="fw-bold">Internationaal Telefoongesprek</div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">+31 6 1811 1116</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">Bel Nu ←</span>
            </a>

            <a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 32 32" width="20" height="20" fill="currentColor"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                    <div>
                        <div class="fw-bold">Direct WhatsApp Kanaal</div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">Reactie binnen enkele minuten</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">Stuur Bericht ←</span>
            </a>`;

const nlNewBlock = `<a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row mb-2">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 32 32" width="22" height="22" fill="#10b981"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                    <div>
                        <div class="fw-bold">Mohammad Salim Aziza <span style="background:rgba(16,185,129,0.15);color:#10b981;padding:2px 8px;border-radius:4px;font-size:11px;">CTO</span></div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">+31 6 1811 1116 (WhatsApp / Bel)</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">Direct Contact ←</span>
            </a>

            <a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row mb-2">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 32 32" width="22" height="22" fill="#c5a880"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                    <div>
                        <div class="fw-bold">Mohammad Raed Kaakeh <span style="background:rgba(197,168,128,0.15);color:#c5a880;padding:2px 8px;border-radius:4px;font-size:11px;">CFO</span></div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">+31 6 1811 1116 (WhatsApp / Bel)</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">Direct Contact ←</span>
            </a>`;

const nlNormOld = nlOldBlock.replace(/\r?\n/g, '\r\n');
const nlNormNew = nlNewBlock.replace(/\r?\n/g, '\r\n');

if (nlHtml.includes(nlNormOld)) {
  nlHtml = nlHtml.replace(nlNormOld, nlNormNew);
  fs.writeFileSync(nlPath, nlHtml, 'utf8');
  console.log('✅ Updated directCallModal in nl/index.html (Dutch)');
} else if (nlHtml.includes(nlOldBlock)) {
  nlHtml = nlHtml.replace(nlOldBlock, nlNewBlock);
  fs.writeFileSync(nlPath, nlHtml, 'utf8');
  console.log('✅ Updated directCallModal in nl/index.html (Dutch LF)');
} else {
  console.log('ℹ️ directCallModal in nl/index.html already updated or differs');
}

// 3. Update en/index.html
const enPath = path.resolve(__dirname, '../en/index.html');
let enHtml = fs.readFileSync(enPath, 'utf8');

const enOldBlock = `<a href="tel:+31618111116" class="call-opt-row">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    <div>
                        <div class="fw-bold">International Phone Call</div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">+31 6 1811 1116</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">Call Now ←</span>
            </a>

            <a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row">
                <div class="d-flex align-items-center gap-3">
                    <svg viewBox="0 0 32 32" width="20" height="20" fill="currentColor"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                    <div>
                        <div class="fw-bold">Direct WhatsApp Chat</div>
                        <div class="text-caption text-white-64 font-latin" dir="ltr">Response within minutes</div>
                    </div>
                </div>
                <span class="text-caption text-primary gold-accent">Chat Now ←</span>
            </a>`;

const enNewBlock = `<a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="call-opt-row mb-2">
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
            </a>`;

const enNormOld = enOldBlock.replace(/\r?\n/g, '\r\n');
const enNormNew = enNewBlock.replace(/\r?\n/g, '\r\n');

if (enHtml.includes(enNormOld)) {
  enHtml = enHtml.replace(enNormOld, enNormNew);
  fs.writeFileSync(enPath, enHtml, 'utf8');
  console.log('✅ Updated directCallModal in en/index.html (English)');
} else if (enHtml.includes(enOldBlock)) {
  enHtml = enHtml.replace(enOldBlock, enNewBlock);
  fs.writeFileSync(enPath, enHtml, 'utf8');
  console.log('✅ Updated directCallModal in en/index.html (English LF)');
} else {
  console.log('ℹ️ directCallModal in en/index.html already updated or differs');
}
