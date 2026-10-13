import os
import re

brain_dir = r'C:\Users\HP\.gemini\antigravity\brain'
stitch_matches = set()

for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if f.endswith('.jsonl') or f.endswith('.txt') or f.endswith('.md'):
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    found = re.findall(r'https?://stitch\.withgoogle\.com[^\s"\'<>]*', content)
                    for m in found:
                        # Clean trailing punctuation
                        m_clean = m.rstrip('.,;:)')
                        stitch_matches.add(m_clean)
            except Exception:
                pass

print("=== FOUND STITCH URLS ===")
for url in sorted(list(stitch_matches)):
    print(url)

print("\n=== SEARCHING FOR 'stitch' MENTIONS IN TRANSCRIPTS ===")
# Check for project names or titles associated with stitch
for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if f.endswith('transcript.jsonl'):
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                    for line in fp:
                        if 'stitch' in line.lower() and ('project' in line.lower() or 'dashboard' in line.lower() or 'portal' in line.lower()):
                            # print line snippet
                            for sentence in line.split('\\n'):
                                if 'stitch' in sentence.lower():
                                    print(f"[{os.path.basename(root)}] {sentence.strip()[:140]}")
            except Exception:
                pass
