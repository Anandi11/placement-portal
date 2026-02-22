<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Admin Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <!-- QUICK ACTIONS -->
    <div class="card mb-4 shadow-sm">
      <div class="card-header bg-dark text-white">Quick Admin Actions</div>
      <div class="card-body d-flex gap-3 flex-wrap">

        <button class="btn btn-primary" @click="scrollTo('companies')">
          Manage Companies
        </button>

        <button class="btn btn-primary" @click="scrollTo('drives')">
          Manage Drives
        </button>

        <button class="btn btn-primary" @click="scrollTo('students')">
          Manage Students
        </button>

        <button class="btn btn-primary" @click="scrollTo('applications')">
          View Applications
        </button>

        <button class="btn btn-success" @click="loadPlacementReport">
          View Placement Report
        </button>

      </div>
    </div>

    <!-- STATS -->
    <div class="row mb-4">
      <div class="col-md-3" v-for="card in statsCards" :key="card.title">
        <div class="card text-center shadow-sm">
          <div class="card-body">
            <h5>{{ card.title }}</h5>
            <h3 class="text-primary">{{ card.value }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- PLACEMENT REPORT -->
    <div v-if="report" class="card mb-4 shadow-sm">
      <div class="card-header bg-success text-white">
        Placement Report Overview
      </div>

      <div class="card-body">
        <p><b>Total Drives:</b> {{ report.total_drives }}</p>
        <p><b>Total Applications:</b> {{ report.applications }}</p>
        <p><b>Total Selected:</b> {{ report.selected }}</p>

        <h5 class="mt-3">Company-wise Selections</h5>
        <ul>
          <li v-for="c in report.company_wise" :key="c.company">
            {{ c.company }} — {{ c.selections }}
          </li>
        </ul>
      </div>
    </div>

    <!-- COMPANIES -->
    <div id="companies" class="card mb-4 shadow-sm">
      <div class="card-header bg-dark text-white">Companies</div>
      <div class="card-body">

        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Name</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="c in companies" :key="c.id">
              <td>{{ c.company_name }}</td>

              <td>
                <span class="badge"
                  :class="{
                    'bg-warning': c.approval_status === 'Pending',
                    'bg-success': c.approval_status === 'Approved',
                    'bg-danger': c.approval_status === 'Rejected'
                  }">
                  {{ c.approval_status }}
                </span>
              </td>

              <td>
                <button
                  class="btn btn-sm btn-success me-2"
                  :disabled="c.approval_status === 'Approved'"
                  @click="approveCompany(c.id)"
                >
                  Approve
                </button>

                <button
                  class="btn btn-sm btn-danger"
                  :disabled="c.approval_status === 'Rejected'"
                  @click="rejectCompany(c.id)"
                >
                  Reject
                </button>
              </td>
            </tr>
          </tbody>

        </table>

      </div>
    </div>

    <!-- DRIVES -->
    <div id="drives" class="card mb-4 shadow-sm">
      <div class="card-header bg-primary text-white">Placement Drives</div>

      <div class="card-body">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Job</th>
              <th>Company</th>
              <th>Status</th>
              <th>Approve</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td>{{ d.job_title }}</td>
              <td>{{ d.company }}</td>
              <td>{{ d.status }}</td>

              <td>
                <button
                  class="btn btn-success btn-sm"
                  :disabled="d.status === 'Approved'"
                  @click="approveDrive(d.id)"
                >
                  {{ d.status === 'Approved' ? 'Approved' : 'Approve' }}
                </button>
              </td>

            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- STUDENTS -->
    <div id="students" class="card mb-4 shadow-sm">
      <div class="card-header bg-secondary text-white">Students</div>

      <div class="card-body">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="s in students" :key="s.id">
              <td>{{ s.name }}</td>
              <td>{{ s.email }}</td>

              <td>
                <button
                  class="btn btn-danger btn-sm"
                  :disabled="!s.active"
                  @click="blacklistUser(s.id)"
                >
                  {{ s.active ? 'Blacklist' : 'Blacklisted' }}
                </button>
              </td>

            </tr>
          </tbody>

        </table>
      </div>
    </div>

    <!-- APPLICATIONS -->
    <div id="applications" class="card shadow-sm">
      <div class="card-header bg-info text-white">Applications</div>

      <div class="card-body">
        <table class="table table-bordered">
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
              <td>{{ a.status }}</td>
            </tr>
          </tbody>

        </table>
      </div>
    </div>

  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      statsCards: [],
      companies: [],
      drives: [],
      students: [],
      applications: [],
      report: null
    };
  },

  mounted() {
    this.loadDashboard();
  },

  methods: {

    logout() {
      this.$router.push("/");
    },

    scrollTo(section) {
      document.getElementById(section).scrollIntoView({ behavior: "smooth" });
    },

    async loadDashboard() {
      const stats = await API.get("/admin/dashboard");

      this.statsCards = [
        { title: "Students", value: stats.data.students },
        { title: "Companies", value: stats.data.companies },
        { title: "Drives", value: stats.data.drives },
        { title: "Applications", value: stats.data.applications }
      ];

      this.companies = (await API.get("/admin/companies")).data;
      this.drives = (await API.get("/admin/drives")).data;
      this.students = (await API.get("/admin/students")).data;
      this.applications = (await API.get("/admin/applications")).data;
    },

    async loadPlacementReport() {
      const res = await API.get("/admin/placement_report");
      this.report = res.data;
    },

    async approveCompany(id) {
      await API.put(`/admin/approve/company/${id}`);
      this.loadDashboard();
    },

    async rejectCompany(id) {
      await API.put(`/admin/reject/company/${id}`);
      this.loadDashboard();
    },

    async approveDrive(id) {
      await API.put(`/admin/approve/drive/${id}`);
      this.loadDashboard();
    },

    async blacklistUser(id) {
      await API.put(`/admin/blacklist/${id}`);
      this.loadDashboard();
    }

  }
};
</script>

<style>
.card {
  border-radius: 10px;
}

.card-header {
  font-weight: bold;
}

table {
  background: white;
}
</style>
