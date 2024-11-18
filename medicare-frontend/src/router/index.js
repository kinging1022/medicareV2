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
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
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
      component: DashboardView
    },
    {
      path:'/dashboard/profile/update',
      name: 'updateprofile',
      component: UpdateProfileView
    },
    {
      path:'/dashboard/profile/password/update',
      name: 'updatepassword',
      component: UpdatePasswordView
    },
    {
      path:'/dashboard/profile/request-appointment',
      name: 'requestappointment',
      component: RequestAppointment
    },
    {
      path:'/session/:id',
      name: 'startsession',
      component: Session,
    },
  ]
})

export default router
