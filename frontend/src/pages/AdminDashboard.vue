<template>
  <div class="admin-shell">

    <!-- SIDEBAR -->
    <aside class="sidebar">
      <div class="sidebar-brand">
        <span class="brand-icon">🎓</span>
        <span class="brand-text">PlaceIT</span>
      </div>

      <nav class="sidebar-nav">
        <a
          v-for="item in navItems"
          :key="item.key"
          class="nav-item"
          :class="{ active: activeSection === item.key }"
          @click="activeSection = item.key"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
          <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
        </a>
      </nav>

      <div class="sidebar-footer">
        <button class="btn-logout" @click="logout">
          <span>⎋</span> Logout
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="main-content">

      <!-- TOP BAR -->
      <header class="topbar">
        <div class="topbar-title">
          <h1>{{ currentSectionLabel }}</h1>
          <span class="topbar-subtitle">Placement Administration Portal</span>
        </div>
        <div class="topbar-actions">
          <div class="search-wrapper">
            <div class="search-container-placeholder" :class="{ active: searchFocused }">
              <span class="search-icon">🔍</span>
              <input
                type="text"
                v-model="searchQuery"
                class="search-input"
                placeholder="Search students or companies..."
                @input="onSearchInput"
                @focus="searchFocused = true"
                @blur="handleBlur"
                @keydown.escape="closeSearch"
              />
              <span v-if="searchLoading" class="search-spinner">⏳</span>
              <button v-if="searchQuery" class="search-clear" @click="clearSearch">✕</button>
            </div>

            <!-- SEARCH RESULTS DROPDOWN -->
            <div v-if="showSearchResults && searchQuery" class="search-dropdown">
              <div v-if="searchLoading" class="search-state">Searching…</div>
              <div v-else-if="!searchResults.students.length && !searchResults.companies.length" class="search-state">
                No results for "<strong>{{ searchQuery }}</strong>"
              </div>
              <template v-else>
                <div v-if="searchResults.students.length">
                  <div class="search-group-label">👤 Students</div>
                  <div v-for="s in searchResults.students" :key="'s-'+s.id"
                       class="search-result-item" @mousedown="goToStudent(s)">
                    <div class="result-avatar">{{ s.name?.charAt(0) }}</div>
                    <div class="result-info">
                      <span class="result-name">{{ s.name }}</span>
                      <span class="result-sub">{{ s.email }}</span>
                    </div>
                    <span class="result-tag" :class="s.active ? 'tag-active' : 'tag-blocked'">
                      {{ s.active ? 'Active' : 'Blacklisted' }}
                    </span>
                  </div>
                </div>
                <div v-if="searchResults.companies.length">
                  <div class="search-group-label">🏢 Companies</div>
                  <div v-for="c in searchResults.companies" :key="'c-'+c.id"
                       class="search-result-item" @mousedown="goToCompany(c)">
                    <div class="result-avatar result-avatar-company">{{ c.company_name?.charAt(0) }}</div>
                    <div class="result-info">
                      <span class="result-name">{{ c.company_name }}</span>
                      <span class="result-sub">Click to manage</span>
                    </div>
                    <span class="result-tag"
                      :class="{
                        'tag-pending':  c.approval_status === 'Pending',
                        'tag-active':   c.approval_status === 'Approved',
                        'tag-blocked':  c.approval_status === 'Rejected'
                      }">{{ c.approval_status }}</span>
                  </div>
                </div>
              </template>
            </div>
          </div>

          <button class="btn-reports" @click="toggleReports">
            🔔 Reports
            <span v-if="reports.length" class="report-count">{{ reports.length }}</span>
          </button>
        </div>
      </header>

      <!-- REPORTS PANEL -->
      <transition name="slide-down">
        <div v-if="showReports" class="reports-panel">
          <div class="reports-header">
            <h3>📊 Monthly Reports</h3>
            <button class="btn-close-reports" @click="showReports = false">✕</button>
          </div>
          <div v-if="!reports.length" class="empty-state">No reports generated yet.</div>
          <div v-for="r in reports" :key="r.id" class="report-card">
            <div v-html="r.html_content"></div>
          </div>
        </div>
      </transition>

      <!-- OVERVIEW SECTION -->
      <section v-if="activeSection === 'overview'" class="section">
        <!-- STATS ROW -->
        <div class="stats-grid">
          <div class="stat-card" v-for="card in statsCards" :key="card.title">
            <div class="stat-icon">{{ card.icon }}</div>
            <div class="stat-info">
              <span class="stat-value">{{ card.value }}</span>
              <span class="stat-label">{{ card.title }}</span>
            </div>
          </div>
        </div>

        <!-- QUICK ACTIONS -->
        <div class="section-card">
          <div class="card-title">Quick Navigation</div>
          <div class="quick-actions">
            <button
              v-for="item in navItems.filter(i => i.key !== 'overview')"
              :key="item.key"
              class="quick-btn"
              @click="activeSection = item.key"
            >
              {{ item.icon }} {{ item.label }}
            </button>
          </div>
        </div>
      </section>

      <!-- COMPANIES SECTION -->
      <section v-if="activeSection === 'companies'" class="section">
        <div class="section-card">
          <div class="card-title">Registered Companies</div>
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Company Name</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in companies" :key="c.id">
                  <td><span class="company-name">{{ c.company_name }}</span></td>
                  <td>
                    <span class="status-badge"
                      :class="{
                        'badge-pending': c.approval_status === 'Pending',
                        'badge-approved': c.approval_status === 'Approved',
                        'badge-rejected': c.approval_status === 'Rejected'
                      }">
                      {{ c.approval_status }}
                    </span>
                  </td>
                  <td>
                    <div class="action-group">
                      <button class="btn-action btn-approve"
                        :disabled="c.approval_status === 'Approved'"
                        @click="approveCompany(c.id)">✓ Approve</button>
                      <button class="btn-action btn-reject"
                        :disabled="c.approval_status === 'Rejected'"
                        @click="rejectCompany(c.id)">✕ Reject</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- DRIVES SECTION -->
      <section v-if="activeSection === 'drives'" class="section">
        <div class="section-card">
          <div class="card-title">Placement Drives</div>
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Job Title</th>
                  <th>Company</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="d in drives" :key="d.id">
                  <td><strong>{{ d.job_title }}</strong></td>
                  <td>{{ d.company }}</td>
                  <td>
                    <span class="status-badge"
                      :class="{
                        'badge-pending': d.status === 'Pending',
                        'badge-approved': d.status === 'Approved'
                      }">
                      {{ d.status }}
                    </span>
                  </td>
                  <td>
                    <button class="btn-action btn-approve"
                      :disabled="d.status === 'Approved'"
                      @click="approveDrive(d.id)">
                      {{ d.status === 'Approved' ? '✓ Approved' : '✓ Approve' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- STUDENTS SECTION -->
      <section v-if="activeSection === 'students'" class="section">
        <div class="section-card">
          <div class="card-title">Student Registry</div>
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Student Name</th>
                  <th>Email</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="s in students" :key="s.id">
                  <td>
                    <div class="student-name-cell">
                      <div class="avatar">{{ s.name?.charAt(0) }}</div>
                      {{ s.name }}
                    </div>
                  </td>
                  <td class="text-muted">{{ s.email }}</td>
                  <td>
                    <button class="btn-action btn-reject"
                      :disabled="!s.active"
                      @click="blacklistUser(s.id)">
                      {{ s.active ? '⛔ Blacklist' : '⛔ Blacklisted' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- APPLICATIONS SECTION -->
      <section v-if="activeSection === 'applications'" class="section">
        <div class="section-card">
          <div class="card-title">All Applications</div>
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Company</th>
                  <th>Drive</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="a in applications" :key="a.application_id">
                  <td>{{ a.student }}</td>
                  <td>{{ a.company }}</td>
                  <td>{{ a.drive }}</td>
                  <td>
                    <span class="status-badge"
                      :class="{
                        'badge-pending': a.status === 'Pending',
                        'badge-approved': a.status === 'Selected',
                        'badge-warning': a.status === 'Shortlisted',
                        'badge-rejected': a.status === 'Rejected'
                      }">
                      {{ a.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

    </main>
  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      activeSection: "overview",
      statsCards: [],
      companies: [],
      drives: [],
      students: [],
      applications: [],
      reports: [],
      showReports: false,

      searchQuery: "",
      searchFocused: false,
      searchLoading: false,
      showSearchResults: false,
      searchTimeout: null,
      searchResults: { students: [], companies: [] },

      navItems: [
        { key: "overview",     icon: "🏠", label: "Overview" },
        { key: "companies",    icon: "🏢", label: "Companies" },
        { key: "drives",       icon: "📋", label: "Drives" },
        { key: "students",     icon: "👤", label: "Students" },
        { key: "applications", icon: "📂", label: "Applications" },
      ]
    };
  },

  computed: {
    currentSectionLabel() {
      return this.navItems.find(i => i.key === this.activeSection)?.label || "";
    }
  },

  mounted() {
    this.loadDashboard();
    this.loadReports();
  },

  methods: {
    logout() { this.$router.push("/"); },
    toggleReports() { this.showReports = !this.showReports; },

    async loadReports() {
      const res = await API.get("/admin/reports");
      this.reports = res.data;
      this.navItems[0].badge = res.data.length || null;
    },

    async loadDashboard() {
      const stats = await API.get("/admin/dashboard");
      this.statsCards = [
        { title: "Students",     value: stats.data.students,     icon: "👤" },
        { title: "Companies",    value: stats.data.companies,    icon: "🏢" },
        { title: "Drives",       value: stats.data.drives,       icon: "📋" },
        { title: "Applications", value: stats.data.applications, icon: "📂" }
      ];
      this.companies    = (await API.get("/admin/companies")).data;
      this.drives       = (await API.get("/admin/drives")).data;
      this.students     = (await API.get("/admin/students")).data;
      this.applications = (await API.get("/admin/applications")).data;
    },

    // Debounced input handler — waits 400ms after user stops typing
    onSearchInput() {
      clearTimeout(this.searchTimeout);
      if (!this.searchQuery.trim()) {
        this.showSearchResults = false;
        this.searchResults = { students: [], companies: [] };
        return;
      }
      this.searchLoading = true;
      this.showSearchResults = true;
      this.searchTimeout = setTimeout(() => this.runSearch(), 400);
    },

    async runSearch() {
      try {
        const [studentsRes, companiesRes] = await Promise.all([
          API.get(`/admin/search/students?q=${encodeURIComponent(this.searchQuery)}`),
          API.get(`/admin/search/companies?q=${encodeURIComponent(this.searchQuery)}`)
        ]);
        this.searchResults = {
          students: studentsRes.data,
          companies: companiesRes.data
        };
      } catch (err) {
        console.error("Search error:", err);
        this.searchResults = { students: [], companies: [] };
      } finally {
        this.searchLoading = false;
      }
    },

    // Click a student result → go to Students section, highlight that row
    goToStudent(student) {
      this.students = [student];
      this.activeSection = "students";
      this.closeSearch();
    },

    // Click a company result → go to Companies section, show that company
    goToCompany(company) {
      this.companies = [company];
      this.activeSection = "companies";
      this.closeSearch();
    },

    clearSearch() {
      this.searchQuery = "";
      this.searchResults = { students: [], companies: [] };
      this.showSearchResults = false;
      this.loadDashboard(); // restore full data
    },

    closeSearch() {
      this.showSearchResults = false;
      this.searchFocused = false;
    },

    // Use mousedown (not blur) on results so click registers before blur hides dropdown
    handleBlur() {
      setTimeout(() => { this.searchFocused = false; this.showSearchResults = false; }, 150);
    },

    async approveCompany(id) { await API.put(`/admin/approve/company/${id}`); this.loadDashboard(); },
    async rejectCompany(id)  { await API.put(`/admin/reject/company/${id}`);  this.loadDashboard(); },
    async approveDrive(id)   { await API.put(`/admin/approve/drive/${id}`);   this.loadDashboard(); },
    async blacklistUser(id)  { await API.put(`/admin/blacklist/${id}`);        this.loadDashboard(); }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.admin-shell {
  display: flex;
  min-height: 100vh;
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: #f0f2f7;
}

/* ── SIDEBAR ── */
.sidebar {
  width: 240px;
  background: #0f172a;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 100;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 24px 20px 20px;
  border-bottom: 1px solid #1e293b;
  color: #fff;
  font-size: 1.2rem;
  font-weight: 700;
}
.brand-icon { font-size: 1.5rem; }

.sidebar-nav {
  flex: 1;
  padding: 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  color: #94a3b8;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.15s;
  position: relative;
}
.nav-item:hover { background: #1e293b; color: #fff; }
.nav-item.active { background: #3b82f6; color: #fff; }
.nav-icon { font-size: 1rem; width: 20px; text-align: center; }
.nav-label { flex: 1; }
.nav-badge {
  background: #ef4444;
  color: white;
  font-size: 0.7rem;
  border-radius: 10px;
  padding: 1px 7px;
  font-weight: 700;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #1e293b;
}
.btn-logout {
  width: 100%;
  padding: 10px;
  background: transparent;
  border: 1px solid #334155;
  border-radius: 8px;
  color: #94a3b8;
  cursor: pointer;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s;
}
.btn-logout:hover { background: #1e293b; color: #fff; }

/* ── MAIN ── */
.main-content {
  margin-left: 240px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* ── TOPBAR ── */
.topbar {
  background: #fff;
  padding: 18px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 50;
}
.topbar-title h1 { font-size: 1.3rem; font-weight: 700; color: #0f172a; }
.topbar-subtitle  { font-size: 0.8rem; color: #94a3b8; }
.topbar-actions   { display: flex; align-items: center; gap: 12px; }

.search-wrapper {
  position: relative;
  width: 320px;
}

.search-container-placeholder {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 14px;
  gap: 8px;
  width: 100%;
  transition: border 0.15s, box-shadow 0.15s;
}
.search-container-placeholder.active,
.search-container-placeholder:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
  background: #fff;
}
.search-icon { color: #94a3b8; font-size: 0.9rem; flex-shrink: 0; }
.search-input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.85rem;
  color: #0f172a;
  width: 100%;
  cursor: text;
  font-family: inherit;
}
.search-input::placeholder { color: #94a3b8; }
.search-spinner { font-size: 0.8rem; flex-shrink: 0; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.search-clear {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 0.8rem;
  padding: 2px 4px;
  border-radius: 4px;
  flex-shrink: 0;
  line-height: 1;
}
.search-clear:hover { background: #f1f5f9; color: #475569; }

/* Dropdown */
.search-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  z-index: 200;
  max-height: 380px;
  overflow-y: auto;
  padding: 6px 0;
}
.search-state {
  padding: 16px 18px;
  font-size: 0.85rem;
  color: #94a3b8;
  text-align: center;
}
.search-group-label {
  padding: 8px 16px 4px;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #94a3b8;
}
.search-result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.1s;
}
.search-result-item:hover { background: #f8fafc; }
.result-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #3b82f6;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  flex-shrink: 0;
}
.result-avatar-company { background: #8b5cf6; }
.result-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.result-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.result-sub {
  font-size: 0.76rem;
  color: #94a3b8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.result-tag {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 20px;
  flex-shrink: 0;
}
.tag-active  { background: #d1fae5; color: #065f46; }
.tag-blocked { background: #fee2e2; color: #991b1b; }
.tag-pending { background: #fef3c7; color: #b45309; }

.btn-reports {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #fef3c7;
  border: 1px solid #fde68a;
  border-radius: 8px;
  color: #92400e;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  transition: all 0.15s;
}
.btn-reports:hover { background: #fde68a; }
.report-count {
  background: #ef4444;
  color: white;
  font-size: 0.7rem;
  border-radius: 10px;
  padding: 1px 6px;
  font-weight: 700;
}

/* ── REPORTS PANEL ── */
.reports-panel {
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  padding: 20px 28px;
}
.reports-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.reports-header h3 { font-size: 1rem; font-weight: 600; color: #0f172a; }
.btn-close-reports {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  font-size: 1rem;
  padding: 4px 8px;
  border-radius: 4px;
}
.btn-close-reports:hover { background: #f1f5f9; }

.report-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.slide-down-enter-active, .slide-down-leave-active { transition: all 0.25s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-10px); }

/* ── SECTION ── */
.section {
  padding: 28px;
  flex: 1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.07);
  border: 1px solid #e2e8f0;
}
.stat-icon { font-size: 1.8rem; }
.stat-value { display: block; font-size: 1.7rem; font-weight: 700; color: #0f172a; }
.stat-label { font-size: 0.8rem; color: #64748b; font-weight: 500; }

.section-card {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.07);
  overflow: hidden;
}

.card-title {
  font-weight: 700;
  font-size: 0.95rem;
  color: #0f172a;
  padding: 18px 22px;
  border-bottom: 1px solid #f1f5f9;
  background: #fafbfc;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 18px 22px;
}
.quick-btn {
  padding: 10px 18px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
  cursor: pointer;
  transition: all 0.15s;
}
.quick-btn:hover { background: #3b82f6; color: #fff; border-color: #3b82f6; }

/* ── SEARCH BAR (students) ── */
.search-bar-container {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 10px 18px;
  gap: 10px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.search-bar-input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.9rem;
  color: #64748b;
  width: 100%;
  cursor: not-allowed;
}

/* ── TABLE ── */
.table-wrapper { overflow-x: auto; }

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
.data-table thead tr {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}
.data-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
}
.data-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
}
.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr:hover td { background: #f8fafc; }

.company-name { font-weight: 600; }
.text-muted { color: #94a3b8; }

.student-name-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #3b82f6;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  flex-shrink: 0;
}

/* ── STATUS BADGES ── */
.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}
.badge-pending  { background: #fef3c7; color: #b45309; }
.badge-approved { background: #d1fae5; color: #065f46; }
.badge-rejected { background: #fee2e2; color: #991b1b; }
.badge-warning  { background: #e0f2fe; color: #0369a1; }

/* ── ACTION BUTTONS ── */
.action-group { display: flex; gap: 8px; }
.btn-action {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-action:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-approve { background: #d1fae5; color: #065f46; }
.btn-approve:not(:disabled):hover { background: #059669; color: #fff; }
.btn-reject  { background: #fee2e2; color: #991b1b; }
.btn-reject:not(:disabled):hover  { background: #ef4444; color: #fff; }

.empty-state { color: #94a3b8; font-size: 0.9rem; padding: 12px; }
</style>