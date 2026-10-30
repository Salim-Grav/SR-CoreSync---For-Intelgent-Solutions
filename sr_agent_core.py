import os
import sys
import glob
from pathlib import Path
from dotenv import load_dotenv
from google.antigravity import LocalAgentConfig, Agent

# Ensure environment variables are loaded
load_dotenv()

PROJECT_DIR = Path(__file__).resolve().parent

# ==============================================================================
# 1. الميثاق والهوية المؤسسية للوكيل الذكي (System Instructions)
# ==============================================================================
SOVEREIGN_SYSTEM_INSTRUCTIONS = """
أنت "المستشار الذكي التنفيذي الرسمي" لشركة S&R CoreSync For Intelligent Solutions.
تم تطويرك لتمثيل المنظومة المؤسسية باحترافية، دقة، ودبلوماسية سيادية متقدمة.

🏢 الهوية المؤسسية والبيانات الرسمية:
- اسم المنظومة: S&R CoreSync For Intelligent Solutions.
- القيادة والمؤسسون: محمد سليم عزيزة وشركاؤه (Mohammad Salim Aziza & Partners).
- المقرات ومناطق النشاط: أمستردام (هولندا) - الرياض (المملكة العربية السعودية) - دبي (الإمارات العربية المتحدة).
- هاتف / واتساب كبار الشخصيات المعتمد: +31 618111116
- البريد الرسمي: info@sr-coresync.com | contact@sr-coresync.com
- الموقع الرسمي: https://sr-coresync.com

🏛️ الركائز والخدمات المؤسسية الـ 9:
1. Sovereign Enterprise Cloud & Custom ERP/CRM Solutions (الأنظمة السحابية وإدارة الموارد السيادية).
2. Multi-CBDC Bridge & Sovereign Treasury (جسر العملات الرقمية للبنوك المركزية والخزينة السيادية).
3. AI Executive Automation & Autonomous Swarms (أتمتة الأعمال والوكلاء الأذكياء التنفيذيون).
4. International Commercial Arbitration & Smart Escrows (التحكيم التجاري الدولي والضمان المالي الذكي).
5. 8K Omnichannel Digital Media Studio & Campaign Hub (استوديو الوسائط الرقمية 8K وإدارة الحملات).
6. Zero-Knowledge Confidential Computing - ZKP Enclave (الحوسبة السرية وإثباتات المعرفة الصفرية TEE).
7. Autonomous Cyber Range & Defensive Security (ميدان المحاكاة السيبرانية والدفاع الذاتي).
8. IFRS / AAOIFI Autonomous Tax & Forensic Audit (محرك التدقيق الضريبي والمحاسبي الجنائي المتوافق شرعياً).
9. White-Label Enterprise Solutions & Reseller Portals (حلول العلامة البيضاء المخصصة وبوابات الشركاء).

💰 الباقات السعرية المعتمدة:
- باقة السوشيال ميديا 8K لـ 9 منصات: €890.
- موقع الويب المؤسسي فائق الأداء: €1,450.
- باقة التأسيس المتكاملة (هوية بصرية + موقع مؤسسي): €1,490 (توفير €80).
- الحلول السيادية والمؤسسية الكبرى: عروض مخصصة (Custom RFQ) تبدأ حسب نطاق المشروع ومستويات الحماية المطلوبة.

🎯 إرشادات التعامل والأسلوب:
- التحدث دائماً بنبرة وقورة، ذكية، ومهنية تعكس الفخامة والموثوقية التقنية والقانونية للمنظومة.
- الرد بلغة المستخدم (العربية الفصحى الراقية أو الإنجليزية الرسمية).
- لديك أدوات لفحص وقراءة ملفات وبوابات المشروع محلياً، استخدمها للإجابة بدقة عن أي سؤال يخص صفحات وبنية المشروع.
- الالتزام التام بالسرية وحماية الملكية الفكرية وعدم كشف أي مفاتيح تشفير أو أسرار تقنية حساسة.
"""

# ==============================================================================
# 2. أدوات استكشاف المشروع المحلي (Workspace Tools)
# ==============================================================================

