import os
import re
import json
import urllib.request

output_dir = 'stitch_imported_screens'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.join(output_dir, 'html'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'screenshots'), exist_ok=True)

manifest_file = r'C:\Users\HP\.gemini\antigravity\brain\09dd8d13-9950-4be7-8d17-dc3c64288199\.system_generated\steps\6951\output.txt'

with open(manifest_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])
print(f"Importing {len(screens)} screens from Google Stitch...")

catalog = []

for idx, s in enumerate(screens):
    screen_id = s.get('name', '').split('/')[-1]
    title = s.get('title', f'Screen_{idx+1}')
    clean_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', title).strip('_')
    
    html_info = s.get('htmlCode', {})
    screenshot_info = s.get('screenshot', {})
    
    html_url = html_info.get('downloadUrl')
    screenshot_url = screenshot_info.get('downloadUrl')
    
    html_path = None
    if html_url:
        html_filename = f"{idx+1:02d}_{clean_title}_{screen_id[:8]}.html"
        html_filepath = os.path.join(output_dir, 'html', html_filename)
        try:
            req = urllib.request.Request(html_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                with open(html_filepath, 'w', encoding='utf-8') as out:
                    out.write(content)
                html_path = html_filepath
                print(f"[{idx+1}/{len(screens)}] HTML saved: {html_filename} ({len(content)} bytes)")
        except Exception as e:
            print(f"[{idx+1}/{len(screens)}] HTML download failed for {title}: {e}")
            
    screenshot_path = None
    if screenshot_url:
        img_filename = f"{idx+1:02d}_{clean_title}_{screen_id[:8]}.png"
        img_filepath = os.path.join(output_dir, 'screenshots', img_filename)
        try:
            req = urllib.request.Request(screenshot_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                img_data = resp.read()
                with open(img_filepath, 'wb') as out:
                    out.write(img_data)
                screenshot_path = img_filepath
                print(f"[{idx+1}/{len(screens)}] Screenshot saved: {img_filename} ({len(img_data)} bytes)")
        except Exception as e:
            print(f"[{idx+1}/{len(screens)}] Screenshot download failed for {title}: {e}")

    catalog.append({
        "index": idx + 1,
        "title": title,
        "screenId": screen_id,
        "resourceName": s.get('name'),
        "htmlPath": html_path,
        "screenshotPath": screenshot_path,
        "width": s.get('width'),
        "height": s.get('height'),
        "deviceType": s.get('deviceType')
    })

catalog_path = os.path.join(output_dir, 'catalog.json')
with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2)

print(f"\nAll screens successfully cataloged in {catalog_path}!")
