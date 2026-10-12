import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update loadAdminTab logic for overviewRes and auditRes
target_overview = '''    // 1. Process Overview & Recent Applications
    if (overviewRes.status === 'fulfilled' && overviewRes.value.ok) {
      const data = await overviewRes.value.json();
      if (document.getElementById('adminMetricsGrid') && data.metrics) {
        document.getElementById('adminMetricsGrid').innerHTML = `
          <div class="card"><div style="color:var(--grey-500); font-weight:700; font-size:0.8rem; text-transform:uppercase;">Total Members</div><div style="font-size:1.8rem; font-weight:800; color:var(--ink-primary); margin-top:4px;">${data.metrics.total_members}</div></div>
          <div class="card"><div style="color:var(--grey-500); font-weight:700; font-size:0.8rem; text-transform:uppercase;">Active MRR</div><div style="font-size:1.8rem; font-weight:800; color:var(--emerald-700); margin-top:4px;">₹${(data.metrics.mrr || 0).toLocaleString('en-IN')}</div></div>
          <div class="card"><div style="color:var(--grey-500); font-weight:700; font-size:0.8rem; text-transform:uppercase;">New Applications</div><div style="font-size:1.8rem; font-weight:800; color:var(--emerald-700); margin-top:4px;">${data.metrics.new_applications}</div></div>
        `;
      }

      if (document.getElementById('applicationsTable')) {
        state.adminApplications = data.recent_applications || [];
        let html = `<table style="width:100%; text-align:left; border-collapse:collapse; color:var(--ink-primary);">
          <thead>
            <tr style="border-bottom:1px solid var(--mint-200); font-size:0.82rem; text-transform:uppercase; color:var(--grey-500);">
              <th style="padding:10px;">Applicant</th>
              <th>Type / Role</th>
              <th>Business & Model</th>
              <th>Contact</th>
              <th>Status</th>
              <th>Update Status</th>
              <th>Inspection & Actions</th>
            </tr>
          </thead>
          <tbody>`;

        (data.recent_applications || []).forEach(app => {
          const inviteLink = app.invitation_token ? `${window.location.origin}/#activate?token=${app.invitation_token}` : '';
          const badgeClass = app.status === 'APPROVED' || app.status === 'INVITED' || app.status === 'CONVERTED' ? 'badge-verified' : (app.status === 'DECLINED' ? 'badge-pending' : 'badge-active');

          html += `<tr style="border-bottom:1px solid var(--border-hairline); font-size:0.88rem;">
            <td style="padding:10px; font-weight:700;">${app.full_name}</td>
            <td><span class="badge badge-active">${app.applicant_type || 'Founder'}</span><br><span style="font-size:0.75rem; color:var(--grey-500);">${app.designation || ''}</span></td>
            <td>${app.business_name || 'N/A'}<br><span style="font-size:0.75rem; color:var(--emerald-700); font-weight:600;">${app.business_model_category || 'Product Based'}</span> • <span style="font-size:0.75rem; color:var(--grey-500);">${app.city || 'Pan India'}</span></td>
            <td>${app.email}<br><span style="font-size:0.75rem; color:var(--grey-500);">${app.phone}</span></td>
            <td><span class="badge ${badgeClass}">${app.status}</span></td>
            <td>
              <select class="form-select" style="padding:4px 8px; font-size:0.78rem; min-width:130px;" onchange="updateAppStatus('${app.id}', this.value)">
                <option value="SUBMITTED" ${app.status === 'SUBMITTED' ? 'selected' : ''}>SUBMITTED</option>
                <option value="UNDER_REVIEW" ${app.status === 'UNDER_REVIEW' ? 'selected' : ''}>UNDER_REVIEW</option>
                <option value="APPROVED" ${app.status === 'APPROVED' ? 'selected' : ''}>APPROVED</option>
                <option value="INVITED" ${app.status === 'INVITED' ? 'selected' : ''}>INVITED</option>
                <option value="WAITLISTED" ${app.status === 'WAITLISTED' ? 'selected' : ''}>WAITLISTED</option>
                <option value="DECLINED" ${app.status === 'DECLINED' ? 'selected' : ''}>DECLINED</option>
              </select>
            </td>
            <td>
              <div style="display:flex; gap:6px; align-items:center;">
                <button class="btn btn-outline-emerald" style="padding:4px 8px; font-size:0.75rem;" onclick="openViewApplicationModal('${app.id}')">View Details</button>
                ${inviteLink ? `
                  <button class="btn btn-outline-emerald" style="padding:4px 8px; font-size:0.75rem;" onclick="navigator.clipboard.writeText('${inviteLink}'); alert('Invitation Link Copied:\\n${inviteLink}');">Copy Link</button>
                ` : `
                  <button class="btn btn-emerald" style="padding:4px 8px; font-size:0.75rem;" onclick="updateAppStatus('${app.id}', 'APPROVED')">Approve</button>
                `}
              </div>
            </td>
          </tr>`;
        });
        html += `</tbody></table>`;
        document.getElementById('applicationsTable').innerHTML = html;
      }
    }

    // 2. Process Audit Logs
    if (auditRes.status === 'fulfilled' && auditRes.value.ok) {
      const auditData = await auditRes.value.json();
      if (document.getElementById('auditLogsTable')) {
        let auditHtml = `<table style="width:100%; text-align:left; border-collapse:collapse; color:var(--ink-primary);">
          <thead>
            <tr style="border-bottom:1px solid var(--mint-200); font-size:0.82rem; text-transform:uppercase; color:var(--grey-500);">
              <th style="padding:8px;">Timestamp</th>
              <th>Action</th>
              <th>User / Entity</th>
              <th>IP Address</th>
            </tr>
          </thead>
          <tbody>`;
        (auditData.audit_logs || []).forEach(log => {
          auditHtml += `<tr style="border-bottom:1px solid var(--border-hairline); font-size:0.82rem;">
            <td style="padding:8px; color:var(--grey-500);">${log.created_at || ''}</td>
            <td style="font-weight:700; color:var(--emerald-900);">${log.action_type || ''}</td>
            <td>${log.entity_type || ''} (${log.user_id || 'System'})</td>
            <td style="color:var(--grey-500);">${log.ip_address || '127.0.0.1'}</td>
          </tr>`;
        });
        auditHtml += `</tbody></table>`;
        document.getElementById('auditLogsTable').innerHTML = auditHtml;
      }
    }'''

