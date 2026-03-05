<template>
  <div class="login-wrapper d-flex align-items-center justify-content-center">
    <div class="card login-card shadow-lg">
      <div class="card-body p-4">

        <div class="text-center mb-4">
          <h3 class="fw-bold">Placement Portal</h3>
          <p class="text-muted mb-0">Login to continue</p>
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="email" class="form-control form-control-lg" placeholder="Enter your email" />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control form-control-lg" placeholder="Enter your password" />
        </div>

        <button @click="login" class="btn btn-dark w-100 btn-lg">
          Login
        </button>

        <div class="text-center mt-4">
          <small class="text-muted">
            Student? <router-link to="/register/student">Register</router-link><br>
            Company? <router-link to="/register/company">Register</router-link>
          </small>
        </div>

      </div>
    </div>
  </div>
</template>
<script>
import API from "../services/api";

export default {
  data() {
    return {
      email: "",
      password: ""
    };
  },

  methods: {

    async login() {
      try {
        const res = await API.post("/auth/login", {
          email: this.email,
          password: this.password
        });

        const role = res.data.role;
        const user_id = res.data.user_id;

        localStorage.setItem("role", role);
        localStorage.setItem("user_id", user_id);
        localStorage.setItem("token", res.data.access_token);
        if (res.data.company_id)
          localStorage.setItem("company_id", res.data.company_id);

        if (res.data.student_id)
          localStorage.setItem("student_id", res.data.student_id);

        if (role === "admin") this.$router.push("/admin");
        else if (role === "student") this.$router.push("/student");
        else this.$router.push("/company");

      } catch (err) {
        alert("Login failed");
      }
    }
  }
};
</script>
