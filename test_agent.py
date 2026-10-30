import sys
from google import antigravity  # اسم الحزمة في pip هو google-antigravity، لكن مسار الاستيراد هو google.antigravity

# ضبط الترميز لدعم الطباعة باللغة العربية بسلاسة في التيرمينال
sys.stdout.reconfigure(encoding="utf-8")

print("تم استدعاء مكتبة Google Antigravity بنجاح داخل بيئة العمل المحلية!")