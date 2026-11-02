#!/usr/bin/env bash
# ==============================================================================
# S&R CoreSync - Git History Purge Script (Security Remediation P0-4)
# ==============================================================================
# يعالج نتيجتَي التدقيق:
#   P2 (مرتفع): ملفات تشغيل وأسرار مودعة في تاريخ Git:
#        .env.vault, chat_history.txt, sr_agent_sessions.db, sr_rag_knowledge.db,
#        server_test*.log, srv8002*.log, sr_subagent_audit.log, uploads/
#   P3 (مرتفع): انتفاخ المستودع (~308MB pack) نتيجة تلك الملفات.
#
# ما يفعله السكربت:
#   1. النسخ الاحتياطي (bundle كامل) قبل أي تغيير.
#   2. تثبيت git-filter-repo إن لم يكن موجوداً.
#   3. إزالة المسارات المذكورة من كامل التاريخ (كل الفروع والوسوم).
#   4. إزالة الملفات من الفهرس الحالي (git rm --cached) وتحديث .gitignore.
#   5. إرشادات الدفع القسري وتدوير الأسرار.
#
# التحذير الأهم (اقرأ قبل التنفيذ):
#   ★ إزالة الملفات من التاريخ لا "تلغي" كونها سُرّبت: أي شخص استنسخ المستودع
#     أو خزّن حزمة (fork/mirror) يملك نسخة. يجب تدوير كل الأسرار الواردة في
#     .env.vault فوراً (MOLLIE, STRIPE, SMTP, SENDGRID, POSTMARK, GEMINI,
#     مفاتيح خزنة SecureVault...) بالتوازي مع هذا التنظيف.
#
# الاستخدام:
#   bash scripts/git_history_purge.sh --dry-run   # استعراض ما سيُزال دون تغيير
#   bash scripts/git_history_purge.sh             # تنفيذ فعلي (يطلب تأكيداً كتابياً)
# ==============================================================================

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# --- المسارات التي ستُمحى من كامل تاريخ المستودع ------------------------------
PURGE_PATHS=(
  ".env.vault"
  "chat_history.txt"
  "sr_agent_sessions.db"
  "sr_rag_knowledge.db"
  "server_test.log"
  "server_test_err.log"
  "srv8002.log"
  "srv8002_err.log"
  "sr_subagent_audit.log"
  "uploads"
)

MODE="run"
if [[ "${1:-}" == "--dry-run" ]]; then
  MODE="dry"
fi

echo "======================================================================"
echo " S&R CoreSync — Git History Purge (mode: $MODE)"
echo "======================================================================"

# --- 0. فحوص مسبقة -----------------------------------------------------------
command -v git >/dev/null 2>&1 || { echo "❌ git غير مثبت"; exit 1; }

if [[ -n "$(git status --porcelain)" ]]; then
  echo "❌ توجد تغييرات غير مودعة. اعمل commit أو stash أولاً (يعمل filter-repo على مستودع نظيف)."
  exit 1
fi

echo "المسارات المستهدفة من التاريخ:"
for p in "${PURGE_PATHS[@]}"; do echo "  - $p"; done
echo

