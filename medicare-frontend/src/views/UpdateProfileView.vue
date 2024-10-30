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
          Edit your Profile
        </p>
      </div>
      <form @submit.prevent="handleSubmit" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="firstName" class="block text-sm font-medium text-gray-700">First Name</label>
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
          <label for="emergency_contact" class="block text-sm font-medium text-gray-700">Emergency Contact</label>
          <input 
            id="blood_type" 
            v-model="formData.emergency_contact" 
            class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
          />
          <p v-if="errors.emergency_contact" class="text-sm text-red-500">{{ errors.emergency_contact }}</p>
        </div>
        <div>
          <label for="blood_type" class="block text-sm font-medium text-gray-700">Blood Type</label>
          <select 
            v-model="formData.blood_type"
            id="blood_type"
            class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
          >
            <option disabled value="">Select blood type</option>
            <option v-for="bloodType in bloodTypes" :key="bloodType" :value="bloodType">
              {{ bloodType }}
            </option>
          </select>
          <p v-if="errors.blood_type" class="text-sm text-red-500">{{ errors.blood_type }}</p>
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
            <label for="height" class="block text-sm font-medium text-gray-700">Height</label>
            <select v-model="formData.height" class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500">
              <option disabled value="">Select height</option>
              <option v-for="height in heightOptions" :key="height.value" :value="height.value">
                {{ height.label }}
              </option>
            </select>
          <p v-if="errors.height" class="text-sm text-red-500">{{ errors.height }}</p>
        </div>
        <div>
          <label for="weight" class="block text-sm font-medium text-gray-700">Weight (lbs)</label>
          <select 
            id="weight"
            v-model="formData.weight"
            class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
          >
            <option disabled value="">Select weight</option>
            <option v-for="weight in weightOptions" :key="weight" :value="weight">{{ weight }} lbs</option>
          </select>
          <p v-if="errors.weight" class="text-sm text-red-500">{{ errors.weight }}</p>
        </div>

        <div>
          <label for="allergies" class="block text-sm font-medium text-gray-700">Allergies</label>
          <input 
            id="blood_type" 
            v-model="formData.allergies" 
            class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-teal-500 focus:border-teal-500"
          />
          <p v-if="errors.allergies" class="text-sm text-red-500">{{ errors.allergies}}</p>
        </div>
        <Button class="w-full bg-teal-500 hover:bg-teal-600 text-white mt-4">
          Submit
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="ml-2 h-4 w-4">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8L7 21m0 0H3m4 0v-4" />
          </svg>
        </Button>
      </form>
    </div>
  </div>
</template>
  <script>
  import { useUserStore } from '@/stores/user';
  import { useToastStore } from '@/stores/toast';
  import axios from 'axios';
  import Button from '@/components/ui/button.vue';
  export default {
    setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  components:{
      Button    
  },
    mounted() {
    this.generateHeightOptions();
    },
    data() {
      return {
        heightOptions:[],
        bloodTypes: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        weightOptions: Array.from({ length: 300 }, (_, index) => index + 1),
        formData: {
          first_name: this.userStore.user.first_name,
          last_name: this.userStore.user.last_name,
          email: this.userStore.user.email,
          dob: this.userStore.user.dob,
          height: this.userStore.user.height|| "",
          weight:this.userStore.user.weight || "",
          emergency_contact:this.userStore.user.emergency_contact || "",
          allergies: this.userStore.user.allergies|| "",
          blood_type:this.userStore.user.blood_type||"",
          

          
          
        },
        errors: {},
        isSubmitting: false,
      };
    },
    methods: {
      generateHeightOptions() {
      
      for (let inches = 36; inches <= 96; inches++) {
          let feet = Math.floor(inches / 12);
          let remainingInches = inches % 12;
          let heightLabel = `${feet}'${remainingInches}"`; 

          
          this.heightOptions.push({
          value: inches,   
          label: heightLabel  
          });
      }
      },
      async handleSubmit() {
        console.log(this.formData)
        this.errors = {}
        if(!this.formData.first_name) this.errors.first_name = "First name is required"
        if(!this.formData.last_name) this.errors.last_name = "Last name is required"
        if(!this.formData.email) this.errors.email = "Email is required"
        if(!this.formData.dob) this.errors.dob = "Date of birth is required"
        if(Object.keys(this.errors).length === 0 ){
          try{
            const userId = this.userStore.user.id
            const update =  await axios.patch(`/api/update/${userId}/`,this.formData);
            console.log(update.data);
            this.userStore.setUserInfo(update.data);
            

            this.toastStore.showToast(5000, "profile update successful.", "bg-emerald-500");
          
          }catch(error){
            console.log(JSON.stringify(error))
            this.toastStore.showToast(5000, "something went wrong.", "bg-red-500");
          }

        }       
        
      },
      
      
    },
  };
  </script>
  