import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

dl_dir = r'C:\Users\HP\Downloads\stitch_founder_for_founder_platform'
for root, dirs, files in os.walk(dl_dir):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                c = fp.read()
            imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', c)
            bgs = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', c)
            if imgs or bgs:
                print(os.path.relpath(p, dl_dir))
                for src in set(imgs + bgs):
                    print('   ', src)
