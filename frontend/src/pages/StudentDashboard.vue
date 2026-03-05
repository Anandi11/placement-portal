<template>
  <div class="student-shell">

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
        <div class="topbar-left">
          <h1>{{ currentLabel }}</h1>
          <span class="topbar-subtitle">Student Placement Portal</span>
        </div>
        <div class="topbar-right">
          <!-- Live drive search -->
          <div v-if="activeSection === 'drives'" class="search-wrapper">
            <div class="search-placeholder" :class="{ active: searchFocused }">
              <span class="search-icon">🔍</span>
              <input
                type="text"
                v-model="searchQuery"
                class="search-input"
                placeholder="Search drives by company or role..."
                @input="onSearchInput"
                @focus="searchFocused = true"
                @blur="handleSearchBlur"
                @keydown.escape="closeSearch"
              />
              <span v-if="searchLoading" class="search-spinner">⏳</span>
              <button v-if="searchQuery" class="search-clear" @click="clearSearch">✕</button>
            </div>

            <!-- DROPDOWN RESULTS -->
            <div v-if="showSearchResults && searchQuery" class="search-dropdown">
              <div v-if="searchLoading" class="search-state">Searching…</div>
              <div v-else-if="!searchResults.length" class="search-state">
                No drives found for "<strong>{{ searchQuery }}</strong>"
              </div>
              <template v-else>
                <div class="search-group-label">🚀 Matching Drives</div>
                <div
                  v-for="d in searchResults"
                  :key="d.id"
                  class="search-result-item"
                  @mousedown="selectDrive(d)"
                >
                  <div class="result-avatar">{{ d.company?.charAt(0) }}</div>
                  <div class="result-info">
                    <span class="result-name">{{ d.job_title }}</span>
                    <span class="result-sub">{{ d.company }}</span>
                  </div>
                  <span class="deadline-badge" :class="{ 'deadline-soon': isDeadlineSoon(d.deadline) }">
                    📅 {{ d.deadline }}
                  </span>
                </div>
              </template>
            </div>
          </div>

          <button v-if="activeSection !== 'profile'" class="btn-export" @click="exportApplications">
            ⬇ Export CSV
          </button>
        </div>
      </header>

      <!-- ── PROFILE SECTION ── -->
      <section v-if="activeSection === 'profile'" class="section">

        <div class="profile-hero">
          <div class="profile-avatar-wrap">
            <div class="profile-avatar">{{ profile.name?.charAt(0) || 'S' }}</div>
            <div class="avatar-online"></div>
          </div>
          <div class="profile-meta">
            <h2>{{ profile.name || 'Your Name' }}</h2>
            <p class="profile-sub">{{ profile.branch || 'Branch' }} &bull; Year {{ profile.year || 'N/A' }} &bull; CGPA {{ profile.cgpa || 'N/A' }}</p>
            <span class="profile-email">{{ profile.email || 'student@college.edu' }}</span>
          </div>
        </div>

        <div class="profile-grid">
          <div class="section-card">
            <div class="card-title">✏️ Edit Profile</div>
            <div class="form-grid">
              <div class="form-group">
                <label>Full Name</label>
                <input v-model="profile.name" class="form-control" placeholder="Your full name" />
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="profile.email" class="form-control" type="email" placeholder="student@college.edu" />
              </div>
              <div class="form-group">
                <label>Branch</label>
                <input v-model="profile.branch" class="form-control" placeholder="e.g. CSE" />
              </div>
              <div class="form-group">
                <label>Year</label>
                <input v-model="profile.year" class="form-control" placeholder="e.g. 4" type="number" />
              </div>
              <div class="form-group">
                <label>CGPA</label>
                <input v-model="profile.cgpa" class="form-control" placeholder="e.g. 8.5" type="number" step="0.1" />
              </div>
              <div class="form-group">
                <label>Phone</label>
                <input v-model="profile.phone" class="form-control" placeholder="e.g. +91 9876543210" />
              </div>
              <div class="form-group full-width">
                <label>Skills</label>
                <input v-model="profile.skills" class="form-control" placeholder="e.g. Python, React, SQL" />
              </div>
              <div class="form-group full-width">
                <label>About / Bio</label>
                <textarea v-model="profile.bio" class="form-control" rows="3" placeholder="Write a short bio about yourself…"></textarea>
              </div>
              <div class="full-width">
                <button class="btn-primary-action" @click="saveProfile">💾 Save Changes</button>
              </div>
            </div>
          </div>

          <div class="section-card resume-card">
            <div class="card-title">📄 Resume</div>
            <div class="resume-body">
              <div v-if="!resumeFile && !profile.resumeUrl" class="resume-dropzone"
                   @dragover.prevent @drop.prevent="onResumeDrop"
                   @click="$refs.resumeInput.click()">
                <div class="dropzone-icon">📁</div>
                <p class="dropzone-label">Drag & drop your resume here</p>
                <p class="dropzone-sub">or <span class="dropzone-link">click to browse</span></p>
                <p class="dropzone-hint">Accepts PDF, DOC, DOCX (max 5MB)</p>
                <input ref="resumeInput" type="file" accept=".pdf,.doc,.docx"
                       style="display:none" @change="onResumeSelect" />
              </div>

              <div v-else class="resume-preview">
                <div class="resume-file-info">
                  <span class="resume-file-icon">📄</span>
                  <div>
                    <p class="resume-file-name">{{ resumeFileName || 'resume.pdf' }}</p>
                    <p class="resume-file-size">{{ resumeFileSize }}</p>
                  </div>
                </div>
                <div class="resume-actions">
                  <button class="btn-action btn-view" @click="viewResume">View</button>
                  <button class="btn-action btn-reject" @click="removeResume">Remove</button>
                </div>
              </div>

              <button v-if="resumeFile" class="btn-primary-action resume-upload-btn" @click="uploadResume">
                ⬆ Upload Resume
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- ── DRIVES SECTION ── -->
      <section v-if="activeSection === 'drives'" class="section">
        <div class="section-card">
          <div class="card-title">🚀 Available Placement Drives</div>
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Job Title</th>
                  <th>Company</th>
                  <th>Deadline</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="d in drives" :key="d.id">
                  <td><strong>{{ d.job_title }}</strong></td>
                  <td>{{ d.company }}</td>
                  <td>
                    <span class="deadline-badge" :class="{ 'deadline-soon': isDeadlineSoon(d.deadline) }">
                      📅 {{ d.deadline }}
                    </span>
                  </td>
                  <td>
                    <button class="btn-action btn-apply" @click="apply(d.id)">✓ Apply</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ── APPLICATIONS SECTION ── -->
      <section v-if="activeSection === 'applications'" class="section">
        <div class="section-card">
          <div class="card-title-row">
            <span class="card-title-text">📂 My Applications</span>
            <button class="btn-sm-secondary" @click="fetchAppliedDrives">🔄 Refresh</button>
          </div>
          <div v-if="appliedDrives.length" class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Drive</th>
                  <th>Company</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="a in appliedDrives" :key="a.id">
                  <td><strong>{{ a.drive }}</strong></td>
                  <td>{{ a.company }}</td>
                  <td>
                    <span class="status-badge"
                      :class="{
                        'badge-pending':  a.status === 'Pending',
                        'badge-warning':  a.status === 'Shortlisted',
                        'badge-approved': a.status === 'Selected',
                        'badge-rejected': a.status === 'Rejected'
                      }">{{ a.status }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty-state">
            <span class="empty-icon">📭</span>
            <p>No applications yet. Browse drives and apply!</p>
            <button class="btn-primary-action" @click="activeSection = 'drives'">Browse Drives</button>
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
      activeSection: "drives",
      drives: [],
      appliedDrives: [],
      resumeFile: null,
      resumeFileName: "",
      resumeFileSize: "",

      searchQuery: "",
      searchFocused: false,
      searchLoading: false,
      showSearchResults: false,
      searchTimeout: null,
      searchResults: [],

      profile: {
        name: "", email: "", branch: "",
        year: "", cgpa: "", phone: "",
        skills: "", bio: "", resumeUrl: null
      },
      navItems: [
        { key: "profile",      icon: "👤", label: "My Profile" },
        { key: "drives",       icon: "🚀", label: "Available Drives" },
        { key: "applications", icon: "📂", label: "My Applications" }
      ]
    };
  },

  computed: {
    currentLabel() {
      return this.navItems.find(i => i.key === this.activeSection)?.label || "";
    }
  },

  mounted() {
    this.fetchDrives();
    this.fetchProfile();
  },

  methods: {
    logout() { localStorage.clear(); this.$router.push("/"); },

    // ── DRIVES ──
    async fetchDrives() {
      const res = await API.get("/student/drives");
      this.drives = res.data;
    },

    async fetchAppliedDrives() {
      const res = await API.get("/student/placement_history");
      this.appliedDrives = res.data;
    },

    async apply(drive_id) {
      try {
        await API.post("/drive/apply", { drive_id });
        alert("Applied successfully!");
        this.fetchDrives();
      } catch (err) {
        alert(err.response?.data?.message || "Already applied or not eligible");
      }
    },

    async exportApplications() {
      await API.post("/student/export");
      alert("Export started! Check backend exports folder.");
    },

    // ── PROFILE ──
    async fetchProfile() {
      try {
        const res = await API.get("/student/profile");
        const d = res.data;
        this.profile = {
          name:      d.name      || "",
          email:     d.email     || "",
          branch:    d.branch    || "",
          year:      d.year      || "",
          cgpa:      d.cgpa      || "",
          phone:     d.phone     || "",
          skills:    d.skills    || "",
          bio:       d.bio       || "",
          resumeUrl: d.resume_url || null
        };
        // If student already has a resume, show its filename in the preview
        if (d.resume_url) {
          this.resumeFileName = d.resume_url.split("/").pop();
          this.resumeFileSize = "";
        }
      } catch (err) {
        console.error("Failed to load profile", err);
      }
    },

    async saveProfile() {
      try {
        await API.put("/student/profile", {
          name:   this.profile.name,
          email:  this.profile.email,
          branch: this.profile.branch,
          year:   this.profile.year,
          cgpa:   this.profile.cgpa,
          phone:  this.profile.phone,
          skills: this.profile.skills,
          bio:    this.profile.bio
        });
        alert("Profile saved successfully!");
      } catch (err) {
        alert(err.response?.data?.error || "Failed to save profile.");
      }
    },

    // ── RESUME ──
    onResumeSelect(e) {
      const file = e.target.files[0];
      if (file) this.setResumeFile(file);
    },

    onResumeDrop(e) {
      const file = e.dataTransfer.files[0];
      if (file) this.setResumeFile(file);
    },

    setResumeFile(file) {
      this.resumeFile = file;
      this.resumeFileName = file.name;
      this.resumeFileSize = (file.size / 1024).toFixed(1) + " KB";
    },

    removeResume() {
      this.resumeFile = null;
      this.resumeFileName = "";
      this.resumeFileSize = "";
      this.profile.resumeUrl = null;
    },

    viewResume() {
      if (this.profile.resumeUrl) window.open(this.profile.resumeUrl, "_blank");
    },

    async uploadResume() {
      if (!this.resumeFile) return;
      const formData = new FormData();
      formData.append("resume", this.resumeFile);
      try {
        const res = await API.post("/student/upload_resume", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        });
        // Update the stored URL so "View" button works immediately
        this.profile.resumeUrl = res.data.resume_url;
        this.resumeFile = null;   // clear staged file — now showing saved state
        alert("Resume uploaded successfully!");
      } catch (err) {
        alert(err.response?.data?.error || "Upload failed. Please try again.");
      }
    },

    isDeadlineSoon(deadline) {
      const diff = new Date(deadline) - new Date();
      return diff > 0 && diff < 3 * 24 * 60 * 60 * 1000;
    },

    // ── DRIVE SEARCH ──
    onSearchInput() {
      clearTimeout(this.searchTimeout);
      if (!this.searchQuery.trim()) {
        this.showSearchResults = false;
        this.searchResults = [];
        // restore full drive list when query is cleared
        this.fetchDrives();
        return;
      }
      this.searchLoading = true;
      this.showSearchResults = true;
      this.searchTimeout = setTimeout(() => this.runSearch(), 400);
    },

    async runSearch() {
      try {
        const res = await API.get(`/student/search/drives?q=${encodeURIComponent(this.searchQuery)}`);
        this.searchResults = res.data;
      } catch (err) {
        console.error("Search error:", err);
        this.searchResults = [];
      } finally {
        this.searchLoading = false;
      }
    },

    // Clicking a result scrolls the drives table to that drive and highlights it
    selectDrive(drive) {
      this.drives = [drive];          // filter table to just this result
      this.closeSearch();
    },

    clearSearch() {
      this.searchQuery = "";
      this.searchResults = [];
      this.showSearchResults = false;
      this.fetchDrives();             // restore full list
    },

    closeSearch() {
      this.showSearchResults = false;
      this.searchFocused = false;
    },

    handleSearchBlur() {
      // Delay so mousedown on a result fires before blur hides the dropdown
      setTimeout(() => {
        this.searchFocused = false;
        this.showSearchResults = false;
      }, 150);
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.student-shell {
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
.nav-item.active { background: #8b5cf6; color: #fff; }
.nav-icon { font-size: 1rem; width: 20px; text-align: center; }

.sidebar-footer { padding: 16px; border-top: 1px solid #1e293b; }
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

.main-content { margin-left: 220px; flex: 1; display: flex; flex-direction: column; }

.topbar {
  background: #fff;
  padding: 18px 28px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.topbar-left h1 { font-size: 1.3rem; font-weight: 700; color: #0f172a; }
.topbar-subtitle { font-size: 0.8rem; color: #94a3b8; }
.topbar-right { display: flex; align-items: center; gap: 12px; }

.search-wrapper {
  position: relative;
  width: 300px;
}

.search-placeholder {
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
.search-placeholder.active,
.search-placeholder:focus-within {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.1);
  background: #fff;
}
.search-icon { color: #94a3b8; flex-shrink: 0; }
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
.search-spinner { font-size: 0.8rem; flex-shrink: 0; }
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
  max-height: 340px;
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
  background: #8b5cf6;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  flex-shrink: 0;
}
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
}

.btn-export {
  padding: 8px 16px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  color: #166534;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-export:hover { background: #dcfce7; }

.section { padding: 28px; }

/* PROFILE HERO */
.profile-hero {
  display: flex;
  align-items: center;
  gap: 24px;
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);
  border-radius: 16px;
  padding: 28px 32px;
  margin-bottom: 24px;
  color: #fff;
}
.profile-avatar-wrap { position: relative; }
.profile-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(255,255,255,0.15);
  border: 3px solid rgba(255,255,255,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
}
.avatar-online {
  position: absolute;
  bottom: 3px;
  right: 3px;
  width: 14px;
  height: 14px;
  background: #22c55e;
  border-radius: 50%;
  border: 2px solid #312e81;
}
.profile-meta h2 { font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; }
.profile-sub { font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-bottom: 6px; }
.profile-email {
  font-size: 0.82rem;
  background: rgba(255,255,255,0.1);
  padding: 4px 12px;
  border-radius: 20px;
  display: inline-block;
}

.profile-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 20px;
}

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
.card-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px;
  border-bottom: 1px solid #f1f5f9;
  background: #fafbfc;
}
.card-title-text { font-weight: 700; font-size: 0.95rem; color: #0f172a; }
.btn-sm-secondary {
  padding: 6px 14px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
}
.btn-sm-secondary:hover { background: #e2e8f0; }

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  padding: 20px;
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
.form-control:focus { border-color: #8b5cf6; box-shadow: 0 0 0 3px rgba(139,92,246,0.1); }

.btn-primary-action {
  padding: 12px 28px;
  background: #8b5cf6;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-primary-action:hover { background: #7c3aed; }

/* RESUME */
.resume-card { display: flex; flex-direction: column; }
.resume-body { padding: 20px; display: flex; flex-direction: column; gap: 16px; }

.resume-dropzone {
  border: 2px dashed #c4b5fd;
  border-radius: 12px;
  padding: 36px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #faf5ff;
}
.resume-dropzone:hover { border-color: #8b5cf6; background: #f5f3ff; }
.dropzone-icon { font-size: 2.5rem; margin-bottom: 10px; }
.dropzone-label { font-weight: 600; color: #4c1d95; font-size: 0.95rem; margin-bottom: 4px; }
.dropzone-sub { font-size: 0.85rem; color: #6b7280; margin-bottom: 4px; }
.dropzone-link { color: #8b5cf6; text-decoration: underline; cursor: pointer; }
.dropzone-hint { font-size: 0.78rem; color: #9ca3af; }

.resume-preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f5f3ff;
  border: 1px solid #ddd6fe;
  border-radius: 10px;
  padding: 16px;
}
.resume-file-info { display: flex; align-items: center; gap: 12px; }
.resume-file-icon { font-size: 2rem; }
.resume-file-name { font-weight: 600; color: #0f172a; font-size: 0.9rem; }
.resume-file-size { font-size: 0.78rem; color: #94a3b8; }
.resume-actions { display: flex; gap: 8px; }
.resume-upload-btn { width: 100%; }

/* TABLE */
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

.deadline-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.78rem;
  background: #f1f5f9;
  color: #475569;
}
.deadline-soon { background: #fff7ed; color: #c2410c; }

.btn-action {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-apply   { background: #ede9fe; color: #5b21b6; }
.btn-apply:hover { background: #8b5cf6; color: #fff; }
.btn-view    { background: #e0f2fe; color: #0369a1; }
.btn-view:hover { background: #0ea5e9; color: #fff; }
.btn-reject  { background: #fee2e2; color: #991b1b; }
.btn-reject:hover { background: #ef4444; color: #fff; }

.empty-state {
  padding: 48px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.empty-icon { font-size: 2.5rem; }
.empty-state p { color: #94a3b8; font-size: 0.9rem; }
</style>