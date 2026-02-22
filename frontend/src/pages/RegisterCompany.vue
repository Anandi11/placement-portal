<template>
  <div class="container mt-5">
    <h2>Company Registration</h2>

    <input v-model="name" placeholder="HR Name" class="form-control mb-2" />
    <input v-model="email" placeholder="Email" class="form-control mb-2" />
    <input v-model="password" type="password" placeholder="Password" class="form-control mb-2" />
    <input v-model="company_name" placeholder="Company Name" class="form-control mb-2" />
    <input v-model="hr_contact" placeholder="Contact" class="form-control mb-2" />
    <input v-model="website" placeholder="Website" class="form-control mb-2" />

    <button @click="register" class="btn btn-success">Register</button>
  </div>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return { name:"", email:"", password:"", company_name:"", hr_contact:"", website:"" };
  },
  methods: {
    async register() {
      await API.post("/auth/register/company", this.$data);
      alert("Company registered");
      this.$router.push("/");
    }
  }
};
</script>