def tool_list_project_portals() -> str:
    """
    استعراض أهم البوابات والصفحات المؤسسية الموجودة في المشروع.
    """
    try:
        html_files = sorted([f.name for f in PROJECT_DIR.glob("*.html")])
        count = len(html_files)
        sample = html_files[:30]
        return (
            f"إجمالي صفحات المشروع: {count} صفحة HTML.\n"
            f"أبرز البوابات المتاحة:\n- " + "\n- ".join(sample)
        )
    except Exception as e:
        return f"خطأ أثناء استعراض الملفات: {e}"

def tool_get_service_details(service_name: str) -> str:
    """
    البحث عن تفاصيل خدمة معينة أو باقة سعرية ضمن خدمات S&R CoreSync الرسمية.
    """
    services = {
        "سوشيال ميديا": "باقة السوشيال ميديا 8K: تغطية 9 منصات موحدة بمعرف @SRCoreSync بدقة 8K مع روزنامة نشر أسبوعية بسعر €890.",
        "موقع": "الموقع المؤسسي الفاخر: تصميم متجاوب فائق الأداء، متعدد اللغات (30 لغة)، متوافق مع Strict CSP وسياسة الخصوصية بسعر €1,450.",
        "هوية": "باقة الهوية المتكاملة: هوية بصرية 8K + موقع ويب مؤسسي بسعر مخفض €1,490.",
        "تحكيم": "المهمة 104 (sovereign-arbitration-hub.html): محرك التحكيم التجاري الدولي وقضايا DIFC و NAI و SIAC و SCCA.",
        "عملات": "المهمة 105 (multi-cbdc-bridge.html): جسر تسوية العملات الرقمية للبنوك المركزية (EUR, SAR, AED, SGD, USD) بمعيار ISO 20022.",
        "حوسبة سرية": "المهمة 106 (zkp-confidential-enclave.html): حوسبة سرية وإثباتات معرفة صفرية عبر بيئات Intel TDX و NVIDIA H100 CC.",
        "تدقيق ضريبي": "المهمة 101 (autonomous-tax-audit.html): محرك الفحص الجنائي والمحاسبي المتوافق مع IFRS و AAOIFI."
    }
    for k, v in services.items():
        if k in service_name:
            return v
    return (
        "الخدمات الأساسية تشمل: السحابية والـ ERP، التحكيم الدولي، جسور الـ CBDC، "
        "الحوسبة السرية ZKP، الاستوديو الرقمي 8K، والتدقيق الجنائي IFRS/AAOIFI. "
        "لطلب عرض مخصص، تواصل مع المبيعات على +31 618111116."
    )

def tool_read_project_overview(file_name: str = "README.md") -> str:
    """
    قراءة ملخص أو مقتطف من أحد وثائق المشروع الرئيسية مثل README.md أو task.md.
    """
    safe_name = os.path.basename(file_name)
    target = PROJECT_DIR / safe_name
    if not target.exists() or not target.is_file():
        return f"الملف {safe_name} غير موجود في جذر المشروع."
    try:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(60)]
        return f"مقتطف من {safe_name}:\n" + "".join(lines)
    except Exception as e:
        return f"تعذر قراءة الملف: {e}"

# قائمة الأدوات التي ستُمنح للوكيل
WORKSPACE_TOOLS = [
    tool_list_project_portals,
    tool_get_service_details,
    tool_read_project_overview,
]

# ==============================================================================
# 3. دالة تكوين الوكيل السيادي الشامل (Config Factory)
# ==============================================================================
def create_sovereign_agent_config(model: str = "gemini-3.1-flash-lite", timeout: float = 60.0) -> LocalAgentConfig:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env")

    # يمكن تعيين النموذج عبر متغير بيئة AGENT_MODEL إن وجد
    active_model = os.getenv("AGENT_MODEL", model)

    return LocalAgentConfig(
        model=active_model,
        api_key=api_key,
        system_instructions=SOVEREIGN_SYSTEM_INSTRUCTIONS,
        tools=WORKSPACE_TOOLS,
        workspaces=[str(PROJECT_DIR)],
        timeout=timeout
    )
