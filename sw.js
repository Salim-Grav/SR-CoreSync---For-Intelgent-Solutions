// S&R CoreSync Solutions - Enterprise Pre-render & Ultra-Low TTFB Service Worker
// Version: coresync-prerender-v14-srx
const CACHE_NAME = 'coresync-prerender-v14-srx';

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
  './js/enterprise-suite.min.js'
];

// 2. Secondary assets: Cached gently in an idle background queue without choking Smart TV connections.
// One entry per resource: './en/' and './en/index.html' are the same document,
// so only the explicit file is listed.
const SECONDARY_ASSETS = [
  './card.html',
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
  './js/sr-lead-dispatcher.js',
  './js/sr-live-feed.js'
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
          return cache.match('./en/index.html');
        }
        if (url.pathname.includes('/nl/')) {
          return cache.match('./nl/index.html');
        }
        return cache.match('./index.html') || cache.match('./demo.html');
      }

      return new Response('Offline resource not available', { status: 503, statusText: 'Offline' });
    })
  );
});
