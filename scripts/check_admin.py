import sqlite3
import hashlib

conn = sqlite3.connect('f4f_community.db')
cursor = conn.cursor()

# 1. Verify admin password
h = cursor.execute("SELECT password_hash FROM users WHERE email = 'admin@founderforfounder.in'").fetchone()[0]
salt, stored_key = h.split('$')
cand = hashlib.pbkdf2_hmac('sha256', b'Admin@123', salt.encode('utf-8'), 100000).hex()
print("Admin@123 matches:", cand == stored_key)

# 2. Update remaining unsplash images in site_settings
cursor.execute("""
    UPDATE site_settings 
    SET key_value = '/assets/hero_banner.jpg'
    WHERE key_value LIKE '%unsplash.com%'
""")
print(f"Updated {cursor.rowcount} remaining unsplash settings to verified local asset.")

conn.commit()
conn.close()
