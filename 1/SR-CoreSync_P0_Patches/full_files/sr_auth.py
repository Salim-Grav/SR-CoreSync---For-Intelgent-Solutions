"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================

==============================================================================
طبقة المصادقة والتحكم بالوصول والحد من المعدل (Security Remediation P0-1/P0-2)
==============================================================================
تعالج هذه الوحدة النتائج الحرجة التالية من التدقيق الأمني:
  - A1 (حرج): جميع نقاط النهاية كانت مكشوفة دون أي مصادقة أو تفويض.
  - A4 (مرتفع): CORS مفتوح على "*" مع allow_credentials=True.
  - A8 (متوسط): جلسات المحادثة بلا مالك؛ أي طرف يقرأ/يحذف جلسات الغير.

نموذج الأمان المعتمد:
  - مفاتيح API (X-API-Key أو Authorization: Bearer أو ?api_key= للـ SSE/المتصفح).
  - دوران: admin (كل الصلاحيات) و client (المحادثة والقراءة فقط).
  - الإغلاق الافتراضي (Fail-Closed): إن لم تُضبط أي مفاتيح تُرفض الطلبات المحمية
    بخطأ 503 ولا يعمل الخادم بشكل مفتوح أبداً.
  - مفتاح التطوير المحلي: CORESYNC_AUTH_DISABLED=1 (للاختبار على 127.0.0.1 فقط).
  - حد من المعدل (Sliding Window) في الذاكرة: افتراضياً 120 طلب/دقيقة، و10/دقيقة
    لمسارات استهلاك Gemini. ملاحظة: الحدّ هنا لكل عملية (worker)؛ للتوزيع المتعدد
    استخدم مخزناً مركزياً (Redis) — انظر دليل التطبيق.

المتغيرات البيئية:
  CORESYNC_API_KEYS        قائمة مفاتيح نصية مفصولة بفواصل بالصيغة: الاسم:المفتاح:الدور
                           مثال: ops-console:sk_live_xxx:admin,site-widget:sk_web_yyy:client
  CORESYNC_AUTH_FILE       مسار ملف JSON بالمفاتيح المُهشّرة (افتراضياً auth_keys.json)
                           الصيغة: {"keys":[{"name":"...","key_sha256":"...","role":"admin"}]}
  CORESYNC_AUTH_DISABLED   "1" لتعطيل المصادقة في التطوير المحلي فقط (يُسجّل تحذير)
  CORESYNC_RATE_LIMIT      الحد العام، مثال "120/min" (افتراضي 120/min)
  CORESYNC_CHAT_RATE_LIMIT حد مسارات المحادثة المكلفة، مثال "10/min" (افتراضي 10/min)
