<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Student Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>
      <button class="btn btn-warning mb-3"
          @click="exportApplications">
          Export My Applications (CSV)
  </button>

    <!-- Available Drives -->
    <div class="card shadow-sm">
      <div class="card-header bg-primary text-white">
        Available Placement Drives
      </div>

      <div class="card-body">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Job</th>
              <th>Company</th>
              <th>Deadline</th>
              <th>Apply</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td>{{ d.job_title }}</td>
              <td>{{ d.company }}</td>
              <td>{{ d.deadline }}</td>

              <td>
                <button class="btn btn-success btn-sm"
                  @click="apply(d.id)">
                  Apply
                </button>
              </td>

            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Applied Drives -->
    <div class="card shadow-sm mt-4">
      <div class="card-header bg-secondary text-white d-flex justify-content-between">
        <span>Applied Drives</span>
        <button class="btn btn-light btn-sm" @click="fetchAppliedDrives">
          View Applied Drives
        </button>
      </div>

      <div class="card-body" v-if="appliedDrives.length">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Drive</th>
              <th>Company</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="a in appliedDrives" :key="a.id">
              <td>{{ a.drive }}</td>
              <td>{{ a.company }}</td>
              <td>{{ a.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="card-body text-center" v-else>
        <p>No applications yet.</p>
      </div>
    </div>

  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      drives: [],
      appliedDrives: []
    };
  },

  mounted() {
    this.fetchDrives();
  },

  methods: {

    logout() {
      localStorage.clear();
      this.$router.push("/");
    },

    async fetchDrives() {
      const res = await API.get("/student/drives");
      this.drives = res.data;
    },

    async exportApplications() {
      await API.post(`/student/export`);
      alert("Export started! Check backend exports folder.");
    },

    async apply(drive_id) {
      try {
        await API.post("/drive/apply", {
          drive_id: drive_id
        });

        alert("Applied successfully!");
      } catch (err) {
        alert(err.response?.data?.message || "Already applied or not eligible");
      }
    },

    async fetchAppliedDrives() {
      const res = await API.get(`/student/placement_history`);
      this.appliedDrives = res.data;
    }

  }
};
</script>

<style>
.card {
  border-radius: 10px;
}
</style>