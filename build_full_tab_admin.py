# Python script to build the complete tab-admin replacement HTML
import re

def build_tab_admin_html():
    with open('stitch_sections/top_and_header.html', 'r', encoding='utf-8') as f:
        top_header = f.read()

    with open('stitch_sections/section1_kpis.html', 'r', encoding='utf-8') as f:
        sec1 = f.read()

    with open('stitch_sections/section2_apps.html', 'r', encoding='utf-8') as f:
        sec2 = f.read()

    with open('stitch_sections/section3_audit.html', 'r', encoding='utf-8') as f:
        sec3 = f.read()

    with open('stitch_sections/section4_photos.html', 'r', encoding='utf-8') as f:
        sec4 = f.read()

    with open('stitch_sections/section5_cms.html', 'r', encoding='utf-8') as f:
        sec5 = f.read()

    with open('stitch_sections/section6_events.html', 'r', encoding='utf-8') as f:
        sec6 = f.read()

    with open('stitch_sections/scripts.html', 'r', encoding='utf-8') as f:
        scripts = f.read()

    # Refinements on each section:
    
    # Top header: wire export URLs
    top_header = top_header.replace('href="#"', 'href="/api/admin/export/csv?type=members" target="_blank"', 1)
    top_header = top_header.replace('href="#"', 'href="/api/admin/export/csv?type=applications" target="_blank"', 1)
    top_header = top_header.replace('href="#"', 'href="/api/admin/export/csv?type=audit" target="_blank"', 1)
    top_header = top_header.replace('admin@snalts.co', 'admin@founderforfounder.biz')

    # Section 1: KPI grid container
    sec1 = sec1.replace('<section class="grid grid-cols-1 md:grid-cols-3 gap-gutter">',
                        '<section class="grid grid-cols-1 md:grid-cols-3 gap-gutter" id="adminMetricsGrid">')

    # Section 2: Applications table container
    # Provide id="applicationsTable" for the table wrapper, and tbody id="applicationsTableBody"
    sec2 = sec2.replace('<div class="w-full overflow-x-auto">',
                        '<div class="w-full overflow-x-auto" id="applicationsTable">')
    sec2 = sec2.replace('<tbody class="divide-y divide-surface-subtle font-body-sm text-body-sm text-on-surface">',
                        '<tbody id="applicationsTableBody" class="divide-y divide-surface-subtle font-body-sm text-body-sm text-on-surface">')

    # Section 3: Audit logs table container
    sec3 = sec3.replace('Refresh Logs', 'Refresh Logs" onclick="loadAdminTab()')
    sec3 = sec3.replace('<div class="w-full overflow-x-auto">',
                        '<div class="w-full overflow-x-auto" id="auditLogsTable">')
    sec3 = sec3.replace('<tbody class="divide-y divide-surface-subtle font-body-sm text-body-sm font-mono text-[13px]">',
                        '<tbody id="auditLogsTableBody" class="divide-y divide-surface-subtle font-body-sm text-body-sm font-mono text-[13px]">')
    sec3 = sec3.replace('admin@snalts.co', 'admin@founderforfounder.biz')

    # Section 4: Meeting photos
    # Connect quick add form and photo grid
    sec4 = sec4.replace('<div class="grid grid-cols-1 md:grid-cols-3 gap-gutter">',
                        '<div class="grid grid-cols-1 md:grid-cols-3 gap-gutter" id="adminMeetingPhotosList">')

    # Section 7: Wrap in <div id="tab-admin" class="portal-tab" style="display: none;">
    full_html = f'''      <!-- TAB 9: ADMIN DASHBOARD & CMS (STITCH UI DESIGN) -->
      <div id="tab-admin" class="portal-tab" style="display: none;">
        <div class="flex flex-col w-full font-body-md text-on-surface">
{top_header}
{sec1}
{sec2}
{sec3}
{sec4}
{sec5}
{sec6}
        </div>
      </div>
{scripts}'''

    return full_html

if __name__ == '__main__':
    html = build_tab_admin_html()
    with open('test_tab_admin_assembled.html', 'w', encoding='utf-8') as out:
        out.write(html)
    print(f"Generated test_tab_admin_assembled.html ({len(html)} bytes)")
