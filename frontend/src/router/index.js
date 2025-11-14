import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/login.vue'
import DefaultLayout from '../pages/defaultLayout.vue'
import Dashboard from '../pages/dashboard.vue'
import ManageUsers from '../pages/manage_users.vue'
import UpdateProfile from '../pages/updateProfile.vue'
import TaskPerUser from '../pages/task_per_user.vue'
import Projects from '../pages/projects.vue'


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
        component: Dashboard,
        meta: { requiresAuth  : true, role: 'admin' }
      },
      {
        path: 'manage-users',
        name: 'ManageUsers',
        component: ManageUsers,
        meta: { requiresAuth  : true, role: 'admin' }

      },
      {
        path: 'update-profile',
        name: 'UpdateProfile',
        component: UpdateProfile,
        meta: { requiresAuth  : true  }
      },
      {
        path: 'task-per-user',
        name: 'TaskPerUser',
        component: TaskPerUser,
        meta: { requiresAuth  : true} 
      },
      {
        path: 'projects',
        name: 'Projects',
        component: Projects,
        meta: { requiresAuth  : true,}
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('loggedIn') === 'true'
  const userType = localStorage.getItem('user_type')

  // If route requires login
  if (to.meta.requiresAuth && !loggedIn) {
    next({ name: 'Login' })
  } 
  // If route has a specific role restriction
  else if (to.meta.role && to.meta.role !== userType) {
    // Redirect based on actual user type
    if (userType === 'admin') {
      next({ name: 'Dashboard' })
    } else if (userType === 'staff') {
      next({ name: 'TaskPerUser' })
    } else {
      next({ name: 'Login' })
    }
  } 
  else {
    next()
  }
})

export default router