replacement_overview = '''    // 1. Process Overview & Recent Applications (Stitch Integrated)
    if (overviewRes.status === 'fulfilled' && overviewRes.value.ok) {
      const data = await overviewRes.value.json();
      if (data.metrics) {
        const totalEl = document.getElementById('statTotalMembers');
        const mrrEl = document.getElementById('statActiveMrr');
        const appsEl = document.getElementById('statPendingApps');
        if (totalEl) totalEl.textContent = data.metrics.total_members ?? 0;
        if (mrrEl) mrrEl.textContent = `₹${(data.metrics.mrr || 0).toLocaleString('en-IN')}`;
        if (appsEl) appsEl.textContent = data.metrics.new_applications ?? 0;
      }

      state.adminApplications = data.recent_applications || [];
      renderAdminApplications(state.adminApplications);
    }

    // 2. Process Audit Logs (Stitch Integrated)
    if (auditRes.status === 'fulfilled' && auditRes.value.ok) {
      const auditData = await auditRes.value.json();
      renderAdminAuditLogs(auditData.audit_logs || []);
    }'''

if target_overview in code:
    code = code.replace(target_overview, replacement_overview)
    print("Updated overviewRes & auditRes handlers.")
else:
    print("WARNING: target_overview not found in public/js/app.js")

# 2. Update renderAdminMeetingPhotosList
target_photos = '''function renderAdminMeetingPhotosList(photos) {
  const container = document.getElementById('adminMeetingPhotosList');
  if (!container) return;
  if (!photos || photos.length === 0) {
    container.innerHTML = '<p style="color: var(--grey-500); font-size: 0.9rem;">No meeting photos added yet.</p>';
    return;
  }
  container.innerHTML = photos.map(p => `
    <div style="background: var(--mint-50); border: 1px solid var(--mint-200); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column;">
      <div style="aspect-ratio: 16 / 9; overflow: hidden; background: #042F2C;">
        <img src="${p.image_url}" alt="${p.title}" loading="lazy" decoding="async" style="width: 100%; height: 100%; object-fit: cover; aspect-ratio: 16 / 9;">
      </div>
      <div style="padding: 12px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <span style="font-size: 0.72rem; font-weight: 800; color: var(--emerald-800); text-transform: uppercase; background: #E4F7EE; padding: 2px 6px; border-radius: 4px;">${p.tag || 'Curated Gathering'}</span>
          <h5 style="margin: 6px 0 2px 0; font-size: 0.98rem; color: var(--ink-primary);">${p.title}</h5>
          <p style="margin: 0; font-size: 0.8rem; color: var(--grey-600);">${p.caption || ''}</p>
        </div>
        <div style="margin-top: 12px; display: flex; justify-content: flex-end;">
          <button type="button" class="btn btn-outline-emerald" style="padding: 4px 10px; font-size: 0.75rem; color: #DC2626; border-color: #FECACA;" onclick="handleDeleteMeetingPhoto('${p.id}')"><svg class="icon-inline" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg> Remove</button>
        </div>
      </div>
    </div>
  `).join('');
}'''

