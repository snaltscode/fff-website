"""
Vercel Serverless Function Entrypoint for Founder for Founder
"""
import sys
import os

# Ensure project root is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import server
import database

# Ensure database is initialized in /tmp when running on Vercel
try:
    database.init_db()
except Exception as e:
    print("Vercel DB Init Notice:", e)

class handler(server.F4FHTTPRequestHandler):
    """Vercel Serverless Function Handler."""
    pass
