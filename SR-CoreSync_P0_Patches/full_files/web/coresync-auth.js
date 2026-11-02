/*
 ==============================================================================
 S&R CoreSync - جسر مصادقة الواجهة الأمامية (تكامل إصلاح P0-1)
 ==============================================================================
 بعد تفعيل المصادقة الإلزامية على الخادم، تحتاج صفحات الواجهة (المحاكي،
 لوحة القيادة، ويدجت المحادثة) إلى إرسال مفتاح API مع كل نداء.

 الاستخدام:
   1) ضع مفتاح العميل (دور client) في التخزين المحلي مرة واحدة:
        localStorage.setItem('CORESYNC_API_KEY', 'srk_xxxxxxxxxxxx');
      (يمكن تنفيذ ذلك من صفحة إعدادات داخلية أو يدوياً من كونسول المتصفح
       على الأجهزة الموثوقة فقط — لا تضع مفاتيح admin في أي صفحة عامة)

   2) أدرج هذا الملف قبل أي سكربت يستدعي /api/:
        <script src="/coresync-auth.js"></script>

 الملاحظات:
   - يضيف الجسر ترويسة X-API-Key تلقائياً لكل fetch يوجه نحو /api/.
   - قنوات EventSource (SSE) لا تدعم الترويسات المخصصة؛ استخدم
     coresyncEventSource(url) الموفرة هنا، أو حوّل إلى fetch-based SSE.
   - مفاتيح client للقراءة/المحادثة فقط؛ العمليات الإدارية تبقى عبر قنوات آمنة.
   - المفتاح يبقى في متصفح المستخدم؛ لا تنشر صفحة تحتوي مفتاح admin أبداً.
 ============================================================================== */
(function () {
  'use strict';
  var KEY_NAME = 'CORESYNC_API_KEY';
  var originalFetch = window.fetch ? window.fetch.bind(window) : null;
  if (!originalFetch) return;

  window.fetch = function (input, init) {
    try {
      var url = typeof input === 'string' ? input : (input && input.url) || '';
      var needsAuth = url.indexOf('/api/') !== -1;
      var key = null;
      try { key = localStorage.getItem(KEY_NAME); } catch (e) { key = null; }
      if (needsAuth && key) {
        init = init || {};
        var source = init.headers || (input && input.headers) || {};
        var headers = new Headers(source);
        if (!headers.has('X-API-Key')) headers.set('X-API-Key', key);
        init.headers = headers;
      }
    } catch (e) { /* لا نعطل الموقع أبداً عند فشل الجسر */ }
    return originalFetch(input, init);
  };

  /**
   * بديل جاهز لقنوات SSE: EventSource لا يقبل ترويسات، لذا يُمرَّر
   * المفتاح كمعامل استعلام (?api_key=...) — مدعوم صراحة في وسيلة المصادقة.
   * استخدمه فقط عبر HTTPS على نطاق موثوق.
   */
  window.coresyncEventSource = function (url) {
    var key = '';
    try { key = localStorage.getItem(KEY_NAME) || ''; } catch (e) { key = ''; }
    var joiner = url.indexOf('?') === -1 ? '?' : '&';
    return new EventSource(url + joiner + 'api_key=' + encodeURIComponent(key));
  };
})();