if [[ "$MODE" == "dry" ]]; then
  echo "［وضع الاستعراض］الأجسام المطابقة الموجودة حالياً في التاريخ:"
  echo
  git rev-list --objects --all \
    | awk '{print $2}' \
    | sort -u \
    | while read -r obj; do
        for p in "${PURGE_PATHS[@]}"; do
          if [[ "$obj" == "$p" || "$obj" == "$p"/* ]]; then
            echo "  MATCH: $obj"
            break
          fi
        done
      done | sort -u | head -50
  echo
  echo "للتقدير الحجمي الكامل:  git filter-repo --analyze  ثم راجع .git/filter-repo/analysis"
  echo "شغّل التنفيذ الفعلي:    bash scripts/git_history_purge.sh"
  exit 0
fi

# --- 1. تأكيد كتابي صريح -----------------------------------------------------
echo "⚠️  هذا الإجراء يعيد كتابة تاريخ المستودع بالكامل ويستلزم force-push."
echo "⚠️  تأكد أن كل من يعمل معك على المستودع قد أُبلغ قبل المتابعة."
read -r -p "اكتب PURGE للتأكيد: " CONFIRM
[[ "$CONFIRM" == "PURGE" ]] || { echo "أُلغي الأمر."; exit 1; }

# --- 2. نسخة احتياطية كاملة ---------------------------------------------------
STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_BUNDLE="../SR-CoreSync_backup_before_purge_${STAMP}.bundle"
echo "1/5 إنشاء نسخة احتياطية: $BACKUP_BUNDLE"
git bundle create "$BACKUP_BUNDLE" --all
echo "   (استرجاعها لاحقاً: git clone \"$BACKUP_BUNDLE\" restored-repo)"

# --- 3. تثبيت git-filter-repo -------------------------------------------------
echo "2/5 التحقق من git-filter-repo..."
if ! command -v git-filter-repo >/dev/null 2>&1; then
  echo "   تثبيت git-filter-repo عبر pip..."
  python3 -m pip install --user git-filter-repo >/dev/null 2>&1 \
    || python3 -m pip install git-filter-repo
fi

# --- 4. المحو من التاريخ ------------------------------------------------------
echo "3/5 إعادة كتابة التاريخ (قد يستغرق دقائق على مستودع 308MB)..."
FILTER_ARGS=()
for p in "${PURGE_PATHS[@]}"; do
  FILTER_ARGS+=("--path" "$p")
done
git filter-repo --force --invert-paths "${FILTER_ARGS[@]}"

# --- 5. تنظيف الفهرس الحالي ورفع الاستثناءات ---------------------------------
echo "4/5 تحديث الفهرس الحالي (git rm --cached)..."
for p in "${PURGE_PATHS[@]}"; do
  git rm -r --cached --ignore-unmatch "$p" >/dev/null 2>&1 || true
done
if [[ -f ".env.vault" ]]; then
  echo "   تنبيه: .env.vault ما زال موجوداً على القرص — انقله خارج المستودع أو احذفه بعد تدوير الأسرار."
fi
git add .gitignore
git commit -m "security(p0-4): purge runtime artifacts & secret vault from git history" \
  --allow-empty || true

# --- 6. الدفع القسري والإرشادات النهائية -------------------------------------
echo "5/5 الخطوات اليدوية الأخيرة (نفّذها بنفسك):"
ORIGIN_URL="$(git config --get remote.origin.url 2>/dev/null || echo '(أُزيل by filter-repo)')"
cat <<EOF

  أ) أعد ربط المستودع البعيد (filter-repo يزيل remotes):
       git remote add origin ${ORIGIN_URL}

  ب) ادفع التاريخ المعاد كتابته بقوة (يتطلب صلاحية تجاوز حماية الفرع مؤقتاً):
       git push --force --all origin
       git push --force --tags origin

  ج) أبلغ كل أعضاء الفريق بإعادة الاستنساخ الكامل (وليس git pull):
       git clone ${ORIGIN_URL}
     النسخ المحلية القديمة تُبقي الملفات المحذوفة حية في كائنات Git لديها.

  د) ★ تدوير الأسرار فوراً (غير قابل للتفاوض) ★
     MOLLIE_API_KEY / STRIPE_SECRET_KEY / STRIPE_WEBHOOK_SECRET /
     SMTP_PASS / SENDGRID_API_KEY / POSTMARK_SERVER_TOKEN /
     GEMINI_API_KEY / كل ما داخل .env.vault (وأعد توليد مفتاح master الخاص بها)

  هـ) لاحقاً: اطلب من GitHub دعم إزالة الكاش المعلق (cached views / PR refs)
     إن كان المستودع عاماً وقُدّمت فيها طلبات دمج.

انتهى. حجم الحزمة الجديد: $(git count-objects -vH | grep size-pack || echo 'n/a')
EOF
