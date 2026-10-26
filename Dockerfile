# ==============================================================================
# S&R CoreSync For Intelligent Solutions - Sovereign Cloud Production Container
# High-Performance Nginx Alpine Web Server with 8K Asset Caching & Security
# ==============================================================================

FROM nginx:1.27-alpine

LABEL maintainer="S&R CoreSync Engineering <dev@sr-coresync.com>"
LABEL description="S&R CoreSync Omnichannel 8K & Sovereign Cloud Web Platform"
LABEL version="2026.1.0"

# Remove default nginx configurations
RUN rm -rf /etc/nginx/conf.d/* /usr/share/nginx/html/*

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy production web assets
COPY . /usr/share/nginx/html/

# Clean up development & VCS files from the runtime webroot
RUN rm -rf /usr/share/nginx/html/.git \
           /usr/share/nginx/html/.github \
           /usr/share/nginx/html/.vscode \
           /usr/share/nginx/html/.secrets \
           /usr/share/nginx/html/.agents \
           /usr/share/nginx/html/.zwork \
           /usr/share/nginx/html/*.bat \
           /usr/share/nginx/html/*.sh \
           /usr/share/nginx/html/*.url

# Set proper ownership and permissions for nginx
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:80/robots.txt || exit 1

# Expose HTTP port
EXPOSE 80

# Run Nginx in foreground as non-root user
USER nginx
CMD ["nginx", "-g", "daemon off;"]
