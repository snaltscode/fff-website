import urllib.parse

class DummyReq:
    def __init__(self, path):
        self.path = path
        self.headers = {}
    
    def get_effective_path(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if '__slug' in qs:
            slug = qs['__slug'][0]
            other_qs = {k: v for k, v in qs.items() if k != '__slug'}
            new_q = ('?' + urllib.parse.urlencode(other_qs, doseq=True)) if other_qs else ''
            return f"/api/{slug}{new_q}"
        return self.path

r1 = DummyReq('/api/index.py?__slug=public/content')
print('Test 1:', r1.get_effective_path())
assert r1.get_effective_path() == '/api/public/content'

r2 = DummyReq('/api/index.py?__slug=members&city=Bengaluru')
print('Test 2:', r2.get_effective_path())
assert r2.get_effective_path() == '/api/members?city=Bengaluru'

print('All slug tests passed!')
