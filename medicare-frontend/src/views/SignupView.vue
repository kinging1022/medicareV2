<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-teal-50 to-green-50 flex items-center justify-center p-4">
      <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
        <div class="space-y-1">
          <div class="flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-8 w-8 text-teal-500 mr-2">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm0 2c-3.86 0-7 2.5-7 5.5V22h14v-6.5c0-3-3.14-5.5-7-5.5z"/>
            </svg>
            <h1 class="text-3xl font-bold text-gray-900">Medicare</h1>
          </div>
          <p class="text-center text-gray-500">
            Create an account and start your journey to better health
          </p>
        </div>
        <form @submit.prevent="handleSubmit" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="firstName" class="block text-sm font-medium text-gray-700">First name</label>
              <input 
                id="firstName" 
                v-model="formData.first_name" 
                placeholder="John"
                class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
              />
              <p v-if="errors.first_name" class="text-sm text-red-500">{{ errors.first_name }}</p>
            </div>
            <div>
              <label for="lastName" class="block text-sm font-medium text-gray-700">Last name</label>
              <input 
                id="lastName" 
                v-model="formData.last_name" 
                placeholder="Doe"
                class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
              />
              <p v-if="errors.last_name" class="text-sm text-red-500">{{ errors.last_name }}</p>
            </div>
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input 
              id="email" 
              v-model="formData.email"
              type="email" 
              placeholder="john@example.com"
              class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
            />
            <p v-if="errors.email" class="text-sm text-red-500">{{ errors.email }}</p>
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <input 
              id="password" 
              v-model="formData.password" 
              type="password"
              class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
            />
            <p v-if="errors.password" class="text-sm text-red-500">{{ errors.password }}</p>
          </div>
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirm Password</label>
            <input 
              id="confirmPassword"
              v-model="formData.re_password"
              type="password"
              class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
            />
            <p v-if="errors.re_password" class="text-sm text-red-500">{{ errors.re_password }}</p>
          </div>
          <div>
            <label for="dateOfBirth" class="block text-sm font-medium text-gray-700">Date of Birth</label>
            <input 
              id="dateOfBirth"
              v-model="formData.dob"
              type="date"
              class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
            />
            <p v-if="errors.dob" class="text-sm text-red-500">{{ errors.dob }}</p>
          </div>
          <div>
            <label for="gender" class="block text-sm font-medium text-gray-700">Gender</label>
            <select v-model="formData.gender" class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500">
              <option disabled value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
              <option value="prefer-not-to-say">Prefer not to say</option>
            </select>
            <p v-if="errors.gender" class="text-sm text-red-500">{{ errors.gender }}</p>
          </div>
          <div class="flex items-center space-x-2">
            <input 
              type="checkbox" 
              id="agreeTerms" 
              v-model="agreeTerms"
              class="border-gray-300 rounded"
            />
            <label for="agreeTerms" class="text-sm font-medium">
              I agree to the 
              <router-link class="text-teal-500 hover:underline" to="#">terms and conditions</router-link>
            </label>
          </div>
          <p v-if="errors.agreeTerms" class="text-sm text-red-500">{{ errors.agreeTerms }}</p>
          <Button class="w-full bg-teal-500 hover:bg-teal-600 text-white mt-4">
            Create Account
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="ml-2 h-4 w-4">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8L7 21m0 0H3m4 0v-4" />
            </svg>
          </Button>
          <p class="text-sm text-gray-600 text-center mt-4">
            Already have an account? 
            <router-link to="/login" class="text-teal-500 hover:underline">Log in</router-link>
          </p>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import Button from "@/components/ui/button.vue";
  import axios from "axios";
  import { useToastStore } from "@/stores/toast";

  export default {
    setup() {
        const toastStore = useToastStore()

        return {
            toastStore
        }
    },
    
    components: {
      Button
    },
    
    data() {
      return {
        formData: {
          first_name: '',
          last_name: '',
          email: '',
          password: '',
          re_password: '',
          dob: '',
          gender: '',
        },
        agreeTerms: false,
        errors: {}
      };
    },
    methods: {
      handleSubmit() {
        this.errors = {};
        if (!this.formData.first_name) this.errors.first_name = "First name is required";
        if (!this.formData.last_name) this.errors.last_name = "Last name is required";
        if (!this.formData.email) this.errors.email = "Email is required";
        if (!this.formData.password) this.errors.password = "Password is required";
        if (this.formData.password !== this.formData.re_password) this.errors.re_password = "Passwords do not match";
        if (!this.formData.dob) this.errors.dob = "Date of birth is required";
        if (!this.formData.gender) this.errors.gender = "Gender is required";
        if (!this.agreeTerms) this.errors.agreeTerms = "You must agree to the terms and conditions";
        if (Object.keys(this.errors).length === 0) {
            console.log(this.formData.data);
         axios
           .post('/api/auth/users/', this.formData)
           .then(response => {
                console.log(response.status)
            
              if (response.status === 201){
                
                  this.toastStore.showToast(5000, 'The user is registered.  Please activate your account by clicking your email link.', 'bg-emerald-500')
                  for (const key in this.formData){
                            if(this.formData.hasOwnProperty(key)){
                                this.formData[key] = '';
                            }
                        }
                    this.agreeTerms = false;
                    
              }
           })
           .catch(error => {
               if(error.response && error.response.data){
                   const serverErrors = error.response.data;
                   Object.keys(serverErrors).forEach(field => {
                       this.errors[field] = serverErrors[field][0];
                   });
                   this.toastStore.showToast(5000,'Registration failed. Please fix the highlighted errors.', 'bg-red-500')
               }
          })
        }
      },
    }
  };
  </script>
 