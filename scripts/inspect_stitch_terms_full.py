with open(r'stitch_imported_screens_v2\html\01_Terms___Conditions___f4f_4a4c7e2e.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
head = re.search(r'<head[^>]*>(.*?)</head>', text, re.DOTALL)
if head:
    # check styles or scripts
    styles = re.findall(r'<style[^>]*>(.*?)</style>', head.group(1), re.DOTALL)
    print("Styles in head:", len(styles))
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', head.group(1), re.DOTALL)
    print("Scripts in head:", len(scripts))
    # print any tailwind cdn or config
    for s in re.findall(r'<script[^>]+src=\"([^\"]+)\"', head.group(1)):
        print("Script src:", s)

body = re.search(r'<body[^>]*>(.*?)</body>', text, re.DOTALL)
if body:
    print("Body length:", len(body.group(1)))
