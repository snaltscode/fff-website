import subprocess
import os
import time

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
run_id = int(time.time())
temp_dir = os.path.join(os.environ.get("TEMP", r"C:\Temp"), f"chrome_headless_profile_{run_id}")

desktop_png = r"d:\Founder for Founder website\screenshot_desktop.png"
mobile_png = r"d:\Founder for Founder website\screenshot_mobile.png"

extra_flags = [
    "--headless=new",
    "--disable-gpu",
    "--disable-cache",
    "--disk-cache-size=0",
    f"--user-data-dir={temp_dir}"
]

# 1. Desktop screenshot (1280x2000)
cmd_desktop = [
    chrome_path,
    *extra_flags,
    "--window-size=1280,2000",
    f"--screenshot={desktop_png}",
    "http://localhost:3009/"
]

print("Capturing desktop screenshot...")
res1 = subprocess.run(cmd_desktop, capture_output=True, text=True)
print("Desktop exit:", res1.returncode)
print("Desktop exists:", os.path.exists(desktop_png))

# 2. Mobile screenshot (390x1600)
cmd_mobile = [
    chrome_path,
    *extra_flags,
    "--window-size=390,1600",
    f"--screenshot={mobile_png}",
    "http://localhost:3009/"
]

print("Capturing mobile screenshot...")
res2 = subprocess.run(cmd_mobile, capture_output=True, text=True)
print("Mobile exit:", res2.returncode)
print("Mobile exists:", os.path.exists(mobile_png))
