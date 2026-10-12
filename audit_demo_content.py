import os
import glob
import re
import sqlite3

EXCLUDE_DIRS = {'.git', 'node_modules', '.next', '__pycache__', '.vercel'}

def scan_files():
    results = {
        'demo_emails': [],
        'demo_phones': [],
        'fake_stats_or_marquee': [],
        'stock_images': [],
        'contact_refs': []
    }
    
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@(?!founderforfounder\.in|gmail\.com)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    example_pattern = re.compile(r'example\.com|test\.com|demo\.com|dummy', re.IGNORECASE)
    phone_pattern = re.compile(r'(\+91[\s-]?[0-9]{5}[\s-]?[0-9]{5}|\+91[\s-]?[9876][0-9]{9}|[0-9]{10})')
    unsplash_pattern = re.compile(r'https?://images\.unsplash\.com/[^\s"\'<>]+')

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not f.endswith(('.ts', '.tsx', '.js', '.html', '.css', '.py', '.sql', '.json')):
                continue
            fpath = os.path.join(root, f)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
            except Exception:
                continue

            # Check demo emails
            for match in example_pattern.finditer(content):
                start = max(0, match.start() - 30)
                end = min(len(content), match.end() + 30)
                results['demo_emails'].append((fpath, content[start:end].replace('\n', ' ')))
            
            # Check stock images
            for match in unsplash_pattern.finditer(content):
                results['stock_images'].append((fpath, match.group(0)))

            # Check 1528+ or fake counters
            if '1528' in content:
                results['fake_stats_or_marquee'].append((fpath, 'Found 1528'))
            if 'Apex Global Tech' in content:
                results['fake_stats_or_marquee'].append((fpath, 'Found Apex Global Tech'))

    return results

def scan_database():
    if not os.path.exists('f4f_community.db'):
        return {}
    conn = sqlite3.connect('f4f_community.db')
    c = conn.cursor()
    
    tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    db_results = {}
    for t in tables:
        try:
            rows = c.execute(f"SELECT * FROM {t}").fetchall()
            cols = [d[0] for d in c.description]
            db_results[t] = {'count': len(rows), 'columns': cols, 'rows': rows[:5]}
        except Exception as e:
            db_results[t] = {'error': str(e)}
    conn.close()
    return db_results

print("Scanning files...")
file_res = scan_files()
print(f"Demo emails found: {len(file_res['demo_emails'])}")
for path, snippet in file_res['demo_emails'][:15]:
    print(f"  {path}: {snippet}")

print(f"\nStock images found: {len(file_res['stock_images'])}")
for path, img in set(file_res['stock_images']):
    print(f"  {path}: {img}")

print(f"\nFake stats / marquee items found: {len(file_res['fake_stats_or_marquee'])}")
for path, item in file_res['fake_stats_or_marquee']:
    print(f"  {path}: {item}")

print("\nScanning database...")
db_res = scan_database()
for t, d in db_res.items():
    if 'error' in d:
        print(f"Table {t}: ERROR {d['error']}")
    else:
        print(f"Table {t}: {d['count']} rows")
