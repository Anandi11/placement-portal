<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Student Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <!-- Drives -->
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

  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      student_id: localStorage.getItem("user_id"),
      drives: []
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

    async apply(drive_id) {
      try {
        await API.post("/drive/apply", {
          student_id: this.student_id,
          drive_id: drive_id
        });

        alert("Applied successfully!");

      } catch (err) {
        alert(err.response?.data?.message || "Already applied or not eligible");
      }
    }

  }
};
</script>

<style>
.card {
  border-radius: 10px;
}
</style>
