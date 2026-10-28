"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

import os

desktop = r'C:\Users\msali\OneDrive\Desktop'
project_dir = r'd:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project'

pull_content = f'''@echo off
chcp 65001 > nul
title سحب أحدث التحديثات من GitHub
color 0a
cd /d "{project_dir}"
echo ======================================================================
echo    S^&R CoreSync - جاري سحب أحدث التحديثات من GitHub (Pull)...
echo ======================================================================
echo.
git pull origin main
echo.
echo ======================================================================
echo ✅ تم سحب كافة التحديثات بنجاح! المحرر جاهز للعمل.
echo ======================================================================
echo.
pause
'''

push_content = f'''@echo off
chcp 65001 > nul
title حفظ ودفع كافة التحديثات إلى GitHub
color 0b
cd /d "{project_dir}"
echo ======================================================================
echo    S^&R CoreSync - جاري حفظ ودفع كافة التحديثات إلى GitHub (Push)...
echo ======================================================================
echo.
git add -A
git commit -m "feat: sync updates completed"
git push origin main
echo.
echo ======================================================================
echo ✅ تم رفع وحفظ كافة التحديثات إلى GitHub بنجاح!
echo ======================================================================
echo.
pause
'''

with open(os.path.join(desktop, 'سحب_التحديثات_من_GitHub.bat'), 'w', encoding='utf-8') as f:
    f.write(pull_content)

with open(os.path.join(desktop, 'حفظ_ودفع_التحديثات_إلى_GitHub.bat'), 'w', encoding='utf-8') as f:
    f.write(push_content)

# Also ensure main interactive script is copied to desktop
interactive_src = os.path.join(project_dir, 'مزامنة_المشروع_مع_GitHub.bat')
interactive_dst = os.path.join(desktop, 'مزامنة_المشروع_مع_GitHub.bat')
if os.path.exists(interactive_src):
    with open(interactive_src, 'r', encoding='utf-8') as src:
        content = src.read()
    with open(interactive_dst, 'w', encoding='utf-8') as dst:
        dst.write(content)

print('SUCCESS: All Desktop synchronization tools created.')