replacement_photos = '''function renderAdminMeetingPhotosList(photos) {
  const container = document.getElementById('adminMeetingPhotosList');
  if (!container) return;
  if (!photos || photos.length === 0) {
    container.innerHTML = '<p class="col-span-1 sm:col-span-2 md:col-span-3 text-text-tertiary text-center py-8">No meeting photos added yet. Use the quick add form above to publish photography to the continuous 16:9 marquee slider.</p>';
    return;
  }
  container.innerHTML = photos.map(p => `
    <div class="bg-surface-card rounded-lg overflow-hidden shadow-sm flex flex-col group border border-hairline">
      <div class="aspect-video w-full relative overflow-hidden bg-surface-container">
        <img class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105" src="${escapeHtml(p.image_url)}" alt="${escapeHtml(p.title)}" loading="lazy" decoding="async">
        <div class="absolute inset-0 bg-gradient-to-t from-primary/80 via-transparent to-transparent"></div>
        <span class="absolute top-3 left-3 bg-primary-container/90 backdrop-blur-sm text-on-primary font-label-caps text-label-caps px-2 py-0.5 rounded">
          ${escapeHtml(p.tag || 'Curated Gathering')}
        </span>
        <div class="absolute bottom-3 left-3 right-3 text-on-primary">
          <span class="font-label-md text-label-md font-semibold block truncate">${escapeHtml(p.title)}</span>
          <span class="font-body-sm text-[12px] opacity-80 block truncate">${escapeHtml(p.caption || '16:9 Slider Active')}</span>
        </div>
      </div>
      <div class="p-3 flex items-center justify-between bg-surface-card">
        <span class="text-text-tertiary text-[12px]">Continuous Slider Active</span>
        <button type="button" class="w-8 h-8 rounded flex items-center justify-center text-error hover:bg-error-container hover:text-on-error-container transition-colors cursor-pointer" title="Delete from slider" onclick="handleDeleteMeetingPhoto('${p.id}')">
          <span class="material-symbols-outlined text-[18px]">delete</span>
        </button>
      </div>
    </div>
  `).join('');
}'''

if target_photos in code:
    code = code.replace(target_photos, replacement_photos)
    print("Updated renderAdminMeetingPhotosList.")
else:
    print("WARNING: target_photos not found in public/js/app.js")

