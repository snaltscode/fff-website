import os
import re

PATTERNS = [
    r'demo@',
    r'founder\.demo',
    r'Apex Global Tech',
    r'Precision Industries',
    r'Elevate Digital',
    r'googleDemoModal',
    r'handleDemoGoogleLogin',
    r'photo-1534528741775',  # Unsplash avatar
]

EXCLUDE_DIRS = {'.git', '.next', 'node_modules', '__pycache__', 'scratch'}
EXCLUDE_FILES = {'global_demo_audit.py', 'audit_demo_content.py', 'clean_db_demo_content.py'}

found_issues = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for file in files:
        if file in EXCLUDE_FILES or file.endswith('.db') or file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jfif'):
            continue
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for pattern in PATTERNS:
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                if matches:
                    found_issues.append((filepath, pattern, len(matches)))
        except Exception as e:
            pass

print("=== GLOBAL DEMO AUDIT RESULTS ===")
if not found_issues:
    print("ALL CLEAN! Zero occurrences of demo patterns found in project source files.")
else:
    for fp, pat, count in found_issues:
        print(f"  {fp}: pattern '{pat}' matched {count} time(s)")
