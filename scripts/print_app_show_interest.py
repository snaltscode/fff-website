with open('public/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('/api/public/show-interest')
if pos != -1:
    start = js.rfind('function', 0, pos)
    end = js.find('}', pos + 200)
    print("Function handling show-interest:\n")
    print(js[start:end+1])
