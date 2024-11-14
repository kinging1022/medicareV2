<template>
    <div class="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div class="relative py-3 sm:max-w-xl sm:mx-auto">
        <div class="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div class="max-w-md mx-auto">
            <h1 class="text-2xl font-semibold mb-6 text-center">Request an Appointment</h1>
  
            <div class="mb-6">
              <h2 class="text-lg font-semibold mb-2">Patient Details</h2>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <p class="text-sm text-gray-600">Name</p>
                  <p class="font-medium">{{ userStore.user.first_name }} {{ userStore.user.last_name }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-600">Email</p>
                  <p class="font-medium">{{ userStore.user.email }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-600">Emergency Phone</p>
                  <p class="font-medium">{{ userStore.user.emergency_contact }}</p>
                </div>
              </div>
            </div>
  
            <form @submit.prevent="handleSubmit" class="space-y-6">
            <div>
              <label for="doctor" class="block text-sm font-medium text-gray-700 mb-1">
                Select Doctor
              </label>
              <select
                id="doctor"
                v-model="selectedDoctor"
                class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                required
              >
                <option value="" disabled selected>Choose a doctor</option>
                <option v-for="doctor in doctors" :key="doctor.id" :value="doctor.id">
                  Dr {{ doctor.first_name }} - {{ doctor.last_name }}
                </option>
              </select>
            </div>
            <div>
                <label for="reason" class="block text-sm font-medium text-gray-700 mb-1">
                  Reason for Appointment
                </label>
                <textarea
                  id="reason"
                  v-model="reason"
                  rows="4"
                  class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md resize-none"
                  placeholder="Please briefly describe the reason for your appointment request."
                  aria-describedby="reason-description"
                  required
                ></textarea>
                <p id="reason-description" class="mt-2 text-sm text-gray-500">
                  Please provide any relevant symptoms or concerns. (10-500 characters)
                </p>
              </div>
  
              <p v-if="error" class="text-red-600 text-sm" role="alert">{{ error }}</p>
              <p v-if="success" class="text-green-600 text-sm" role="alert">
                Appointment request submitted successfully!
              </p>
  
              <button
                type="submit"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Submit Appointment Request
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
   
  <script>
  import { useUserStore } from '@/stores/user';
  import axios from 'axios';
  export default {
    setup(){
        const userStore = useUserStore()

        return{
            userStore
        }
    },
    data() {
      return {
        reason: '',
        error: '',
        success: false,
        selectedDoctor : '',
        doctors :[]
      };
    },
    mounted(){
        this.getDoctors()
    },
    methods: {
    async handleSubmit() {
        this.error = '';
        this.success = false;

        if (this.reason.length < 10) {
        this.error = 'Please provide a reason of at least 10 characters.';
        return;  
        }

        if (this.reason.length > 500) {
        this.error = 'Reason must not exceed 500 characters.';
        return; 
        }
        const payload = {'body':this.reason,
                        'created_for': this.selectedDoctor,
        }
        console.log(this.reason);
        try {

            const response = await axios.post('/api/request/appointment/',payload)


        }catch(error){
            console.log(this.error)
        }

        this.success = true;
        this.reason = '';  
        },
        getDoctors(){
            const ws = new WebSocket('ws://localhost:8000/ws/users/')

            ws.onopen = () =>{
                ws.send(
                    JSON.stringify({
                        action:'list',
                        request_id : new Date().getTime()
                    })
                )
            }
            ws.onmessage = (e) => {

            
                const response = JSON.parse(e.data);
                if (response.action === 'list') {
                    let users = response.data;
                    this.doctors = []; 
                    for (const user of users) { 
                        if (user.role === 'doctor') {
                            this.doctors.push(user); 
                            }
                        }
                        console.log(this.doctors);
                    }
                };
            },
    },

  };
  </script>
  
  <style scoped>
  /* Add any component-specific styles here if needed */
  </style>