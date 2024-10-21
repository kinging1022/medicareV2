<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-teal-50 to-green-50 flex items-center justify-center p-4">
      <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
        <div class="space-y-1">
          <div class="flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-8 w-8 text-teal-500 mr-2">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm0 2c-3.86 0-7 2.5-7 5.5V22h14v-6.5c0-3-3.14-5.5-7-5.5z"/>
            </svg>
            <h1 class="text-3xl font-bold text-gray-900">Medicare Login</h1>
          </div>
          <p class="text-center text-gray-500">Log in to access your account</p>
        </div>
        <form @submit.prevent="handleSubmit" class="mt-6 space-y-4">
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
          <Button class="w-full bg-teal-500 hover:bg-teal-600 text-white mt-4">
            Log In
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="ml-2 h-4 w-4">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8L7 21m0 0H3m4 0v-4"/>
            </svg>
          </Button>
          <p class="text-sm text-gray-600 text-center mt-4">
            Don't have an account? 
            <router-link to="/signup" class="text-teal-500 hover:underline">Sign up</router-link>
          </p>
        </form>
      </div>
    </div>
  </template>

  <script>
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";
import Button from "@/components/ui/button.vue";
import axios from "axios";

export default {
  components: {
    Button,
  },
  data() {
    return {
      formData: {
        email: "",
        password: "",
      },
      errors: {},
    };
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  methods: {
    async handleSubmit() {
      this.errors = {};

      
      if (!this.formData.email) this.errors.email = "Email is required";
      if (!this.formData.password) this.errors.password = "Password is required";

      
      if (Object.keys(this.errors).length === 0) {
        try {
          
          const response = await axios.post("/api/auth/token/login/", this.formData);
          this.userStore.setToken(response.data);

          
          this.toastStore.showToast(5000, "Login successfully.", "bg-emerald-500");

          
          Object.keys(this.formData).forEach((key) => {
            this.formData[key] = "";
          });

          
          const userInfo = await axios.get("/api/auth/users/me");
          this.userStore.setUserInfo(userInfo.data);

          this.$router.push('/dashboard')

        } catch (error) {
          if (error.response && error.response.data) {
            console.log(error.response.data)
            const serverErrors = error.response.data;
            Object.keys(serverErrors).forEach((field) => {
              this.errors[field] = serverErrors[field][0];
            });

            if (serverErrors.detail==="No active account found with the given credentials"){
                this.resendActivationEmail()
            }
          }

          
          this.toastStore.showToast(5000, "Login failed. Please check your inputs.", "bg-red-500");
        }
      }
    },
    async resendActivationEmail(){
        try{
            const response = await axios.post('/api/auth/users/resend_activation/',{
                email:this.formData.email
            })
            this.toastStore.showToast(5000, 'Check your email to activate your account.', 'bg-emerald-500');
        }catch(error){
            console.log(error)
        }
    }
  },
};
</script>