# 3. Add application render, filter, and audit functions if not already present
admin_helpers = '''
// ==========================================
// STITCH ADMIN CONSOLE DYNAMIC RENDER & FILTERS
// ==========================================
let currentAppFilter = 'all';
let currentAppSearch = '';

function renderAdminApplications(apps) {
  const tbody = document.getElementById('applicationsTableBody');
  const countBadge = document.getElementById('appQueueCountBadge');
  const footerCount = document.getElementById('appTableFooterCount');
  if (countBadge) {
    countBadge.textContent = `${apps.length} in Queue`;
  }
  if (footerCount) {
    footerCount.textContent = `Showing ${apps.length} application${apps.length === 1 ? '' : 's'}`;
  }
  if (!tbody) return;

  if (!apps || apps.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="py-12 text-center text-text-tertiary">No applications match the current filter.</td></tr>`;
    return;
  }

  tbody.innerHTML = apps.map(app => {
    const inviteLink = app.invitation_token ? `${window.location.origin}/#activate?token=${app.invitation_token}` : '';
    const initials = (app.full_name || 'Founder').split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase();

    // Status pill styles matching Stitch theme
    let statusPill = '';
    if (app.status === 'APPROVED' || app.status === 'INVITED' || app.status === 'CONVERTED') {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-primary-fixed text-on-primary-fixed font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-emerald-deep"></span> ${app.status}</span>`;
    } else if (app.status === 'UNDER_REVIEW') {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-secondary"></span> REVIEW</span>`;
    } else if (app.status === 'WAITLISTED') {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container-high text-text-secondary font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-outline"></span> WAITLIST</span>`;
    } else if (app.status === 'DECLINED') {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-error-container text-on-error-container font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-error"></span> DECLINED</span>`;
    } else {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-subtle text-on-surface-variant font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-secondary"></span> PENDING</span>`;
    }

    return `
      <tr class="hover:bg-surface-subtle/50 transition-colors">
        <td class="py-4 px-space-md">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-primary text-on-primary font-semibold flex items-center justify-center font-label-md text-label-md flex-shrink-0">
              ${initials}
            </div>
            <div class="flex flex-col">
              <span class="font-label-md text-label-md text-text-primary font-semibold">${escapeHtml(app.full_name)}</span>
              <span class="text-text-tertiary text-[12px] flex items-center gap-1">
                <span class="material-symbols-outlined text-[13px]">location_on</span> ${escapeHtml(app.city || 'Pan India')}
              </span>
            </div>
          </div>
        </td>
        <td class="py-4 px-space-md">
          <div class="flex flex-col gap-1 items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded bg-surface-subtle text-primary font-label-caps text-label-caps">${escapeHtml(app.applicant_type || 'Founder')}</span>
            <span class="text-text-tertiary text-[11px]">${escapeHtml(app.designation || 'Founding Team')}</span>
          </div>
        </td>
        <td class="py-4 px-space-md">
          <div class="flex flex-col">
            <span class="font-medium text-text-primary">${escapeHtml(app.business_name || 'Private Venture')}</span>
            <span class="text-text-secondary text-[12px]">${escapeHtml(app.business_model_category || 'Product Based')}</span>
          </div>
        </td>
        <td class="py-4 px-space-md">
          <div class="flex flex-col text-[12px]">
            <span class="text-primary font-mono select-all">${escapeHtml(app.email)}</span>
            <div class="flex items-center gap-1 text-text-secondary mt-0.5">
              <span class="font-mono">${escapeHtml(app.phone)}</span>
              <span class="material-symbols-outlined text-[13px] text-secondary" title="Verified phone">verified</span>
            </div>
          </div>
        </td>
        <td class="py-4 px-space-md">
          ${statusPill}
        </td>
        <td class="py-4 px-space-md">
          <select class="h-9 px-2 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer border border-hairline" onchange="updateAppStatus('${app.id}', this.value)">
            <option value="SUBMITTED" ${app.status === 'SUBMITTED' ? 'selected' : ''}>SUBMITTED</option>
            <option value="UNDER_REVIEW" ${app.status === 'UNDER_REVIEW' ? 'selected' : ''}>UNDER_REVIEW</option>
            <option value="APPROVED" ${app.status === 'APPROVED' ? 'selected' : ''}>APPROVED</option>
            <option value="INVITED" ${app.status === 'INVITED' ? 'selected' : ''}>INVITED</option>
            <option value="WAITLISTED" ${app.status === 'WAITLISTED' ? 'selected' : ''}>WAITLISTED</option>
            <option value="DECLINED" ${app.status === 'DECLINED' ? 'selected' : ''}>DECLINED</option>
          </select>
        </td>
        <td class="py-4 px-space-md text-right">
          <div class="flex items-center justify-end gap-2">
            <button class="h-9 px-3 rounded bg-surface-subtle hover:bg-surface-container font-label-md text-label-md text-on-surface flex items-center gap-1.5 transition-colors cursor-pointer" onclick="openViewApplicationModal('${app.id}')">
              <span class="material-symbols-outlined text-[16px]">visibility</span>
              <span>Inspect</span>
            </button>
            ${inviteLink ? `
              <button class="h-9 px-3 rounded bg-surface-subtle hover:bg-surface-container font-label-md text-label-md text-primary flex items-center gap-1.5 transition-colors cursor-pointer" onclick="navigator.clipboard.writeText('${inviteLink}'); alert('Invitation Token Link Copied:\\n${inviteLink}');">
                <span class="material-symbols-outlined text-[16px]">content_copy</span>
                <span>Copy Token</span>
              </button>
            ` : `
              <button class="h-9 px-3 rounded bg-primary-container hover:bg-emerald-deep font-label-md text-label-md text-on-primary flex items-center gap-1.5 shadow-sm transition-all cursor-pointer" onclick="updateAppStatus('${app.id}', 'APPROVED')">
                <span class="material-symbols-outlined text-[16px]">send</span>
                <span>Approve</span>
              </button>
            `}
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

function renderAdminAuditLogs(logs) {
  const tbody = document.getElementById('auditLogsTableBody');
  if (!tbody) return;
  if (!logs || logs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" class="py-8 text-center text-text-tertiary">No audit logs recorded yet.</td></tr>`;
    return;
  }
  tbody.innerHTML = logs.map(log => {
    let actionBadge = `<span class="bg-surface-subtle text-primary px-2 py-0.5 rounded text-[11px] font-bold">${escapeHtml(log.action_type || 'AUDIT_LOG')}</span>`;
    if ((log.action_type || '').includes('APPROV') || (log.action_type || '').includes('CREATE')) {
      actionBadge = `<span class="bg-primary-fixed text-on-primary-fixed px-2 py-0.5 rounded text-[11px] font-bold">${escapeHtml(log.action_type)}</span>`;
    } else if ((log.action_type || '').includes('TOKEN') || (log.action_type || '').includes('INVIT')) {
      actionBadge = `<span class="bg-secondary-container text-on-secondary-container px-2 py-0.5 rounded text-[11px] font-bold">${escapeHtml(log.action_type)}</span>`;
    }

    return `
      <tr class="hover:bg-surface-subtle/50 transition-colors">
        <td class="py-3.5 px-space-md text-text-tertiary">${escapeHtml(log.created_at || '')}</td>
        <td class="py-3.5 px-space-md">${actionBadge}</td>
        <td class="py-3.5 px-space-md text-text-primary font-mono text-[12px]">${escapeHtml(log.user_id || 'Master Admin')}</td>
        <td class="py-3.5 px-space-md text-text-secondary">${escapeHtml(log.entity_type || 'SYSTEM')} ${log.entity_id ? `(#${escapeHtml(String(log.entity_id).slice(0,8))})` : ''}</td>
        <td class="py-3.5 px-space-md text-right text-text-tertiary font-mono">${escapeHtml(log.ip_address || '127.0.0.1')}</td>
      </tr>
    `;
  }).join('');
}

function filterApplications(filterStatus, clickedTab) {
  currentAppFilter = filterStatus;
  const filterTabs = document.querySelectorAll('.filter-tab');
  filterTabs.forEach(t => {
    t.classList.remove('bg-surface-card', 'text-primary', 'shadow-sm');
    t.classList.add('text-text-secondary');
  });
  if (clickedTab) {
    clickedTab.classList.add('bg-surface-card', 'text-primary', 'shadow-sm');
    clickedTab.classList.remove('text-text-secondary');
  }
  applyAdminAppFilters();
}

function handleAppSearch(query) {
  currentAppSearch = (query || '').toLowerCase().trim();
  applyAdminAppFilters();
}

function handleMasterAdminSearch(query) {
  handleAppSearch(query);
  const searchInput = document.getElementById('appSearch');
  if (searchInput) searchInput.value = query;
}

function applyAdminAppFilters() {
  const allApps = state.adminApplications || [];
  const filtered = allApps.filter(app => {
    // Status Filter
    if (currentAppFilter !== 'all') {
      if (currentAppFilter === 'SUBMITTED' && app.status !== 'SUBMITTED') return false;
      if (currentAppFilter === 'UNDER_REVIEW' && app.status !== 'UNDER_REVIEW') return false;
      if (currentAppFilter === 'APPROVED' && (app.status !== 'APPROVED' && app.status !== 'INVITED' && app.status !== 'CONVERTED')) return false;
      if (currentAppFilter === 'WAITLISTED' && app.status !== 'WAITLISTED') return false;
    }
    // Search Text
    if (currentAppSearch) {
      const q = currentAppSearch;
      const match = (app.full_name || '').toLowerCase().includes(q) ||
                    (app.business_name || '').toLowerCase().includes(q) ||
                    (app.email || '').toLowerCase().includes(q) ||
                    (app.city || '').toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });
  renderAdminApplications(filtered);
}

// Global Export Dropdown Toggle Listener
document.addEventListener('click', (e) => {
  const exportBtn = document.getElementById('exportBtn');
  const exportMenu = document.getElementById('exportMenu');
  if (!exportBtn || !exportMenu) return;
  if (exportBtn.contains(e.target)) {
    e.stopPropagation();
    exportMenu.classList.toggle('hidden');
  } else if (!exportMenu.contains(e.target)) {
    exportMenu.classList.add('hidden');
  }
});
'''

if 'function renderAdminApplications' not in code:
    code += admin_helpers
    print("Appended Stitch admin helper functions to public/js/app.js.")

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved public/js/app.js successfully!")
