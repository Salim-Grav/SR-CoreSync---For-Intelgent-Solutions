import subprocess
import os
import shutil

SNAPSHOT_PATH = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\live_terminal_snapshot.jpg'
TEMP_PROFILE = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\chrome_snapshot_profile'

def capture(url=None):
    if not url:
        url = 'file:///' + os.path.abspath('voice-dictate.html').replace('\\', '/')
    
    os.makedirs(TEMP_PROFILE, exist_ok=True)
    temp_shot = os.path.abspath('temp_screenshot_capture.png')
    cmd = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={TEMP_PROFILE}',
        '--virtual-time-budget=2000',
        f'--screenshot={temp_shot}',
        '--window-size=1280,800',
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if os.path.exists(temp_shot):
        shutil.copyfile(temp_shot, SNAPSHOT_PATH)
        os.remove(temp_shot)
        print(f'SUCCESS: Live screenshot saved to {SNAPSHOT_PATH} ({os.path.getsize(SNAPSHOT_PATH)} bytes)')
        return True
    else:
        print('FAILED to capture screenshot:', res.stderr)
        return False

if __name__ == '__main__':
    capture()

