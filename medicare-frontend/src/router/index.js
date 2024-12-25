import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import ActivateUserView from '@/views/ActivateUserView.vue'
import ActivationSuccesView from '@/views/ActivationSuccesView.vue'
import DashboardView from '@/views/DashboardView.vue'
import UpdateProfileView from '@/views/UpdateProfileView.vue'
import UpdatePasswordView from '@/views/UpdatePasswordView.vue'
import RequestAppointment from '@/views/RequestAppointment.vue'
import Session from '@/views/Session.vue'
import NotificationView from '@/views/NotificationView.vue'
import CreditView from '@/views/CreditView.vue'
import SessionHistory from '@/views/SessionHistory.vue'
import RequestPasswordReset from '@/views/RequestPasswordReset.vue'
import ForgotPassword from '@/views/ForgotPassword.vue'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
      meta: { guestOnly: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true }
    },
    {
      path: '/auth/activate/:uid/:token',
      name: 'Activate',
      component: ActivateUserView
    },
    {
      path:'/activation/success',
      name: 'activationsuccessful',
      component: ActivationSuccesView
    },
    {
      path:'/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path:'/dashboard/profile/update',
      name: 'updateprofile',
      component: UpdateProfileView,
      meta: { requiresAuth: true }
    },
    {
      path:'/dashboard/profile/password/update',
      name: 'updatepassword',
      component: UpdatePasswordView,
      meta: { requiresAuth: true }
    },
    {
      path:'/dashboard/profile/request-appointment',
      name: 'requestappointment',
      component: RequestAppointment,
      meta: { requiresAuth: true }
    },
    {
      path:'/session/:id',
      name: 'startsession',
      component: Session,
      meta: { requiresAuth: true, hideHeaderFooter: true }
    },
    {
      path:'/notification',
      name: 'notification',
      component: NotificationView,
      meta: { requiresAuth: true }
    },
    {
      path:'/buy-credit',
      name: 'credit',
      component: CreditView,
      meta: { requiresAuth: true }
    },
    {
      path:'/session-history/:id',
      name: 'session-history',
      component: SessionHistory,
      meta: { requiresAuth: true, hideHeaderFooter: true }
    },
    {
      path:'/password/reset/',
      name: 'password-reset',
      component: RequestPasswordReset,
     
    },
    {
      path:'/password/reset/confirm/:uid/:token',
      name: 'forgot-password',
      component: ForgotPassword,
     
    },
  ]
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = userStore.user.isAuthenticated

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.guestOnly && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router