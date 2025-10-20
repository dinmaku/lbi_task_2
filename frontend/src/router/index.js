import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/login.vue'
import DefaultLayout from '../pages/defaultLayout.vue'
import Dashboard from '../pages/dashboard.vue'
import ManageUsers from '../pages/manage_users.vue'
import UpdateProfile from '../pages/updateProfile.vue'
import TaskPerUser from '../pages/task_per_user.vue'


const routes = [
  { 
    path: '/', 
    name: 'Login', 
    component: Login 
  },
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'manage-users',
        name: 'ManageUsers',
        component: ManageUsers
      },
      {
        path: 'update-profile',
        name: 'UpdateProfile',
        component: UpdateProfile
      },
      {
        path: 'task-per-user',
        name: 'TaskPerUser',
        component: TaskPerUser
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router