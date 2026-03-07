<template>
  <div class="auth-shell">

    <!-- LEFT PANEL -->
    <div class="auth-left">
      <div class="auth-left-inner">
        <router-link to="/" class="brand">
          <span class="brand-icon">🎓</span>
          <span class="brand-name">PlaceIT</span>
        </router-link>
        <div class="hero-text">
          <div class="role-chip">🏢 Company</div>
          <h1>Hire the best talent on campus</h1>
          <p>Post placement drives, review applications, and build your team from top graduating students.</p>
        </div>
        <div class="perks">
          <div class="perk" v-for="p in perks" :key="p.text">
            <span class="perk-icon">{{ p.icon }}</span>
            <span>{{ p.text }}</span>
          </div>
        </div>
      </div>
      <div class="left-grid"></div>
    </div>

    <!-- RIGHT PANEL -->
    <div class="auth-right">
      <div class="auth-form-wrap">

        <div class="form-header">
          <h2>Company registration</h2>
          <p>Fill in your company details — pending admin approval after signup</p>
        </div>

        <!-- STEP INDICATOR -->
        <div class="steps">
          <div class="step" :class="{ active: step === 1, done: step > 1 }">
            <div class="step-dot">{{ step > 1 ? '✓' : '1' }}</div>
            <span>Account</span>
          </div>
          <div class="step-line" :class="{ done: step > 1 }"></div>
          <div class="step" :class="{ active: step === 2 }">
            <div class="step-dot">2</div>
            <span>Company</span>
          </div>
        </div>

        <div class="form-body">

          <!-- STEP 1: Account details -->
          <template v-if="step === 1">
            <div class="field-row">
              <div class="field-group" :class="{ focused: focusedField === 'name' }">
                <label>HR / Contact Name</label>
                <input v-model="name" placeholder="Jane Smith"
                  @focus="focusedField='name'" @blur="focusedField=''" />
              </div>
              <div class="field-group" :class="{ focused: focusedField === 'email' }">
                <label>Work Email</label>
                <input v-model="email" type="email" placeholder="hr@company.com"
                  @focus="focusedField='email'" @blur="focusedField=''" />
              </div>
            </div>

            <div class="field-group" :class="{ focused: focusedField === 'password' }">
              <label>Password</label>
              <div class="input-with-toggle">
                <input v-model="password" :type="showPassword ? 'text' : 'password'"
                  placeholder="Min. 8 characters"
                  @focus="focusedField='password'" @blur="focusedField=''"
                  @keydown.enter="nextStep" />
                <button class="toggle-pw" @click="showPassword = !showPassword" tabindex="-1">
                  {{ showPassword ? '🙈' : '👁' }}
                </button>
              </div>
            </div>

            <div v-if="error" class="error-banner">⚠ {{ error }}</div>

            <button class="btn-submit" @click="nextStep">
              Continue →
            </button>
          </template>

          <!-- STEP 2: Company details -->
          <template v-if="step === 2">
            <div class="field-group" :class="{ focused: focusedField === 'company_name' }">
              <label>Company Name</label>
              <input v-model="company_name" placeholder="Acme Corporation"
                @focus="focusedField='company_name'" @blur="focusedField=''" />
            </div>

            <div class="field-row">
              <div class="field-group" :class="{ focused: focusedField === 'hr_contact' }">
                <label>HR Contact Number</label>
                <input v-model="hr_contact" placeholder="+91 98765 43210"
                  @focus="focusedField='hr_contact'" @blur="focusedField=''" />
              </div>
              <div class="field-group" :class="{ focused: focusedField === 'website' }">
                <label>Website</label>
                <input v-model="website" placeholder="https://acme.com"
                  @focus="focusedField='website'" @blur="focusedField=''"
                  @keydown.enter="register" />
              </div>
            </div>

            <div class="approval-note">
              <span class="note-icon">ℹ</span>
              Your account will be reviewed by the placement admin before activation. You'll be notified once approved.
            </div>

            <div v-if="error" class="error-banner">⚠ {{ error }}</div>
            <div v-if="success" class="success-banner">✓ {{ success }}</div>

            <div class="btn-row">
              <button class="btn-back" @click="step = 1">← Back</button>
              <button class="btn-submit" :class="{ loading }" @click="register" :disabled="loading">
                <span v-if="!loading">Register Company →</span>
                <span v-else class="spinner"></span>
              </button>
            </div>
          </template>

        </div>

        <div class="form-footer">
          Already have an account?
          <router-link to="/" class="link-login">Sign in</router-link>
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
      step: 1,
      name: "", email: "", password: "",
      company_name: "", hr_contact: "", website: "",
      showPassword: false,
      focusedField: "",
      loading: false,
      error: "",
      success: "",
      perks: [
        { icon: "📋", text: "Post targeted placement drives" },
        { icon: "👥", text: "Review and shortlist applicants" },
        { icon: "✅", text: "Select candidates directly" },
        { icon: "🔔", text: "Managed by placement admin" }
      ]
    };
  },

  methods: {
    nextStep() {
      this.error = "";
      if (!this.name || !this.email || !this.password) {
        this.error = "Please fill in all fields.";
        return;
      }
      if (this.password.length < 8) {
        this.error = "Password must be at least 8 characters.";
        return;
      }
      this.step = 2;
    },

    async register() {
      this.error = "";
      this.success = "";
      if (!this.company_name || !this.hr_contact) {
        this.error = "Please fill in all company details.";
        return;
      }
      this.loading = true;
      try {
        await API.post("/auth/register/company", {
          name: this.name, email: this.email, password: this.password,
          company_name: this.company_name,
          hr_contact: this.hr_contact,
          website: this.website
        });
        this.success = "Registered! Awaiting admin approval. Redirecting…";
        setTimeout(() => this.$router.push("/"), 2000);
      } catch (err) {
        this.error = err.response?.data?.message || "Registration failed. Please try again.";
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

/* ── LEFT ── */
.auth-left {
  width: 40%;
  background: #0f172a;
  position: relative;
  display: flex;
  overflow: hidden;
}
.left-grid {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(14,165,233,0.15) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
}
.auth-left::before {
  content: '';
  position: absolute;
  width: 380px; height: 380px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(14,165,233,0.18) 0%, transparent 70%);
  bottom: -80px; right: -80px;
  pointer-events: none;
}

.auth-left-inner {
  position: relative;
  z-index: 1;
  padding: 52px 44px;
  display: flex;
  flex-direction: column;
  gap: 40px;
  flex: 1;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.brand-icon { font-size: 1.5rem; }
.brand-name {
  font-family: 'Syne', sans-serif;
  font-size: 1.3rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
}

.role-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(14,165,233,0.15);
  border: 1px solid rgba(14,165,233,0.35);
  color: #7dd3fc;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 5px 12px;
  border-radius: 20px;
  margin-bottom: 16px;
}

.hero-text { flex: 1; }
.hero-text h1 {
  font-family: 'Syne', sans-serif;
  font-size: 2.1rem;
  font-weight: 800;
  color: #fff;
  line-height: 1.2;
  margin-bottom: 14px;
  letter-spacing: -0.03em;
}
.hero-text p {
  font-size: 0.9rem;
  color: #64748b;
  line-height: 1.65;
}

.perks { display: flex; flex-direction: column; gap: 12px; }
.perk {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.875rem;
  color: #94a3b8;
  font-weight: 500;
}
.perk-icon {
  width: 32px; height: 32px;
  border-radius: 8px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  flex-shrink: 0;
}

/* ── RIGHT ── */
.auth-right {
  flex: 1;
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  overflow-y: auto;
}

.auth-form-wrap { width: 100%; max-width: 440px; }

.form-header { margin-bottom: 24px; }
.form-header h2 {
  font-family: 'Syne', sans-serif;
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.03em;
  margin-bottom: 6px;
}
.form-header p { color: #64748b; font-size: 0.875rem; line-height: 1.5; }

/* Steps */
.steps {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 28px;
}
.step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #94a3b8;
}
.step.active { color: #0f172a; }
.step.done { color: #059669; }
.step-dot {
  width: 28px; height: 28px;
  border-radius: 50%;
  border: 2px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  background: #fff;
  color: #94a3b8;
  transition: all 0.2s;
}
.step.active .step-dot { border-color: #0ea5e9; color: #0ea5e9; }
.step.done .step-dot { border-color: #059669; background: #059669; color: #fff; }
.step-line {
  flex: 1;
  height: 2px;
  background: #e2e8f0;
  margin: 0 10px;
  transition: background 0.2s;
}
.step-line.done { background: #059669; }

.form-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 28px;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.field-group { display: flex; flex-direction: column; gap: 6px; }
.field-group label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
  transition: color 0.15s;
}
.field-group.focused label { color: #0f172a; }
.field-group input {
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  padding: 11px 14px;
  font-size: 0.9rem;
  color: #0f172a;
  background: #fff;
  outline: none;
  transition: border 0.15s, box-shadow 0.15s;
  font-family: inherit;
  width: 100%;
}
.field-group input:focus {
  border-color: #0ea5e9;
  box-shadow: 0 0 0 3px rgba(14,165,233,0.1);
}
.field-group input::placeholder { color: #cbd5e1; }

.input-with-toggle { position: relative; }
.input-with-toggle input { padding-right: 44px; }
.toggle-pw {
  position: absolute;
  right: 12px; top: 50%;
  transform: translateY(-50%);
  background: none; border: none;
  cursor: pointer; font-size: 1rem; color: #94a3b8; padding: 4px;
}

.approval-note {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 0.82rem;
  color: #92400e;
  line-height: 1.5;
}
.note-icon { font-style: normal; font-size: 1rem; flex-shrink: 0; margin-top: 1px; }

.error-banner {
  background: #fef2f2; border: 1px solid #fecaca;
  border-radius: 8px; padding: 10px 14px;
  font-size: 0.85rem; color: #dc2626; font-weight: 500;
}
.success-banner {
  background: #f0fdf4; border: 1px solid #bbf7d0;
  border-radius: 8px; padding: 10px 14px;
  font-size: 0.85rem; color: #166534; font-weight: 500;
}

.btn-row { display: flex; gap: 12px; }
.btn-back {
  padding: 13px 20px;
  background: #fff;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  color: #475569;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.15s;
  white-space: nowrap;
}
.btn-back:hover { background: #f1f5f9; }

.btn-submit {
  flex: 1;
  padding: 13px;
  background: #0ea5e9;
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Syne', sans-serif;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  width: 100%;
}
.btn-submit:hover:not(:disabled) {
  background: #0284c7;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(14,165,233,0.3);
}
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

.form-footer {
  text-align: center;
  font-size: 0.85rem;
  color: #94a3b8;
}
.link-login {
  color: #0ea5e9;
  font-weight: 600;
  text-decoration: none;
  margin-left: 4px;
}
.link-login:hover { text-decoration: underline; }

@media (max-width: 768px) {
  .auth-shell { flex-direction: column; }
  .auth-left { width: 100%; min-height: 200px; }
  .auth-left-inner { padding: 28px 24px; gap: 20px; }
  .hero-text h1 { font-size: 1.6rem; }
  .field-row { grid-template-columns: 1fr; }
}
</style>