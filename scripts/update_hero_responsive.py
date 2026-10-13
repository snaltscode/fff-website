with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'class="font-headline-hero text-headline-hero text-primary tracking-tight font-bold leading-tight" id="heroTitle"'
replacement = 'class="font-headline-hero text-3xl sm:text-4xl md:text-5xl lg:text-headline-hero text-primary tracking-tight font-bold leading-tight" id="heroTitle"'

if target in text:
    text = text.replace(target, replacement)
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: heroTitle updated with responsive scaling.")
else:
    print("NOT FOUND: heroTitle target string")
