css_rule = '''
/* Executive Guild Responsive Headline Scaling */
@media (max-width: 640px) {
  .text-headline-hero {
    font-size: 2.15rem !important;
    line-height: 1.18 !important;
    word-break: break-word;
  }
  .text-headline-lg {
    font-size: 1.65rem !important;
    line-height: 1.25 !important;
    word-break: break-word;
  }
  .text-headline-md {
    font-size: 1.35rem !important;
    line-height: 1.3 !important;
    word-break: break-word;
  }
}
'''

for path in ['public/css/styles.css', 'src/app/globals.css']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'Executive Guild Responsive Headline Scaling' not in content:
        content = content.rstrip() + '\n' + css_rule
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Appended responsive headline scaling to {path}")
    else:
        print(f"Already present in {path}")
