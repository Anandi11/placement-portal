import { createRouter, createWebHistory } from 'vue-router'

import Login from '../pages/Login.vue'
import RegisterStudent from '../pages/RegisterStudent.vue'
import RegisterCompany from '../pages/RegisterCompany.vue'
import AdminDashboard from '../pages/AdminDashboard.vue'
import StudentDashboard from '../pages/StudentDashboard.vue'
import CompanyDashboard from '../pages/CompanyDashboard.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/register/student', component: RegisterStudent },
  { path: '/register/company', component: RegisterCompany },
  { path: '/admin', component: AdminDashboard },
  { path: '/student', component: StudentDashboard },
  { path: '/company', component: CompanyDashboard },
]

export default createRouter({
  history: createWebHistory(),
  routes
})
