<template>
  <div class="bg-gray-100 py-4 px-3 sm:px-4">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-blue-400 to-blue-500 p-4">
          <div class="flex items-center">
            <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center text-xl font-bold text-blue-600 shadow mr-4">
              {{ initials }}
            </div>
            <div>
              <h1 class="text-xl font-bold text-white">{{ userStore.user.role === 'doctor' ? 'Dr. ' : '' }}{{ userStore.user.first_name }} {{ userStore.user.last_name }}</h1>
              <p class="text-blue-100 text-sm">
                {{ userStore.user.display_age }} years old • {{ userStore.user.gender }}
              </p>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="p-4">
          <!-- Credits Card -->
          <div v-if="userStore.user.role === 'patient'" class="bg-gradient-to-br from-green-400 to-blue-500 rounded-lg shadow p-4 mb-4 transform transition-all duration-300 hover:scale-102">
            <h3 class="text-base font-semibold mb-2 text-white">Your Credits</h3>
            <div v-if="!emptyCredit && userCredits.total_credits !== undefined" class="flex items-center">
              <div class="w-12 h-12 bg-white bg-opacity-30 rounded-full flex items-center justify-center mr-3">
                <CreditCard class="h-6 w-6 text-white" />
              </div>
              <div>
                <p class="text-2xl font-bold text-white">{{ userCredits.total_credits }}</p>
                <p class="text-xs text-blue-100">Total Credits</p>
              </div>
            </div>
            <p v-else-if="emptyCredit" class="text-white text-sm">No credits available.</p>
            <p v-else class="text-white text-sm">Loading credit information...</p>
          </div>

          <!-- Personal Information Grid -->
          <div class="grid grid-cols-2 gap-3 mb-4">
            <div v-if="userStore.user.blood_type" class="bg-white p-3 rounded-lg shadow transition-all duration-300 hover:shadow-md">
              <Heart class="h-5 w-5 text-red-500 mb-1" />
              <p class="text-xs text-gray-500">Blood Type</p>
              <p class="font-semibold text-sm">{{ userStore.user.blood_type }}</p>
            </div>
            <div v-if="userStore.user.height" class="bg-white p-3 rounded-lg shadow transition-all duration-300 hover:shadow-md">
              <Ruler class="h-5 w-5 text-blue-500 mb-1" />
              <p class="text-xs text-gray-500">Height</p>
              <p class="font-semibold text-sm">{{ displayHeight }}</p>
            </div>
            <div v-if="userStore.user.weight" class="bg-white p-3 rounded-lg shadow transition-all duration-300 hover:shadow-md">
              <Scale class="h-5 w-5 text-green-500 mb-1" />
              <p class="text-xs text-gray-500">Weight</p>
              <p class="font-semibold text-sm">{{ userStore.user.weight }} lbs</p>
            </div>
            <div v-if="userStore.user.allergies" class="bg-white p-3 rounded-lg shadow transition-all duration-300 hover:shadow-md">
              <AlertTriangle class="h-5 w-5 text-yellow-500 mb-1" />
              <p class="text-xs text-gray-500">Allergies</p>
              <p class="font-semibold text-sm">{{ userStore.user.allergies }}</p>
            </div>
          </div>

          <!-- Emergency Contact -->
          <div v-if="userStore.user.emergency_contact" class="bg-white p-3 rounded-lg shadow mb-4 transition-all duration-300 hover:shadow-md">
            <div class="flex items-center mb-2">
              <Phone class="h-5 w-5 text-indigo-500 mr-2" />
              <h3 class="text-sm font-semibold">Emergency Contact</h3>
            </div>
            <p class="text-sm">{{ userStore.user.emergency_contact }}</p>
          </div>

          <!-- Action Buttons -->
          <div class="grid grid-cols-2 gap-2">
            <template v-if="userStore.user.role === 'patient'">
              <RouterLink
                v-if="userStore.latestAppointment === 'done' || userStore.latestAppointment === null"
                :to="{ name: 'requestappointment' }"
                class="px-3 py-2 bg-green-500 text-white text-sm rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition-colors duration-300 flex items-center justify-center"
              >
                <PlusCircle class="h-4 w-4 mr-1" />
                Request Appointment
              </RouterLink>
              <RouterLink
                :to="{ name: 'updateprofile' }"
                class="px-3 py-2 bg-blue-500 text-white text-sm rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-300 flex items-center justify-center"
              >
                <User class="h-4 w-4 mr-1" />
                Update Profile
              </RouterLink>
            </template>
            <RouterLink
              :to="{ name: 'updatepassword' }"
              class="px-3 py-2 bg-emerald-500 text-white text-sm rounded-md hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-opacity-50 transition-colors duration-300 flex items-center justify-center"
            >
              <KeyRound class="h-4 w-4 mr-1" />
              Edit Password
            </RouterLink>
            <button
              @click="logOut()"
              class="px-3 py-2 bg-red-500 text-white text-sm rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition-colors duration-300 flex items-center justify-center"
            >
              <LogOut class="h-4 w-4 mr-1" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { LogOut, KeyRound, User, PlusCircle, CreditCard, Heart, Ruler, Scale, AlertTriangle, Phone } from 'lucide-vue-next';
import { parseISO, format } from 'date-fns';
import { useUserStore } from '@/stores/user';
import axios from 'axios';

export default {
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  data() {
    return {
      userCredits: {},
      emptyCredit: false
    }
  },
  mounted() {
    this.getCreditBalance();
  },
  components: {
    User,
    LogOut,
    PlusCircle,
    KeyRound,
    CreditCard,
    Heart,
    Ruler,
    Scale,
    AlertTriangle,
    Phone
  },
  computed: {
    initials() {
      return `${this.userStore.user.first_name} ${this.userStore.user.last_name}`
        .split(' ')
        .map(name => name.charAt(0).toUpperCase())
        .join('');
    },
    displayHeight() {
      let height = parseInt(this.userStore.user.height);
      let feet = Math.floor(height / 12);
      let remainingInches = height % 12;
      return `${feet}' ${remainingInches}"`;
    },
  },
  methods: {
    formatDate(dateString) {
      try {
        return format(parseISO(dateString), 'MMMM dd, yyyy - hh:mm a');
      } catch (error) {
        console.error('Date parsing error:', error);
        return 'Invalid Date';
      }
    },
    logOut() {
      this.userStore.removeToken();
      this.$router.push('/');
    },
    async getCreditBalance() {
      try {
        const response = await axios.get('/payments/usercredits/')
        if(response.status === 200){
          this.userCredits = response.data
        } else if(response.status === 204){
          this.emptyCredit = true
        }
      } catch (error) {
        if (error.response) {
          console.log(error)
        } else {
          console.error("An unexpected error occurred:", error);
        }
      }
    }
  },
};
</script>

