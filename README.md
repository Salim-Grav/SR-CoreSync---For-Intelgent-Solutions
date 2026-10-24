# S&R CoreSync Solutions

> **Advanced Enterprise Software, Smart ERP & Intelligent AI Systems**
>
> Headquartered in the Netherlands & serving enterprises across Europe & the Middle East.

---

## 🌟 Overview

**S&R CoreSync Solutions** is a next-generation corporate platform uniting European engineering standards with high-velocity agile architecture. The platform delivers enterprise cloud systems, tailored ERP solutions, automated financial compliance, and bespoke AI applications.

---

## ☁️ Hosting Model

| Layer | Technology | Notes |
|---|---|---|
| **Web** | GitHub Pages | `sr-coresync.com` → `185.199.108-111.153` (A records). Static only. |
| **API** | Cloudflare Worker (`sr-lead-capture`) | Lead capture, webhooks, KV ledger. Source: [`workers/sr-lead-capture/`](./workers/sr-lead-capture/) |
| **Mail** | Hostinger MX + SendGrid | SPF / DKIM / DMARC / BIMI configured in `workers/config/dns-records.json` |

> **Important:** GitHub Pages does **not** execute PHP or Node and does **not** honour `.htaccess`.
> Security headers live in [`_headers`](./_headers) (the GitHub Pages native mechanism), and the
> publish workflow uploads a curated subset of the repository. Run
> `python scripts/validate_publish_set.py` to verify what would be published.

---

## 🌐 Multilingual Architecture (29 Languages)

| Language | Location | Layout |
|---|---|---|
| 🇸🇦 **العربية** | [`index.html`](./index.html) | RTL, Alexandria + Plus Jakarta Sans |
| 🇬🇧 **English** | [`en/index.html`](./en/index.html) | LTR, European enterprise terminology |
| 🇳🇱 **Dutch** | [`nl/index.html`](./nl/index.html) | LTR, Dutch fiscal & EU GDPR terminology |
| 🇩🇪 **Deutsch** | [`de/index.html`](./de/index.html) | LTR |
| 🏳️ **Kurdish (Sorani)** | [`ckb/index.html`](./ckb/index.html) | RTL |
| 🇹🇷 **Türkçe** | [`tr/index.html`](./tr/index.html) | LTR |

Plus 23 further EU languages: `bg, cs, da, el, es, et, fi, fr, ga, hr, hu, it, ku, lt, lv, mt, no, pl, pt, ro, sk, sl, sv`.

Every language folder ships a complete, standalone `index.html` + `demo.html` — there is no
runtime templating. Generation lives in `scripts/build_all_multilingual_portals.py`.

---

## 👥 Executive Leadership

- **Eng. Mohammad Salim Aziza** — Co-Founder & CTO // Lead Cloud Systems Architect
- **Mr. Mohammad Raed Kaakeh** — Co-Founder & CFO // Financial ERP Architect

---

## 🚀 Key Modules & Capabilities

1. **Cloud ERP & Enterprise Systems** — Distributed data architectures, inventory management, multi-branch supply chains.
2. **AI & Smart Automation** — RAG architecture, intelligent document extraction, automated conversational agents.
3. **Financial Accounting Tech** — Multi-currency general ledgers, Dutch VAT & EU tax compliance, direct banking APIs.
4. **Cinematic Web Experience** — Founder cinematic backgrounds, glowing golden neon signatures, GSAP/Swiper motion.
5. **Cloud Web Apps (PWA)** — 9 in-browser applications: TaxSync, FlowScan AI, CloudPOS, SecureVault, Financial AI SDK, CivicSync, HealthBridge, OmniBakery, Cloud Terminal Agent.
6. **Enterprise Suite** — Official PDF Quotation, client notes centre, GDPR bar, meeting scheduler, readiness assessment, ROI studio, licensing admin.

### Engine modules (`js/`)

| File | Role |
|---|---|
| `sr-software-apps.js` | Cloud web app & PWA runtime engine (9 applications) |
| `enterprise-suite.min.js` | Enterprise Suite v2.0 (~110 exported functions) |
| `sr-readiness.js` | AI Readiness & Digital Maturity scoring (5 axes, radar chart) |
| `sr-trust-ribbon.js` | European trust ribbon & compliance verification modal |
| `sr-tier-matrix.js` | Enterprise tier matrix & institutional calculator |
| `sr-quick-dock.js` | Sovereign floating macOS-style quick dock |
| `sr-geo-lang.js` | Browser-language detection with polite banner |
| `sr-lead-dispatcher.js` | Lead capture client (targets the Cloudflare Worker) |
| `sr-brand-inspector.js` | 4K logo inspector + Brand Kit ZIP export |
| `sr-live-feed.js` | Live trust feed — real, aggregated worker data only (never fabricated) |
| `sr-mockup-3d.min.js` | Zero-dependency WebGL 3D mockup viewer |
| `chart.umd.min.js` · `jszip.min.js` | Vendored third-party libraries |

---

## 💻 Tech Stack

- **HTML5 & CSS3** — Vanilla CSS design system, responsive flex/grid layouts.
- **JavaScript ES6+** — IIFE + UMD modules, GSAP 3, ScrollTrigger, Swiper 11, Odometer.js.
- **Backend** — PHP 8 (legacy reference), Node.js CommonJS modules, Cloudflare Workers (ES modules).
- **PWA** — `manifest.json` + `sw.js` (stale-while-revalidate service worker).
- **SVG & Motion Design** — Pure vector SVG with embedded typography and multi-stage Gaussian bloom filters.

---

## 🛡️ Security Posture

| Control | Implementation |
|---|---|
| Response headers | `_headers` (HSTS, CSP, COOP, CORP, Permissions-Policy, Referrer-Policy) |
| Publish isolation | `deploy-pages.yml` uploads a curated `_site/`; server-side material is excluded and guarded |
| Lead capture | Cloudflare Worker — input sanitisation, honeypot, rate limiting, KV ledger |
| Secrets | Never committed. Worker secrets via `wrangler secret put`. |
| Asset path integrity | `scripts/audit_language_paths.py` + `scripts/validate_publish_set.py` |

Run the full local quality gate:

```bash
node scripts/validate.js
python scripts/audit_language_paths.py
python scripts/validate_publish_set.py
```

---

## 📜 License

All rights reserved © 2026 S&R CoreSync Solutions.
