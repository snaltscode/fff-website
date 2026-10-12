import sqlite3

conn = sqlite3.connect('f4f_community.db')
cursor = conn.cursor()

# 1. Deactivate fake seed testimonials
cursor.execute("""
    UPDATE testimonials 
    SET is_active = 0 
    WHERE business_name IN ('Apex Global Tech', 'Precision Industries', 'Elevate Digital')
       OR author_name IN ('Vikram K.', 'Ananya M.', 'Rohan S.')
""")
print(f"Deactivated {cursor.rowcount} fake testimonials.")

# 2. Deactivate Unsplash demo images in event_gallery
cursor.execute("""
    UPDATE event_gallery 
    SET is_active = 0 
    WHERE image_url LIKE '%unsplash.com%'
""")
print(f"Deactivated {cursor.rowcount} demo event gallery photos.")

# 2.5 Delete fake seed 1:1 meetings
cursor.execute("""
    DELETE FROM one_on_one_meetings 
    WHERE partner_company IN ('Apex Global Tech', 'Precision Industries', 'Elevate Digital')
""")
print(f"Deleted {cursor.rowcount} fake 1:1 meetings.")

# 3. Clean up site_settings hero and feature images to point to verified local assets
settings_updates = {
    'hero_capsule_1_url': '/assets/hero_banner.jpg',
    'hero_capsule_2_url': '/assets/logo.png',
    'hero_capsule_3_url': '/assets/hero_banner.png',
    'feature_img_network': '/assets/hero_banner.jpg',
    'feature_img_needs': '/assets/hero_banner.jpg',
    'feature_img_crm': '/assets/hero_banner.jpg',
    'feature_img_meetings': '/assets/hero_banner.jpg',
    'feature_img_collaborations': '/assets/hero_banner.jpg',
    'feature_img_challenges': '/assets/hero_banner.jpg',
}

for k, v in settings_updates.items():
    cursor.execute("UPDATE site_settings SET key_value = ? WHERE key_name = ?", (v, k))

print(f"Updated {len(settings_updates)} site_settings entries.")

conn.commit()
conn.close()
print("Database cleanup complete.")