"""

import os
import sys
import time
import json
import hmac
import hashlib
import logging
from pathlib import Path
from collections import defaultdict, deque
from typing import Optional, Dict, List, Tuple, Callable, Awaitable

logger = logging.getLogger("sr_auth")

# ضبط الترميز لدعم العربية في الطرفية
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECT_DIR = Path(__file__).resolve().parent

# ==============================================================================
# 1. الهويات والأدوار (Principals & Roles)
# ==============================================================================
ROLE_ADMIN = "admin"
ROLE_CLIENT = "client"
_VALID_ROLES = {ROLE_ADMIN, ROLE_CLIENT}


class Principal:
    """هوية مستدعي مُصادق عليها (مفتاح API مرتبط باسم ودور)"""

    __slots__ = ("name", "role", "source")

    def __init__(self, name: str, role: str, source: str = "api_key"):
        self.name = name
        self.role = role if role in _VALID_ROLES else ROLE_CLIENT
        self.source = source

    @property
    def is_admin(self) -> bool:
        return self.role == ROLE_ADMIN

    def as_dict(self) -> Dict[str, str]:
        return {"name": self.name, "role": self.role, "source": self.source}


# ==============================================================================
# 2. مخزن المفاتيح (Key Store) — تُخزَّن المفاتيح مهشّرة SHA-256 فقط
# ==============================================================================
class SovereignKeyStore:
    """تحميل مفاتيح API من ملف JSON مهشّر و/أو متغير بيئة، والمصادقة بمقارنة زمن-ثابت"""

    def __init__(self):
        self._entries: Dict[str, Tuple[str, str]] = {}  # key_sha256 -> (name, role)
        self.auth_enabled: bool = False
        self._load()

    @staticmethod
    def hash_key(plain: str) -> str:
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()

    def _load(self) -> None:
        # (أ) ملف JSON بالمفاتيح المُهشّرة مسبقاً (الأسلوب الموصى به للإنتاج)
        auth_file = Path(os.getenv("CORESYNC_AUTH_FILE", str(PROJECT_DIR / "auth_keys.json")))
        try:
            if auth_file.is_file():
                data = json.loads(auth_file.read_text(encoding="utf-8"))
                count = 0
                for entry in data.get("keys", []):
                    digest = str(entry.get("key_sha256", "")).strip().lower()
                    name = str(entry.get("name", "unnamed")).strip()
                    role = str(entry.get("role", ROLE_CLIENT)).strip()
                    if len(digest) == 64:
                        self._entries[digest] = (name, role)
                        count += 1
                if count:
                    logger.info("تم تحميل %d مفتاح API مهشّر من %s", count, auth_file)
        except Exception as exc:  # ملف تالف لا يجب أن يفتح الخادم
            logger.error("تعذر تحميل ملف مفاتيح المصادقة %s: %s", auth_file, exc)

        # (ب) متغير بيئة بصيغة الاسم:المفتاح_النصي:الدور (يُهشَّر فور التحميل)
        env_keys = os.getenv("CORESYNC_API_KEYS", "").strip()
        if env_keys:
            count = 0
            for spec in env_keys.split(","):
                parts = [p.strip() for p in spec.split(":") if p.strip()]
                if len(parts) < 2:
                    continue
                name = parts[0]
                plain = parts[1]
                role = parts[2] if len(parts) >= 3 else ROLE_CLIENT
                self._entries[self.hash_key(plain)] = (name, role)
                count += 1
            if count:
                logger.info("تم تحميل %d مفتاح API من متغير البيئة CORESYNC_API_KEYS", count)

        self.auth_enabled = bool(self._entries)

    def authenticate(self, presented_key: str) -> Optional[Principal]:
        """مصادقة مفتاح مقدَّم بمقارنة زمن-ثابت؛ لا يكشف أي معلومة عند الفشل"""
        if not presented_key:
            return None
        digest = self.hash_key(presented_key)
        for candidate, (name, role) in self._entries.items():
            if hmac.compare_digest(candidate, digest):
                return Principal(name=name, role=role)
        return None

    def extract_key(self, raw_headers, query_string: bytes) -> Optional[str]:
        """استخراج المفتاح من الترويسات أو الاستعلام (الاستعلام لقنوات SSE/EventSource)"""
        # ترويسات ASGI قائمة أزواج (bytes, bytes) وليست قاموساً
        headers = dict(raw_headers or [])
        api_key = headers.get(b"x-api-key")
        if api_key:
            return api_key.decode("latin-1").strip()
        authorization = headers.get(b"authorization")
        if authorization:
            value = authorization.decode("latin-1").strip()
            if value.lower().startswith("bearer "):
                return value[7:].strip()
        if query_string:
            from urllib.parse import parse_qs
            try:
                params = parse_qs(query_string.decode("latin-1"))
                values = params.get("api_key")
                if values and values[0].strip():
                    return values[0].strip()
            except Exception:
                pass
        return None


# ==============================================================================
# 3. وسيلة المصادقة السيادية (Pure-ASGI Middleware) — إغلاق افتراضي
# ==============================================================================
# مسارات عامة لا تتطلب مصادقة (فحوص الجاهزية للوِب المحمل)
PUBLIC_PATHS = {"/", "/health"}

# مسارات الإدارة الحصرية (تتطلب دور admin): (الطريقة، المسار، مطابقة_بالبادئة؟)
# كل ما عداها يتطلب مصادقة صالحة فقط (admin أو client)
ADMIN_RULES: Tuple[Tuple[str, str, bool], ...] = (
    ("DELETE", "/api/sessions/", True),   # حذف الجلسات (A1: كان مكشوفاً)
    ("POST", "/api/upload", False),       # حقن المعرفة في RAG (A2: قناة تسميم)
    ("POST", "/api/rag/reindex", False),  # إعادة الفهرسة الكاملة
    ("POST", "/api/subagent/run-audit", False),
    ("POST", "/api/events/publish", False),  # بث أحداث مزيّفة للوحة القيادة (A7)
    ("POST", "/api/appeals/lodge", False),   # قيد استئنافات وتجميد أصول (Mission 112)
    ("GET", "/api/appeals/list", False),
    ("GET", "/api/sessions", False),      # سرد كل الجلسات (مطابقة تامة، لا تشمل سجل جلسة بعينها)
)


def _dev_principal() -> Principal:
    return Principal(name="local-dev", role=ROLE_ADMIN, source="auth_disabled")


class SovereignAuthMiddleware:
    """
    مصادقة جميع الطلبات المحمية على مستوى ASGI، مع الإغلاق الافتراضي:
      - 401 لمفتاح غائب/خاطئ.
      - 403 لمفتاح صحيح على مسار إداري بدور client.
      - 503 إن لم تُهيّأ أي مفاتيح على الإطلاق (فشل التهيئة، لا فتحٌ للخادم).
    الهوية المُصادقة تُخزَّن في scope["state"]["principal"] لاستخدامها في
    نقاط النهاية (التحقق من ملكية الجلسات عبر get_principal).
    """

    def __init__(self, app, key_store: Optional[SovereignKeyStore] = None):
        self.app = app
        self.key_store = key_store or SovereignKeyStore()
        if not self.key_store.auth_enabled and os.getenv("CORESYNC_AUTH_DISABLED") != "1":
            logger.warning(
                "⚠️ لم تُضبط أي مفاتيح API (CORESYNC_API_KEYS أو CORESYNC_AUTH_FILE). "
                "سيرفض الخادم كل الطلبات المحمية برمز 503 حتى تُضبط المفاتيح. "
                "للتطوير المحلي فقط: CORESYNC_AUTH_DISABLED=1"
            )

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path = scope.get("path", "")
        method = scope.get("method", "GET").upper()

        # طلبات CORS المسبقة (OPTIONS) تُمرَّر لوسيلة CORS الخارجية دون مصادقة
        if method == "OPTIONS":
            return await self.app(scope, receive, send)

        # مسارات الصحة العامة فقط
        if path in PUBLIC_PATHS:
            return await self.app(scope, receive, send)

        # وضع التطوير المحلي الصريح (لن يعمل الخادم الإنتاجي هكذا)
        if not self.key_store.auth_enabled:
            if os.getenv("CORESYNC_AUTH_DISABLED") == "1":
                scope.setdefault("state", {})["principal"] = _dev_principal()
                return await self.app(scope, receive, send)
            await self._send_json_error(send, 503, {
                "status": "auth_not_configured",
                "detail": "المصادقة غير مهيأة: اضبط CORESYNC_API_KEYS أو CORESYNC_AUTH_FILE قبل التشغيل."
            })
            return

        principal = self.key_store.authenticate(
            self.key_store.extract_key(scope.get("headers") or [], scope.get("query_string", b""))
        )  # type: ignore[arg-type]
        if principal is None:
            await self._send_json_error(send, 401, {
                "status": "unauthorized",
                "detail": "مفتاح API مفقود أو غير صالح. مرّره عبر الترويسة X-API-Key أو Authorization: Bearer."
            })
            return

        # فرض الدور على مسارات الإدارة الحصرية
        for required_method, rule_path, is_prefix in ADMIN_RULES:
            if method != required_method:
                continue
            if path.startswith(rule_path) if is_prefix else (path == rule_path):
                if not principal.is_admin:
                    await self._send_json_error(send, 403, {
                        "status": "forbidden",
                        "detail": "هذه العملية تتطلب مفتاحاً بدور admin."
                    })
                    return
                break

        scope.setdefault("state", {})["principal"] = principal
        return await self.app(scope, receive, send)

    async def _send_json_error(self, send, status: int, body: dict) -> None:
        import json as _json
        payload = _json.dumps(body, ensure_ascii=False).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json; charset=utf-8"),
                (b"content-length", str(len(payload)).encode("latin-1")),
                (b"www-authenticate", b"ApiKey"),
            ],
        })
        await send({"type": "http.response.body", "body": payload})


# ==============================================================================
# 4. وسيلة الحد من المعدل (Sliding Window, في الذاكرة — لكل عملية worker)
# ==============================================================================
def _parse_rate(spec: str, default: Tuple[int, int]) -> Tuple[int, int]:
    """تحويل صيغة مثل '120/min' إلى (الحد، النافذة_بالثواني)"""
    try:
        value, _, unit = spec.strip().partition("/")
        limit = int(value)
        window = {"s": 1, "sec": 1, "m": 60, "min": 60, "h": 3600, "hour": 3600}.get(
            unit.strip().lower() or "min", 60
        )
        return limit, window
    except Exception:
        return default


class SovereignRateLimitMiddleware:
    """
    حد من المعدل بنافذة منزلقة مفصولة إلى مجموعتين:
      - المجموعة العامة: كل المسارات (افتراضياً 120 طلب/دقيقة).
      - مجموعة المحادثة المكلفة: مسارات استهلاك Gemini (افتراضياً 10 طلبات/دقيقة).
    المفتاح: اسم الهوية المُصادقة إن وُجدت وإلا عنوان IP.
    ملاحظة صادقة: العدّاد في الذاكرة المحلية لكل عملية uvicorn؛ عند التشغيل
    بعمليات متعددة استخدم حداً مركزياً (Redis/الوكيل العكسي) — موثق في الدليل.
    """

    CHAT_PREFIXES = ("/api/chat", "/api/ai-concierge")

    def __init__(self, app):
        self.app = app
        general = _parse_rate(os.getenv("CORESYNC_RATE_LIMIT", "120/min"), (120, 60))
        chat = _parse_rate(os.getenv("CORESYNC_CHAT_RATE_LIMIT", "10/min"), (10, 60))
        self.general_limit, self.general_window = general
        self.chat_limit, self.chat_window = chat
        self._hits: Dict[Tuple[str, str, int], deque] = defaultdict(deque)

    def _client_ip(self, scope) -> str:
        client = scope.get("client")
        return client[0] if client else "unknown"

    def _identity(self, scope) -> str:
        principal = (scope.get("state") or {}).get("principal")
        if principal is not None:
            return f"key:{principal.name}"
        return f"ip:{self._client_ip(scope)}"

    def _allow(self, bucket: Tuple[str, int], limit: int, window: int) -> Tuple[bool, int]:
        now = time.monotonic()
        hits = self._hits[bucket]
        while hits and hits[0] <= now - window:
            hits.popleft()
        if len(hits) >= limit:
            retry_after = int(window - (now - hits[0])) + 1
            return False, max(retry_after, 1)
        hits.append(now)
        return True, 0

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope.get("method", "GET").upper() == "OPTIONS":
            return await self.app(scope, receive, send)

        path = scope.get("path", "")
        identity = self._identity(scope)

        if path.startswith(self.CHAT_PREFIXES):
            allowed, retry_after = self._allow(("chat", identity, self.chat_window), self.chat_limit, self.chat_window)
            if not allowed:
                await self._send_rate_limited(send, retry_after, "تجاوزت حد معدل المحادثة المسموح؛ حاول لاحقاً.")
                return

        allowed, retry_after = self._allow(("general", identity, self.general_window), self.general_limit, self.general_window)
        if not allowed:
            await self._send_rate_limited(send, retry_after, "تجاوزت الحد العام لمعدل الطلبات؛ حاول لاحقاً.")
            return

        return await self.app(scope, receive, send)

    async def _send_rate_limited(self, send, retry_after: int, detail: str) -> None:
        import json as _json
        payload = _json.dumps({"status": "rate_limited", "detail": detail}, ensure_ascii=False).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": 429,
            "headers": [
                (b"content-type", b"application/json; charset=utf-8"),
                (b"content-length", str(len(payload)).encode("latin-1")),
                (b"retry-after", str(retry_after).encode("latin-1")),
            ],
        })
        await send({"type": "http.response.body", "body": payload})


# ==============================================================================
# 5. تبعيات FastAPI للوصول إلى الهوية وملكية الجلسات
# ==============================================================================
def get_principal(request):
    """تبعية FastAPI: استرجاع الهوية المُصادقة التي ضبطتها وسيلة المصادقة"""
    principal = getattr(request.state, "principal", None)
    if principal is None:
        # وصلنا إلى نقطة نهاية محمية دون وسيلة مصادقة (وضع التطوير المحلي)
        principal = _dev_principal()
    return principal


def principal_label(principal) -> str:
    """التسمية الآمنة للسجلات (بدون أي أسرار)"""
    return f"{principal.name}({principal.role})"
