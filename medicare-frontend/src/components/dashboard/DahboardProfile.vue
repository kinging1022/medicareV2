<template>
    <div class="bg-white p-6 rounded-lg shadow-md">
      <h2 class="text-2xl font-semibold mb-4">Personal Information</h2>
      
      <div class="flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4 mb-4">
        <div class="w-20 h-20 bg-gray-300 rounded-full flex items-center justify-center text-2xl font-bold">
          {{ initials }}
        </div>
        <div class="text-center sm:text-left">
          <h3 class="text-xl font-semibold">{{ userStore.user.first_name }} {{ userStore.user.last_name }}</h3>
          <p class="text-gray-600">
            {{ userStore.user.display_age }} years old • {{ userStore.user.gender }}
          </p>
        </div>
      </div>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
        <div v-if="userStore.user.blood_type">
          <p class="font-semibold">Blood Type</p>
          <p>{{ userStore.user.blood_type }}</p>
        </div>
        <div v-if="userStore.user.height">
          <p class="font-semibold">Height</p>
          <p>{{ displayHeight }}</p>
        </div>
        <div v-if="userStore.user.weight">
          <p class="font-semibold">Weight</p>
          <p>{{ userStore.user.weight }}lbs</p>
        </div>
        <div v-if="userStore.user.allergies">
          <p class="font-semibold">Allergies</p>
          <p>{{ userStore.user.allergies }}</p>
        </div>
      </div>
      
      <div class="mb-4" v-if="userStore.user.emergency_contact">
        <p class="font-semibold">Emergency Contact</p>
        <p>{{ userStore.user.emergency_contact }}</p>
      </div>
      
      <div class="flex flex-col sm:flex-row justify-start space-y-4 sm:space-y-0 sm:space-x-4">
        <!-- Routes for Patients -->
        <template v-if="userStore.user.role === 'patient'">
          <RouterLink
            :to="{ name: 'requestappointment' }"
            v-if="userStore.latestAppointment === 'done' || userStore.latestAppointment === null"
            class="px-4 py-2 bg-green-500 text-center text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
          >
            <PlusCircle class="inline-block mr-2 h-4 w-4" />
            Request Appointment
          </RouterLink>
          
          <RouterLink
            :to="{ name: 'updateprofile' }"
            class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-center focus:ring-opacity-50"
          >
            <User class="inline-block mr-2 h-4 w-4" />
            Update Profile
          </RouterLink>
        </template>
        
        <!-- Routes for All Users -->
        <RouterLink
          :to="{ name: 'updatepassword' }"
          class="px-4 py-2 bg-emerald-500 text-white rounded-md hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-center focus:ring-opacity-50"
        >
          <KeyRound class="inline-block mr-2 h-4 w-4" />
          Edit Password
        </RouterLink>
        
        <button
          @click="logOut()"
          class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50"
        >
          <LogOut class="inline-block mr-2 h-4 w-4" />
          Logout
        </button>
      </div>
    </div>
  </template>
  
  
  <script>
  import { LogOut, KeyRound, User, PlusCircle } from 'lucide-vue-next';
  import { parseISO, format } from 'date-fns';
  import { useUserStore } from '@/stores/user';
  import axios from 'axios';
  
  export default {
    setup() {
      const userStore = useUserStore();
      
      return {
        userStore,
      };
    },
    
    components: {
      User,
      LogOut,
      PlusCircle,
      KeyRound,
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
        let heightDisplay = `${feet}' ${remainingInches}"`;
  
        return heightDisplay;
      },
    },
    
    methods: {
      formatDate(dateString) {
        try {
          return format(parseISO(dateString), 'MMMM dd, yyyy - hh:mm a'); // Example format: October 28, 2023
        } catch (error) {
          console.error('Date parsing error:', error);
          return 'Invalid Date';
        }
      },
      
      logOut() {
        this.userStore.removeToken();
        this.$router.push('/');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add any specific styles here */
  </style>
  