<template>
  <div class="container mt-5">
    <h2>Student Registration</h2>

    <input v-model="name" placeholder="Name" class="form-control mb-2" />
    <input v-model="email" placeholder="Email" class="form-control mb-2" />
    <input v-model="password" type="password" placeholder="Password" class="form-control mb-2" />
    <input v-model="branch" placeholder="Branch" class="form-control mb-2" />
    <input v-model="cgpa" placeholder="CGPA" class="form-control mb-2" />
    <input v-model="year" placeholder="Year" class="form-control mb-2" />

    <button @click="register" class="btn btn-success">Register</button>
  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return { name:"", email:"", password:"", branch:"", cgpa:"", year:"" };
  },
  methods: {
    async register() {
      await API.post("/auth/register/student", this.$data);
      alert("Registered successfully");
      this.$router.push("/");
    }
  }
};
</script>
