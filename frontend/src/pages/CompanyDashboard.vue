<template>
  <div class="company-shell">

    <!-- SIDEBAR -->
    <aside class="sidebar">
      <div class="sidebar-brand">
        <span class="brand-icon">🏢</span>
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
        </a>
      </nav>

      <div class="sidebar-footer">
        <button class="btn-logout" @click="logout">⎋ Logout</button>
      </div>
    </aside>

    <!-- MAIN -->
    <main class="main-content">

      <!-- TOPBAR -->
      <header class="topbar">
        <div>
          <h1>{{ currentLabel }}</h1>
          <span class="topbar-subtitle">Company Recruitment Portal</span>
        </div>
      </header>

      <!-- CREATE DRIVE -->
      <section v-if="activeSection === 'create'" class="section">
        <div class="section-card">
          <div class="card-title">📋 New Placement Drive</div>
          <div class="form-grid">
            <div class="form-group">
              <label>Job Title</label>
              <input v-model="form.job_title" class="form-control" placeholder="e.g. Software Engineer" />
            </div>
            <div class="form-group">
              <label>Application Deadline</label>
              <input v-model="form.deadline" type="date" class="form-control" />
            </div>
            <div class="form-group full-width">
              <label>Job Description</label>
              <textarea v-model="form.job_description" class="form-control" rows="4" placeholder="Describe the role, responsibilities, and requirements…"></textarea>
            </div>
            <div class="form-group">
              <label>Eligible Branches</label>
              <input v-model="form.branch" class="form-control" placeholder="e.g. CSE, IT, CSM" />
            </div>
            <div class="form-group">
              <label>Minimum CGPA</label>
              <input v-model="form.cgpa" class="form-control" placeholder="e.g. 7.5" type="number" step="0.1" />
            </div>
            <div class="form-group">
              <label>Year of Study</label>
              <input v-model="form.year" class="form-control" placeholder="e.g. 4" />
            </div>
            <div class="full-width">
              <button class="btn-primary-action" @click="createDrive">
                🚀 Create Drive
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- DRIVES LIST -->
      <section v-if="activeSection === 'drives'" class="section">
        <div class="section-card">
          <div class="card-title">Your Placement Drives</div>
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Job Title</th>
                  <th>Status</th>
                  <th>Applicants</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="d in drives" :key="d.id"
                    :class="{ 'row-active': selectedDrive === d.id }">
                  <td class="text-muted">{{ d.id }}</td>
                  <td><strong>{{ d.job_title }}</strong></td>
                  <td>
                    <span class="status-badge"
                      :class="{
                        'badge-pending':  d.status === 'Pending',
                        'badge-approved': d.status === 'Approved',
                        'badge-rejected': d.status === 'Rejected'
                      }">{{ d.status }}</span>
                  </td>
                  <td>
                    <button class="btn-action btn-view"
                      @click="loadApplicants(d.id)">
                      View Applicants
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- APPLICANTS PANEL -->
        <transition name="fade">
          <div v-if="applicants.length" class="section-card mt-20">
            <div class="card-title applicants-header">
              <span>Applicants for Drive #{{ selectedDrive }}</span>
              <button class="btn-close" @click="applicants = []">✕ Close</button>
            </div>
            <div class="table-wrapper">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Student</th>
                    <th>Current Status</th>
                    <th>Update Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="a in applicants" :key="a.application_id">
                    <td>
                      <div class="student-cell">
                        <div class="avatar">{{ a.student_name?.charAt(0) }}</div>
                        {{ a.student_name }}
                      </div>
                    </td>
                    <td>
                      <span class="status-badge"
                        :class="{
                          'badge-pending':  a.status === 'Pending',
                          'badge-warning':  a.status === 'Shortlisted',
                          'badge-approved': a.status === 'Selected',
                          'badge-rejected': a.status === 'Rejected'
                        }">{{ a.status }}</span>
                    </td>
                    <td>
                      <div class="action-group">
                        <button class="btn-action btn-shortlist"
                          @click="updateStatus(a.application_id, 'Shortlisted')">Shortlist</button>
                        <button class="btn-action btn-approve"
                          @click="updateStatus(a.application_id, 'Selected')">Select</button>
                        <button class="btn-action btn-reject"
                          @click="updateStatus(a.application_id, 'Rejected')">Reject</button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </transition>
      </section>

    </main>
  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      activeSection: "drives",
      drives: [],
      applicants: [],
      selectedDrive: null,
      form: {
        job_title: "", job_description: "",
        branch: "", cgpa: "", year: "", deadline: ""
      },
      navItems: [
        { key: "drives", icon: "📋", label: "My Drives" },
        { key: "create", icon: "➕", label: "Create Drive" }
      ]
    };
  },

  computed: {
    currentLabel() {
      return this.navItems.find(i => i.key === this.activeSection)?.label || "";
    }
  },

  mounted() { this.fetchDrives(); },

  methods: {
    logout() { localStorage.clear(); this.$router.push("/"); },

    async createDrive() {
      await API.post("/company/create_drive", { ...this.form });
      alert("Drive created!");
      this.fetchDrives();
      this.activeSection = "drives";
    },

    async fetchDrives() {
      const res = await API.get("/company/drives");
      this.drives = res.data;
    },

    async loadApplicants(drive_id) {
      this.selectedDrive = drive_id;
      const res = await API.get(`/company/applicants/${drive_id}`);
      this.applicants = res.data;
    },

    async updateStatus(app_id, status) {
      await API.put(`/company/application/update/${app_id}`, { status });
      alert("Status updated");
      this.loadApplicants(this.selectedDrive);
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.company-shell {
  display: flex;
  min-height: 100vh;
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: #f0f2f7;
}

.sidebar {
  width: 220px;
  background: #0f172a;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 24px 20px 20px;
  border-bottom: 1px solid #1e293b;
  color: #fff;
  font-size: 1.15rem;
  font-weight: 700;
}
.brand-icon { font-size: 1.4rem; }

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
}
.nav-item:hover { background: #1e293b; color: #fff; }
.nav-item.active { background: #0ea5e9; color: #fff; }
.nav-icon { font-size: 1rem; width: 20px; text-align: center; }

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
  transition: all 0.15s;
}
.btn-logout:hover { background: #1e293b; color: #fff; }

.main-content {
  margin-left: 220px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.topbar {
  background: #fff;
  padding: 18px 28px;
  border-bottom: 1px solid #e2e8f0;
}
.topbar h1 { font-size: 1.3rem; font-weight: 700; color: #0f172a; }
.topbar-subtitle { font-size: 0.8rem; color: #94a3b8; }

.section { padding: 28px; }
.mt-20 { margin-top: 20px; }

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
.applicants-header { display: flex; justify-content: space-between; align-items: center; }
.btn-close {
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  color: #64748b;
  font-size: 0.8rem;
  padding: 4px 10px;
}
.btn-close:hover { background: #f1f5f9; }

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  padding: 22px;
}
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group.full-width, .full-width { grid-column: 1 / -1; }
.form-group label { font-size: 0.82rem; font-weight: 600; color: #475569; }
.form-control {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.9rem;
  color: #0f172a;
  outline: none;
  transition: border 0.15s;
  font-family: inherit;
  resize: vertical;
}
.form-control:focus { border-color: #0ea5e9; box-shadow: 0 0 0 3px rgba(14,165,233,0.1); }

.btn-primary-action {
  padding: 12px 28px;
  background: #0ea5e9;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-primary-action:hover { background: #0284c7; }

.table-wrapper { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.data-table thead tr { background: #f8fafc; border-bottom: 2px solid #e2e8f0; }
.data-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
}
.data-table td { padding: 14px 16px; border-bottom: 1px solid #f1f5f9; color: #1e293b; }
.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr:hover td { background: #f8fafc; }
.row-active td { background: #f0f9ff !important; }
.text-muted { color: #94a3b8; }

.student-cell { display: flex; align-items: center; gap: 10px; font-weight: 600; }
.avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: #0ea5e9; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; font-weight: 700; flex-shrink: 0;
}

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

.action-group { display: flex; gap: 6px; flex-wrap: wrap; }
.btn-action {
  padding: 6px 12px; border-radius: 6px;
  font-size: 0.78rem; font-weight: 600;
  border: none; cursor: pointer; transition: all 0.15s;
}
.btn-view      { background: #e0f2fe; color: #0369a1; }
.btn-view:hover { background: #0ea5e9; color: #fff; }
.btn-shortlist { background: #fef3c7; color: #b45309; }
.btn-shortlist:hover { background: #f59e0b; color: #fff; }
.btn-approve   { background: #d1fae5; color: #065f46; }
.btn-approve:hover { background: #059669; color: #fff; }
.btn-reject    { background: #fee2e2; color: #991b1b; }
.btn-reject:hover { background: #ef4444; color: #fff; }

.fade-enter-active, .fade-leave-active { transition: all 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(8px); }
</style>