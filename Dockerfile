# ==============================================================================
# S&R CoreSync For Intelligent Solutions - Sovereign Cloud Production Container
# High-Performance Nginx Alpine Web Server with 8K Asset Caching & Security
#
# [P0-3] إعادة بناء آمنة: سياق البناء نفسه مقيّد بقائمة بيضاء صارمة عبر
#        .dockerignore (منع-افتراضي). لا يُنسخ إلى الـ webroot إلا أصول الموقع
#        العامة: صفحات HTML، مجلدات الأصول، ومجلدات اللغات.
#        الملفات المستبعدة نهائياً من سياق البناء تشمل:
#          .env.vault / *.db / *.log / uploads/ / chat_history.txt /
#          كامل الكود البرمجي (Python) / سكربتات التشغيل / وثائق التشغيل الداخلية
#        بحيث يستحيل تسريب خزنة الأسرار أو قواعد بيانات الجلسات داخل الصورة.
# ==============================================================================

FROM nginx:1.27-alpine

LABEL maintainer="S&R CoreSync Engineering <dev@sr-coresync.com>"
LABEL description="S&R CoreSync Omnichannel 8K & Sovereign Cloud Web Platform"
LABEL version="2026.1.1"
LABEL security.p0="whitelist-build-context (see .dockerignore)"

# Remove default nginx configurations
RUN rm -rf /etc/nginx/conf.d/* /usr/share/nginx/html/*

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy production web assets (whitelisted exclusively by .dockerignore)
COPY . /usr/share/nginx/html/

# Defense-in-depth: أي ملف حساس تسرب للمصادفة عبر سياق البناء يُحذف من الصورة
# (هذه طبقة احتياطية ثانية؛ القاعدة الأساسية هي .dockerignore)
RUN rm -rf /usr/share/nginx/html/.git* \
           /usr/share/nginx/html/.env* \
           /usr/share/nginx/html/.github \
           /usr/share/nginx/html/.vscode \
           /usr/share/nginx/html/.secrets \
           /usr/share/nginx/html/.agents \
           /usr/share/nginx/html/.githooks \
           /usr/share/nginx/html/.zwork \
           /usr/share/nginx/html/*.db \
           /usr/share/nginx/html/*.log \
           /usr/share/nginx/html/*.py \
           /usr/share/nginx/html/*.bat \
           /usr/share/nginx/html/*.sh \
           /usr/share/nginx/html/*.ps1 \
           /usr/share/nginx/html/*.url \
           /usr/share/nginx/html/*.md \
           /usr/share/nginx/html/scripts \
           /usr/share/nginx/html/sdk \
           /usr/share/nginx/html/uploads \
           /usr/share/nginx/html/workers \
           /usr/share/nginx/html/deploy \
           /usr/share/nginx/html/docs \
           /usr/share/nginx/html/dist \
           /usr/share/nginx/html/archive_agents \
           /usr/share/nginx/html/templates || true

# Set proper ownership and permissions for nginx
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    find /usr/share/nginx/html -type f -exec chmod 644 {} + && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx

# Healthcheck (على /robots.txt الموجودة فعلاً في الـ webroot)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:80/robots.txt || exit 1

# Expose HTTP port
EXPOSE 80

# Run Nginx in foreground as non-root user
USER nginx
CMD ["nginx", "-g", "daemon off;"]
