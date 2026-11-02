/**
 * S&R CoreSync - CLGID The Hague Interactive Prototype Controller
 * Supervised by: Eng. Mohammad Salim Aziza
 */

function publishClgidArticle(e) {
    if (e && e.preventDefault) e.preventDefault();
    const titleInput = document.getElementById('articleTitleInput');
    const catInput = document.getElementById('articleCategoryInput');
    const feed = document.getElementById('clgidArticlesFeed');
    
    if (!titleInput || !feed) return;
    const title = titleInput.value.trim();
    const cat = catInput ? catInput.value : 'أخبار المركز';
    if (!title) return;

    const newCard = document.createElement('div');
    newCard.style.cssText = "background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3); border-radius:8px; padding:12px 16px; display:flex; justify-content:space-between; align-items:center; animation: fadeIn 0.3s ease;";
    newCard.innerHTML = `
        <div>
            <span style="font-size:0.75rem; color:#34d399; font-weight:700;">[${cat}]</span>
            <strong style="color:#ffffff; margin-inline-start:8px;">${title}</strong>
        </div>
        <span style="font-size:0.75rem; color:#34d399; font-weight:700;">✓ نُشر للتو على الموقع!</span>
    `;

    feed.prepend(newCard);
    titleInput.value = '';
    alert('🎉 تم نشر المقال بنجاح تام! هذا مثال حي على سهولة إدارة المحتوى في الموقع الجديد.');
}

window.publishClgidArticle = publishClgidArticle;
