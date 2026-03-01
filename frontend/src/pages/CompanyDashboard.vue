<template>
  <div class="container mt-4">

    <!-- HEADER -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Company Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <!-- CREATE DRIVE -->
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-primary text-white">Create Placement Drive</div>

      <div class="card-body">

        <div class="row">
          <div class="col-md-6 mb-2">
            <input v-model="form.job_title" class="form-control" placeholder="Job Title">
          </div>

          <div class="col-md-6 mb-2">
            <input v-model="form.deadline" type="date" class="form-control">
          </div>

          <div class="col-md-12 mb-2">
            <textarea v-model="form.job_description" class="form-control" placeholder="Job Description"></textarea>
          </div>

          <div class="col-md-4 mb-2">
            <input v-model="form.branch" class="form-control" placeholder="Branches (CSE,IT,CSM)">
          </div>

          <div class="col-md-4 mb-2">
            <input v-model="form.cgpa" class="form-control" placeholder="Min CGPA">
          </div>

          <div class="col-md-4 mb-2">
            <input v-model="form.year" class="form-control" placeholder="Year">
          </div>
        </div>

        <button class="btn btn-success mt-3" @click="createDrive">
          Create Drive
        </button>

      </div>
    </div>

    <!-- DRIVES LIST -->
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-dark text-white">Your Drives</div>

      <div class="card-body">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Job</th>
              <th>Status</th>
              <th>Applicants</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td>{{ d.id }}</td>
              <td>{{ d.job_title }}</td>
              <td>{{ d.status }}</td>

              <td>
                <button class="btn btn-info btn-sm"
                  @click="loadApplicants(d.id)">
                  View Applicants
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- APPLICANTS -->
    <div v-if="applicants.length" class="card shadow-sm">
      <div class="card-header bg-secondary text-white">
        Applicants for Selected Drive
      </div>

      <div class="card-body">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Student</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="a in applicants" :key="a.application_id">
              <td>{{ a.student_name }}</td>
              <td>{{ a.status }}</td>

              <td>

                <button class="btn btn-warning btn-sm me-2"
                  @click="updateStatus(a.application_id, 'Shortlisted')">
                  Shortlist
                </button>

                <button class="btn btn-success btn-sm me-2"
                  @click="updateStatus(a.application_id, 'Selected')">
                  Select
                </button>

                <button class="btn btn-danger btn-sm"
                  @click="updateStatus(a.application_id, 'Rejected')">
                  Reject
                </button>

              </td>

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
      drives: [],
      applicants: [],
      selectedDrive: null,

      form: {
        job_title: "",
        job_description: "",
        branch: "",
        cgpa: "",
        year: "",
        deadline: ""
      }
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

    async createDrive() {
      await API.post("/company/create_drive", {
        ...this.form
      });

      alert("Drive created!");
      this.fetchDrives();
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
      await API.put(`/company/application/update/${app_id}`, {
        status: status
      });

      alert("Status updated");
      this.loadApplicants(this.selectedDrive);
    }

  }
};
</script>

<style>
.card {
  border-radius: 10px;
}
</style>
