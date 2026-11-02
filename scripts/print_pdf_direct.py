import subprocess
import os

pdf_path = os.path.abspath('CLGID_The_Hague_Modernization_Proposal_2026.pdf')
html_path = 'file:///' + os.path.abspath('clgid-prototype.html').replace('\\', '/')
temp_user_dir = os.path.abspath('temp_chrome_print_dir')

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--no-pdf-header-footer',
    f'--user-data-dir={temp_user_dir}',
    f'--print-to-pdf={pdf_path}',
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)

if os.path.exists(pdf_path):
    print("SUCCESS: PDF created! Size:", os.path.getsize(pdf_path), "bytes")
else:
    print("FAILED: PDF not found")
