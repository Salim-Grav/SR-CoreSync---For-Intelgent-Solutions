with open('js/smart-business-advisor.js', 'r', encoding='utf-8') as f:
    text = f.read()

bad_block = """            var summary = encodeURIComponent(
                "🏛️ استشارة مالية وضريبية ذكية معتمدة (S&R CoreSync):
" +
                "🏢 القطاع: " + a.sector + "
" +
                "⚖️ الكيان: " + a.entity + "
" +
                "💶 المبيعات السنوية: €" + Math.round(a.revenue).toLocaleString('nl-NL') + "
" +
                "📈 صافي الربح التشغيلي: €" + Math.round(a.operatingProfit).toLocaleString('nl-NL') + "
" +
                "💰 الوفورات الضريبية المقدرة: €" + Math.round(a.taxSavings).toLocaleString('nl-NL') + "
" +
                "🛡️ مؤشر الامتثال والأمان: " + a.auditScore + "%
" +
                "نرجو جدولة مراجعة الملف مع المحاسب القانوني المعتمد (الأستاذ رودين)."
            );"""

good_block = """            var lines = [
                '🏛️ استشارة مالية وضريبية ذكية معتمدة (S&R CoreSync):',
                '🏢 القطاع: ' + a.sector,
                '⚖️ الكيان: ' + a.entity,
                '💶 المبيعات السنوية: €' + Math.round(a.revenue).toLocaleString('nl-NL'),
                '📈 صافي الربح التشغيلي: €' + Math.round(a.operatingProfit).toLocaleString('nl-NL'),
                '💰 الوفورات الضريبية المقدرة: €' + Math.round(a.taxSavings).toLocaleString('nl-NL'),
                '🛡️ مؤشر الامتثال والأمان: ' + a.auditScore + '%',
                'نرجو جدولة مراجعة الملف مع المحاسب القانوني المعتمد (الأستاذ رودين).'
            ];
            var summary = encodeURIComponent(lines.join('\\n'));"""

text = text.replace(bad_block, good_block)

# Also check any other string with newlines in recs
bad_desc = "desc: `بما أن الأرباح التشغيلية بلغت ${formatCurrency(operatingProfit)}، يُنصح بالتحول الاستراتيجي إلى شركة BV لعزل الذمة المالية الشخصية وتفادي الشريحة الضريبية العليا Box 1 (49.5%).`"
# That's a template literal which is fine in ES6.

with open('js/smart-business-advisor.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Cleaned up string syntax.')
