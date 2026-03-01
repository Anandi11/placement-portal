<template>
  <div class="container mt-5">
    <h2>Login</h2>

    <input v-model="email" placeholder="Email" class="form-control mb-2" />
    <input v-model="password" type="password" placeholder="Password" class="form-control mb-2" />

    <button @click="login" class="btn btn-primary">Login</button>

    <p class="mt-3">
      Student? <router-link to="/register/student">Register</router-link><br>
      Company? <router-link to="/register/company">Register</router-link>
    </p>
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
