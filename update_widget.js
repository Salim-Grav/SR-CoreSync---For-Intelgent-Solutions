const fs = require('fs');
let s = fs.readFileSync('js/sr-agent-widget.js', 'utf8');

// 1. Add upload button & hidden file input inside form
const oldFormInput = 'id="sr-agent-mic"';
if (s.includes(oldFormInput)) {
    const targetBlock = `<button type="button" class="sr-agent-mic-btn" id="sr-agent-mic"`;
    const newButtons = `<input type="file" id="sr-agent-file-input" accept=".pdf,.docx,.txt,.md" multiple style="display:none;">
                    <button type="button" class="sr-agent-upload-btn" id="sr-agent-upload" title="إرفاق مستند للتحليل الذكي والفهرسة (PDF / DOCX - بحد أقصى 5MB)">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
                        </svg>
                    </button>
                    ${targetBlock}`;
    s = s.replace(targetBlock, newButtons);
    console.log('Button inserted');
}

// 2. Add element declarations
const oldElems = `const micBtn = document.getElementById('sr-agent-mic');`;
const newElems = `${oldElems}
        const uploadBtn = document.getElementById('sr-agent-upload');
        const fileInput = document.getElementById('sr-agent-file-input');`;
if (s.includes(oldElems)) {
    s = s.replace(oldElems, newElems);
    console.log('Hooks inserted');
}

// 3. Add upload handling logic
const uploadCode = `
        // معالجة رفع وإرفاق المستندات للتحليل عبر RAG
        if (uploadBtn && fileInput) {
            uploadBtn.addEventListener('click', () => {
                fileInput.click();
            });

            fileInput.addEventListener('change', async (e) => {
                const files = e.target.files;
                if (!files || files.length === 0) return;

                const uploadEndpoint = API_ENDPOINT.replace(/\\/api\\/(ai-concierge|chat)$/, '/api/upload');
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    if (file.size > 5 * 1024 * 1024) {
                        appendMessage(\`⚠️ الملف "\${file.name}" يتجاوز الحد الأقصى المسموح به (5 ميجابايت).\`, false);
                        continue;
                    }

                    appendMessage(\`📎 جاري رفع وتحليل المستند: **\${file.name}** (\${(file.size / 1024).toFixed(1)} KB)...\`, true);
                    typingEl.style.display = 'inline-flex';
                    messagesEl.scrollTop = messagesEl.scrollHeight;

                    const formData = new FormData();
                    formData.append('files', file);

                    try {
                        const res = await fetch(uploadEndpoint, {
                            method: 'POST',
                            body: formData
                        });
                        typingEl.style.display = 'none';

                        if (!res.ok) {
                            const errData = await res.json().catch(() => ({}));
                            throw new Error(errData.detail || ('HTTP ' + res.status));
                        }

                        const data = await res.json();
                        appendMessage(\`✅ تم استخراج نصوص **\${file.name}** وفهرستها بنجاح في قاعدة المعرفة السيادية (RAG)! يمكنك الآن توجيه أي أسئلة حول محتوى المستند.\`, false);
                    } catch (err) {
                        typingEl.style.display = 'none';
                        appendMessage(\`❌ تعذر تحليل المستند "\${file.name}": \${err.message}\`, false);
                    }
                }
                fileInput.value = '';
            });
        }
`;

const voiceStateComment = 'let currentVoiceLang = \'ar-SA\';';
if (s.includes(voiceStateComment)) {
    s = s.replace(voiceStateComment, voiceStateComment + '\n' + uploadCode);
    console.log('Upload code inserted');
}

fs.writeFileSync('js/sr-agent-widget.js', s, 'utf8');
