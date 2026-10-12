with open('public/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start line "// 1. Process Overview & Recent Applications"
start_idx = None
end_idx = None

for i, l in enumerate(lines):
    if '// 1. Process Overview & Recent Applications' in l:
        start_idx = i
    if '// 3. Process Site Settings Customizer' in l:
        end_idx = i
        break

print(f"Found block from line {start_idx+1} to {end_idx+1}")

replacement_lines = [
    "    // 1. Process Overview & Recent Applications (Stitch Integrated)\n",
    "    if (overviewRes.status === 'fulfilled' && overviewRes.value.ok) {\n",
    "      const data = await overviewRes.value.json();\n",
    "      if (data.metrics) {\n",
    "        const totalEl = document.getElementById('statTotalMembers');\n",
    "        const mrrEl = document.getElementById('statActiveMrr');\n",
    "        const appsEl = document.getElementById('statPendingApps');\n",
    "        if (totalEl) totalEl.textContent = data.metrics.total_members ?? 0;\n",
    "        if (mrrEl) mrrEl.textContent = `₹${(data.metrics.mrr || 0).toLocaleString('en-IN')}`;\n",
    "        if (appsEl) appsEl.textContent = data.metrics.new_applications ?? 0;\n",
    "      }\n",
    "\n",
    "      state.adminApplications = data.recent_applications || [];\n",
    "      renderAdminApplications(state.adminApplications);\n",
    "    }\n",
    "\n",
    "    // 2. Process Audit Logs (Stitch Integrated)\n",
    "    if (auditRes.status === 'fulfilled' && auditRes.value.ok) {\n",
    "      const auditData = await auditRes.value.json();\n",
    "      renderAdminAuditLogs(auditData.audit_logs || []);\n",
    "    }\n",
    "\n"
]

lines[start_idx:end_idx] = replacement_lines

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Successfully replaced overview & audit log block in public/js/app.js!")
