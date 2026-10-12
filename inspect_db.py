import sqlite3

conn = sqlite3.connect('f4f_community.db')
c = conn.cursor()

print("--- MEMBER PROFILES ---")
for r in c.execute("SELECT id, user_id, full_name, business_name, designation, city, profile_photo, mobile, whatsapp FROM member_profiles").fetchall():
    print(r)

print("\n--- TESTIMONIALS ---")
for r in c.execute("SELECT * FROM testimonials").fetchall():
    print(r)

print("\n--- SITE SETTINGS ---")
for r in c.execute("SELECT key_name, key_value FROM site_settings").fetchall():
    print(r)

conn.close()
