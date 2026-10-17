import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://api.github.com/repos/snaltscode/fff-website/deployments', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode())
        print(f"Total deployments: {len(data)}")
        for d in data[:10]:
            print(f"ID: {d.get('id')} Ref: {d.get('ref')} Sha: {d.get('sha')[:8]} Env: {d.get('environment')} Created: {d.get('created_at')}")
            
            # Fetch deployment status
            stat_req = urllib.request.Request(d.get('statuses_url'), headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(stat_req, context=ctx) as s_resp:
                s_data = json.loads(s_resp.read().decode())
                for s in s_data[:2]:
                    print(f"   Status: {s.get('state')} TargetUrl: {s.get('target_url')} Desc: {s.get('description')}")
except Exception as e:
    print('Error:', e)
