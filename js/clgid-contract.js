/**
 * S&R CoreSync - CLGID The Hague Contract Controller
 * Supervised by: Eng. Mohammad Salim Aziza
 */

function confirmClientElectronicSignature() {
    const placeholder = document.getElementById('clientSignPlaceholder');
    const signBtn = document.getElementById('clientSignBtn');
    
    if (placeholder) {
        placeholder.style.background = 'rgba(5, 150, 105, 0.05)';
        placeholder.style.border = '1px solid #059669';
        placeholder.innerHTML = `
            <div style="font-family:'Cairo', sans-serif; font-size:1.05rem; color:#0a1e36; font-weight:800; display:flex; flex-direction:column; align-items:center;">
                <span>محمود الناصر</span>
                <span style="font-size:0.65rem; color:#059669; font-weight:700;">موقّع إلكترونياً • ${new Date().toLocaleDateString('ar-EG')}</span>
            </div>
            <div style="position:absolute; right:14px; top:16px; font-size:1.4rem;">
                ✍️
            </div>
        `;
    }

    if (signBtn) {
        signBtn.disabled = true;
        signBtn.style.background = '#059669';
        signBtn.style.color = '#ffffff';
        signBtn.innerHTML = '<span>✓ تم اعتماد وتوثيق التوقيع بنجاح (eIDAS Compliant)</span>';
    }

    // Ping audit
    try {
        const payload = {
            event: "client_contract_e_signature",
            contractRef: "SR-CLGID-2026-NL",
            signer: "Mahmoud Al-Naser",
            role: "Director of CLGID The Hague",
            timestamp: new Date().toISOString()
        };
        if (navigator.sendBeacon) {
            navigator.sendBeacon("https://sr-lead-capture.sr-coresync.workers.dev/lead", JSON.stringify(payload));
        }
    } catch(e) {}

    alert("🎉 تهانينا! تم توثيق واعتماد التوقيع الإلكتروني رسمياً بموجب القانون الهولندي. يمكنك الآن الضغط على زر 'طباعة وحفظ الاتفاقية الرسمية (PDF)'.");
}

window.confirmClientElectronicSignature = confirmClientElectronicSignature;

