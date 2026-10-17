import subprocess
import hashlib
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/live_prod.html', 'rb') as f:
    live_bytes = f.read()

live_hash = hashlib.md5(live_bytes).hexdigest()
print(f"Live HTML size: {len(live_bytes)}, md5: {live_hash}")

# Get all git commits that modified public/index.html
res = subprocess.run(['git', 'log', '--format=%h %ad %s', '--date=iso', '--', 'public/index.html'], capture_output=True, text=True)
commits = [line.strip() for line in res.stdout.strip().splitlines() if line.strip()]

print(f"Found {len(commits)} commits touching public/index.html")

for line in commits:
    chash = line.split()[0]
    # get content of public/index.html at that commit
    f_res = subprocess.run(['git', 'show', f'{chash}:public/index.html'], capture_output=True)
    if f_res.returncode == 0:
        c_bytes = f_res.stdout
        c_hash = hashlib.md5(c_bytes).hexdigest()
        # compare ignoring line endings
        c_norm = c_bytes.replace(b'\r\n', b'\n')
        l_norm = live_bytes.replace(b'\r\n', b'\n')
        diff_len = abs(len(c_norm) - len(l_norm))
        is_exact = (c_norm == l_norm)
        print(f"Commit {chash} ({line[:50]}...): size={len(c_norm)} diff_from_live={diff_len} exact={is_exact}")
        if is_exact:
            print(f"*** EXACT MATCH FOUND: {line} ***")
            break
