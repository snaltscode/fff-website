import glob

files = glob.glob('public/*.html')
all_ok = True
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    has_bg = 'id="static-textured-bg"' in c
    has_trans = 'background-color: transparent !important' in c
    print(f'{f}: bg={has_bg}, transparent_body={has_trans}')
    if not (has_bg and has_trans):
        all_ok = False

print('ALL HTML PAGES CONFIGURED WITH STATIC TEXTURED BG:', all_ok)
