import sqlite3

conn = sqlite3.connect('f4f_community.db')
c = conn.cursor()

print("--- EVENT GALLERY ---")
for r in c.execute("SELECT * FROM event_gallery").fetchall():
    print(r)

print("\n--- EVENTS ---")
for r in c.execute("SELECT id, title, image_url, event_date, location FROM events").fetchall():
    print(r)

print("\n--- NEEDS OFFERS ---")
for r in c.execute("SELECT id, user_id, title, need_type, description FROM needs_offers").fetchall():
    print(r)

print("\n--- LEADS ---")
for r in c.execute("SELECT id, user_id, lead_name, company, value, status FROM leads").fetchall():
    print(r)

print("\n--- AUDIT LOGS ---")
for r in c.execute("SELECT id, user_id, action, details FROM audit_logs ORDER BY created_at DESC LIMIT 10").fetchall():
    print(r)

conn.close()
