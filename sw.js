// S&R CoreSync For Intelligent Solutions - Enterprise Pre-render & Ultra-Low TTFB Service Worker
// Version: coresync-prerender-v16-offline
const CACHE_NAME = 'coresync-prerender-v16-offline';

// 1. Critical assets: everything the first screen needs to paint.
// Anything that is only reachable after a scroll (founder banners, portraits,
// NFC cards, e-mail/portal documents) belongs in SECONDARY_ASSETS instead:
// precaching it on install made the first visit pull ~3.5 MB and starved the
// LCP request on mobile connections.
const CRITICAL_ASSETS = [
  './index.html',
  './manifest.json',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/icon-maskable-192.png',
  './assets/icon-maskable-512.png',
  './assets/sr-core-emblem.svg?v=sovereign2026',
  './assets/sr-core-emblem-official.webp',
  './assets/logo-neon-icon.svg',
  './assets/sr-emblem-gold-luxury.webp',
  './assets/about-founder-poster.webp',
  './css/dananajmah-bundle.min.css',
  './css/enterprise-suite.min.css',
  './css/concierge.css',
  './css/sr-analytics.css',
  './js/enterprise-suite.min.js',
  './js/concierge.js',
  './js/sr-analytics.js',
  './offline.html'
];

// 2. Secondary assets: Cached gently in an idle background queue without choking Smart TV connections.
// One entry per resource: './en/' and './en/index.html' are the same document,
// so only the explicit file is listed.
const SECONDARY_ASSETS = [
  './card.html',
  './social-8k-studio.html',
  './en/index.html',
  './nl/index.html',
  './corporate-profile.html',
  './preview-founders-showcase.html',
  './demo.html',
  './assets/salim-aziza.vcf',
  './assets/raed-kaaka.vcf',
  './assets/founder-salim.png',
  './assets/founder-raed.png',
  './assets/sr-emblem-gold-luxury.jpg',
  './assets/founder-banner-salim.webp',
  './assets/founder-banner-salim.jpg',
  './assets/founder-banner-raed.webp',
  './assets/founder-banner-raed.jpg',
  './assets/nfc-card-salim-spec.png',
  './assets/nfc-card-raed-spec.png',
  './assets/qr-founder-salim.png',
  './assets/qr-founder-raed.png',
  './assets/work-1.webp',
  './assets/work-2.webp',
  './assets/work-3.webp',
  './css/demo-portal.css',
  './css/blog.css',
  './css/client-portal.css',
  './js/sr-lead-dispatcher.js',
  './js/sr-live-feed.js',
  './js/blog.js',
  './js/client-portal.js',
  './js/nfc-card.js',
  './blog.html',
  './privacy.html',
  './client-portal.html',
  './insights/erp-selection-2026.html',
  './insights/cloud-cost-30.html',
  './insights/ai-concierge-rag.html',
  './insights/ecommerce-conversion.html',
  './insights/zero-trust.html',
  './insights/brand-identity-roi.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      // Pre-cache only critical assets immediately so banners load instantly
      await cache.addAll(CRITICAL_ASSETS).catch((err) => {
        console.warn('[SW] Critical precache notice:', err);
      });
      return self.skipWaiting();
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[SW] Purging outdated cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(async () => {
      await self.clients.claim();
      // Cache secondary assets in a staggered idle queue to protect Smart TV bandwidth
      caches.open(CACHE_NAME).then((cache) => {
        SECONDARY_ASSETS.forEach((asset, idx) => {
          setTimeout(() => {
            cache.add(asset).catch(() => {});
          }, 2000 + (idx * 250));
        });
      });
    })
  );
});

// Stale-While-Revalidate (SWR) Engine for Sub-50ms Global TTFB
self.addEventListener('fetch', (event) => {
  const request = event.request;

  // Bypass non-GET requests and external API endpoints (e.g. Stripe, WhatsApp API)
  if (request.method !== 'GET') {
    return;
  }

  const url = new URL(request.url);

  // If request is external or a backend dynamic API call (.php / /api/lead), bypass cache to network
  if (url.origin !== self.location.origin || url.pathname.endsWith('.php') || url.pathname.includes('/webhooks/') || url.pathname.endsWith('/api/lead')) {
    return;
  }

  // The status page exists to say what is true right now. Serving it from the
  // stale-while-revalidate cache would show yesterday's outage on today's page,
  // so it always goes to the network and falls back to cache only when offline.
  if (url.pathname.endsWith('/status.html') || url.pathname.endsWith('/status')) {
    event.respondWith(
      fetch(request).catch(() => caches.match(request).then((cached) => cached || caches.match('./404.html')))
    );
    return;
  }

  // Stale-While-Revalidate Strategy
  event.respondWith(
    caches.open(CACHE_NAME).then(async (cache) => {
      const cachedResponse = await cache.match(request);

      // Start network fetch in background to keep cache fresh
      const networkFetchPromise = fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            cache.put(request, networkResponse.clone());
          }
          return networkResponse;
        })
        .catch((err) => {
          // Network failed (offline mode)
          return null;
        });

      // If cached response exists, return immediately for instant <20ms TTFB
      if (cachedResponse) {
        return cachedResponse;
      }

      // Otherwise wait for network response
      const networkResponse = await networkFetchPromise;
      if (networkResponse) {
        return networkResponse;
      }

      // Offline Navigation Fallback
      if (request.mode === 'navigate') {
        if (url.pathname.includes('/en/')) {
          return cache.match('./en/index.html') || cache.match('./offline.html');
        }
        if (url.pathname.includes('/nl/')) {
          return cache.match('./nl/index.html') || cache.match('./offline.html');
        }
        return cache.match('./offline.html') || cache.match('./index.html') || cache.match('./demo.html');
      }

      return new Response('Offline resource not available', { status: 503, statusText: 'Offline' });
    })
  );
});

/* --------------------------------------------------------------------------
   Web Push (requires a backend with VAPID keys to actually deliver messages;
   the handler is ready so no service-worker change is needed afterwards).
   -------------------------------------------------------------------------- */
self.addEventListener('push', (event) => {
  let payload = {};
  try {
    payload = event.data ? event.data.json() : {};
  } catch (e) {
    payload = { body: event.data ? event.data.text() : '' };
  }

  const title = payload.title || 'S&R CoreSync';
  const options = {
    body: payload.body || 'لديك تحديث جديد من S&R CoreSync.',
    icon: payload.icon || './assets/icon-192.png',
    badge: payload.badge || './assets/icon-192.png',
    dir: 'rtl',
    lang: 'ar',
    tag: payload.tag || 'sr-coresync',
    renotify: false,
    data: { url: payload.url || './index.html' }
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const target = (event.notification.data && event.notification.data.url) || './index.html';

  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if ('focus' in client) {
          client.navigate(target).catch(() => {});
          return client.focus();
        }
      }
      if (self.clients.openWindow) {
        return self.clients.openWindow(target);
      }
    })
  );
});

/* Allow the page to activate a waiting worker and to warm specific URLs. */
self.addEventListener('message', (event) => {
  const data = event.data || {};
  if (data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  if (data.type === 'CACHE_URLS' && Array.isArray(data.urls)) {
    event.waitUntil(
      caches.open(CACHE_NAME).then((cache) => {
        return Promise.all(
          data.urls.map((url) => cache.add(url).catch(() => {}))
        );
      })
    );
  }
});
