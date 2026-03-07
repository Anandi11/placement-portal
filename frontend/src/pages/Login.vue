<template>
  <div class="auth-shell">

    <!-- LEFT PANEL -->
    <div class="auth-left">
      <div class="auth-left-inner">
        <div class="brand">
          <span class="brand-icon">🎓</span>
          <span class="brand-name">PlaceIT</span>
        </div>
        <div class="hero-text">
          <h1>Your career<br>starts here.</h1>
          <p>Connect students with top companies through a seamless placement experience.</p>
        </div>
      </div>
      <div class="left-grid"></div>
    </div>

    <!-- RIGHT PANEL -->
    <div class="auth-right">
      <div class="auth-form-wrap">

        <div class="form-header">
          <h2>Welcome back</h2>
          <p>Sign in to your account to continue</p>
        </div>

        <div class="form-body">

          <div class="field-group" :class="{ focused: focusedField === 'email', filled: email }">
            <label>Email address</label>
            <input
              v-model="email"
              type="email"
              placeholder="you@example.com"
              @focus="focusedField = 'email'"
              @blur="focusedField = ''"
            />
          </div>

          <div class="field-group" :class="{ focused: focusedField === 'password', filled: password }">
            <label>Password</label>
            <div class="input-with-toggle">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                @focus="focusedField = 'password'"
                @blur="focusedField = ''"
                @keydown.enter="login"
              />
              <button class="toggle-pw" @click="showPassword = !showPassword" tabindex="-1">
                {{ showPassword ? '🙈' : '👁' }}
              </button>
            </div>
          </div>

          <div v-if="error" class="error-banner">⚠ {{ error }}</div>

          <button class="btn-submit" :class="{ loading }" @click="login" :disabled="loading">
            <span v-if="!loading">Sign In →</span>
            <span v-else class="spinner"></span>
          </button>

        </div>

        <div class="form-footer">
          <p>New here?</p>
          <div class="register-links">
            <router-link to="/register/student" class="reg-link reg-student">
              <span>🎓</span> Register as Student
            </router-link>
            <router-link to="/register/company" class="reg-link reg-company">
              <span>🏢</span> Register as Company
            </router-link>
          </div>
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
      password: "",
      showPassword: false,
      focusedField: "",
      loading: false,
      error: ""
    };
  },

  methods: {
    async login() {
      this.error = "";
      if (!this.email || !this.password) {
        this.error = "Please fill in all fields.";
        return;
      }
      this.loading = true;
      try {
        const res = await API.post("/auth/login", {
          email: this.email,
          password: this.password
        });

        const { role, user_id, access_token, company_id, student_id } = res.data;

        localStorage.setItem("role", role);
        localStorage.setItem("user_id", user_id);
        localStorage.setItem("token", access_token);
        if (company_id) localStorage.setItem("company_id", company_id);
        if (student_id) localStorage.setItem("student_id", student_id);

        if (role === "admin")        this.$router.push("/admin");
        else if (role === "student") this.$router.push("/student");
        else                         this.$router.push("/company");

      } catch (err) {
        this.error = err.response?.data?.message || "Invalid email or password.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.auth-shell {
  display: flex;
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
}

/* ── LEFT PANEL ── */
.auth-left {
  width: 44%;
  background: #0f172a;
  position: relative;
  display: flex;
  align-items: stretch;
  overflow: hidden;
}

/* Dot-grid background */
.left-grid {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(251,191,36,0.15) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
}

/* Glowing orb */
.auth-left::before {
  content: '';
  position: absolute;
  width: 420px;
  height: 420px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(251,191,36,0.18) 0%, transparent 70%);
  bottom: -100px;
  right: -100px;
  pointer-events: none;
}

.auth-left-inner {
  position: relative;
  z-index: 1;
  padding: 52px 48px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 1;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-icon { font-size: 1.6rem; }
.brand-name {
  font-family: 'Syne', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
}

.hero-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px 0 40px;
}
.hero-text h1 {
  font-family: 'Syne', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  color: #fff;
  line-height: 1.1;
  margin-bottom: 20px;
  letter-spacing: -0.03em;
}
.hero-text h1 span { color: #fbbf24; }
.hero-text p {
  font-size: 1rem;
  color: #94a3b8;
  line-height: 1.6;
  max-width: 320px;
}

.stats-row {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 28px 32px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  backdrop-filter: blur(8px);
}
.stat { text-align: center; }
.stat-n {
  display: block;
  font-family: 'Syne', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: #fbbf24;
}
.stat-l {
  display: block;
  font-size: 0.78rem;
  color: #64748b;
  margin-top: 2px;
  font-weight: 500;
}
.stat-divider {
  width: 1px;
  height: 36px;
  background: rgba(255,255,255,0.1);
}

/* ── RIGHT PANEL ── */
.auth-right {
  flex: 1;
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
}

.auth-form-wrap {
  width: 100%;
  max-width: 400px;
}

.form-header {
  margin-bottom: 36px;
}
.form-header h2 {
  font-family: 'Syne', sans-serif;
  font-size: 1.9rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.03em;
  margin-bottom: 6px;
}
.form-header p {
  color: #64748b;
  font-size: 0.9rem;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-bottom: 32px;
}

/* Field group */
.field-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}
.field-group label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #475569;
  transition: color 0.15s;
}
.field-group.focused label { color: #0f172a; }

.field-group input {
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 0.95rem;
  color: #0f172a;
  background: #fff;
  outline: none;
  transition: border 0.15s, box-shadow 0.15s;
  font-family: inherit;
  width: 100%;
}
.field-group input:focus {
  border-color: #0f172a;
  box-shadow: 0 0 0 3px rgba(15,23,42,0.08);
}
.field-group input::placeholder { color: #cbd5e1; }

.input-with-toggle {
  position: relative;
}
.input-with-toggle input { padding-right: 48px; }
.toggle-pw {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 4px;
  color: #94a3b8;
}

/* Error */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.85rem;
  color: #dc2626;
  font-weight: 500;
}

/* Submit button */
.btn-submit {
  width: 100%;
  padding: 14px;
  background: #0f172a;
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Syne', sans-serif;
  letter-spacing: 0.01em;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 50px;
}
.btn-submit:hover:not(:disabled) {
  background: #1e293b;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(15,23,42,0.2);
}
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Footer */
.form-footer p {
  font-size: 0.85rem;
  color: #94a3b8;
  margin-bottom: 12px;
  font-weight: 500;
}
.register-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.reg-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.15s;
  border: 1.5px solid #e2e8f0;
}
.reg-student {
  color: #5b21b6;
  background: #faf5ff;
  border-color: #ddd6fe;
}
.reg-student:hover { background: #ede9fe; border-color: #c4b5fd; }
.reg-company {
  color: #0369a1;
  background: #f0f9ff;
  border-color: #bae6fd;
}
.reg-company:hover { background: #e0f2fe; border-color: #7dd3fc; }

/* Responsive */
@media (max-width: 768px) {
  .auth-shell { flex-direction: column; }
  .auth-left { width: 100%; min-height: 220px; }
  .auth-left-inner { padding: 32px 28px; }
  .hero-text { padding: 24px 0 20px; }
  .hero-text h1 { font-size: 2rem; }
  .stats-row { gap: 16px; padding: 20px 24px; }
}
</style>