import subprocess
import os

js_test = '''
const puppeteer = require("puppeteer");
(async () => {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  page.on("console", msg => {
    if (msg.type() === "error") console.log("PAGE ERROR:", msg.text());
  });
  page.on("pageerror", err => console.log("UNCAUGHT EXCEPTION:", err.message));
  await page.goto("http://localhost:3000/", { waitUntil: "networkidle0" });
  await browser.close();
})();
'''

# Or check what error popup is rendering in public/index.html / Next.js
with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
m = re.findall(r'(\d+\s*error)', html, re.I)
print("Static error string in HTML:", m)
