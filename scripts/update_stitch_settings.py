import sqlite3

conn = sqlite3.connect('f4f_community.db')
cursor = conn.cursor()

stitch_images = {
    'hero_capsule_1_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBQOGkFg7WlUWSrH99zAr_NpVfxigqQdvK1JXSl3dRMsAah88IIJNAhSx8OtC4DKo9EJqPKrthaRiIpLyqt_xcOwaZP62w7cSPmLdKivLOoQd09W35SQpnkWSfEWVisoyktKg1Orkg8BptmZwIKPc3y1r-4ghvDAecJkMjxHFDzIQYE2O1zppL4xfqRP3baviEwS-40bNBYfBFV6PFSQ0z7D12zfeBHWQ_3r5oCcjVYX2-bGarNL6J7',
    'format_img_play': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBVZvQ8mvPxjjMTjLrF6-VqxIN0JEH2LYfuTgdcdGk8PvQJyiu2u5oUtJijFilpwAZABufmCOZ06UT57PQqBGEKg1-9OMd-FRWPy29OF454SI1Ln-aaI9CEglLaVMReFz2gQ03uy4ow09oEq5zXUjdalnL-7FSNgARVaL5qOVsGy11qfvzW63V6icp4B0-nVZYF19XZFsC63s9ZAMvAZiIyVtOHp0EXxr4_1ZbrkQpBaEiN3iParP9H',
    'format_img_explore': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCw3xI8RlZpWZZ17uYgNPXasB04r1wJ0whnybywimVFdwREr2rr3DDSLYUulOUtaIVmEF80MqZbw10LmTsFrhl3rXyBNL72LAzwCDpNJJneZqJPTPRSkhlKzAiFKS0Tn1iRRN8nO65zy6XqDSx0PbtzudO-cEaeOigNSihGIOw_GdwmVBTeL7A0Cm4M1Z1dGv29lhLSDdtXG_2o5S3MccxG6bZxfslS2BnVSCHvd5UxkkZiTjyt0-6q',
    'format_img_dine': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCBen8o-u4_a_KNZnmBPSlcSQkQnSlXVC-0qrB9AuScyPbRygpxb68mYWNoCy69eIlaNxi6FkrV7mJfwh3bUsuRLj84Od-p6BleYqSdJMRF79MsyY8pxbZwLS29Vp5e3DPlSRjeCYCtSUdxKbFOF4f26E9pgbmVgDz4jPROhIk2cqPzRgfkpEi-8iE7obRt1sv15_o7XqKE-PVrJM6xGmFN9_Tqsr5pAQOE7HF_VtMpZVUT8aD9EZn6',
    'format_img_build': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDN0pvVm_B1pcvX3C1p41zAEVv0F7UOI4ZTEugE8UJNnDeu5eNbAPsWH_IRBeMTTrBdA1Zpcf2ZypCbINRgud_0WaGY9LhRanEqZLYWkrdklcms6PyKaBzR6EiAgA4rYlrNQ-aPnPLdocN7UEYfEq2eAVjX5vKcMzASL9PbNdFccHCH-3vD01dWm7WYDmctJQmiJRSbwgyZ7oPtz252aZQLyRXIxBYIhzTXyU4bbmWRw5KNEMp02I-u',
    'format_img_celebrate': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDMlhWLkz1P-mAPBK0gUIwbxPJcntsb_nuq1ISYkf94RDSh48oieYKwAMHeik8gD0Ev1u5UN-XgFp8CYopUvicZNBFwYnZ3sV9DL43PO02Ra8X0ENCaaSr2YHl121PlGI1_CAUaRP9E9uB33aoy9A-fhPPa1fn4ODQSR0o8gSOldIdnFRVHcVu-WJYsMtsdrx5u91M5OrNIuFwVbWfIO9F_ap7LdiFrLl6PmOLMCmy7I5ecoUoXXNBQ'
}

for key, val in stitch_images.items():
    cursor.execute("UPDATE site_settings SET key_value = ? WHERE key_name = ?", (val, key))

conn.commit()
print("UPDATED SITE_SETTINGS WITH STITCH REAL ASSETS!")

cursor.execute("SELECT key_name, key_value FROM site_settings WHERE key_name LIKE '%img%' OR key_name LIKE '%capsule%'")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()
