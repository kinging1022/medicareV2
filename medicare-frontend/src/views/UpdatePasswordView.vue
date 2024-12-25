
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
        <p class="text-center text-gray-500">Update your password</p>
      </div>
      <form class="space-y-6" @submit.prevent="handleSubmit">
  <div v-for="(label, fieldName) in passwordFields" :key="fieldName">
    <label :for="fieldName" class="block text-sm font-medium text-gray-700">
      {{ label }}
    </label>
    <div class="mt-1 relative rounded-md shadow-sm">
      <input
        :id="fieldName"
        :name="fieldName"
        :type="showPasswords[fieldName] ? 'text' : 'password'"
        :autocomplete="autocomplete[fieldName]"
        required
        class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm pr-10"
        v-model="formData[fieldName]"
      />
      <button type="button" class="absolute inset-y-0 right-0 pr-3 flex items-center" @click="togglePasswordVisibility(fieldName)">
        <EyeIcon v-if="showPasswords[fieldName]" class="h-5 w-5 text-gray-400" />
        <EyeOffIcon v-else class="h-5 w-5 text-gray-400" />
      </button>
    </div>
    <p v-if="errors[fieldName]" class="mt-2 text-sm text-red-600">{{ errors[fieldName] }}</p>
  </div>

  <div v-if="errors.submit" class="rounded-md bg-red-50 p-4">
    <div class="flex">
      <div class="ml-3">
        <h3 class="text-sm font-medium text-red-800">{{ errors.submit }}</h3>
      </div>
    </div>
  </div>

  <div v-if="successMessage" class="rounded-md bg-green-50 p-4">
    <div class="flex">
      <div class="ml-3">
        <h3 class="text-sm font-medium text-green-800">{{ successMessage }}</h3>
      </div>
    </div>
  </div>

  <div>
    <button
      type="submit"
      :disabled="isSubmitting"
      class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium  bg-teal-500 hover:bg-teal-600 text-white mt-4"
    >
      {{ isSubmitting ? "Updating..." : "Update Password" }}
    </button>
  </div>
</form>
      
    </div>
  </div>
</template>
<script>
import { EyeIcon, EyeOffIcon } from 'lucide-vue-next';
import axios from 'axios';
import { useUserStore } from '@/stores/user';

export default {
  components: {
    EyeIcon,
    EyeOffIcon
  },
  setup() {
    const userStore = useUserStore();
    return {
      userStore
    };
  },
  data() {
    return {
      formData: {
        currentPassword: '',
        newPassword: '',
        confirmNewPassword: ''
      },
      showPasswords: {
        currentPassword: false,
        newPassword: false,
        confirmNewPassword: false
      },
      errors: {},
      isSubmitting: false,
      successMessage: '',
      passwordFields: {
        currentPassword: 'Current Password',
        newPassword: 'New Password',
        confirmNewPassword: 'Confirm New Password'
      },
      autocomplete: {
        currentPassword: 'current-password',
        newPassword: 'new-password',
        confirmNewPassword: 'new-password'
      }
    };
  },
  methods: {
    togglePasswordVisibility(field) {
      this.showPasswords[field] = !this.showPasswords[field];
    },
    validateForm() {
      const newErrors = {};
      if (!this.formData.currentPassword) newErrors.currentPassword = 'Current password is required';
      if (!this.formData.newPassword) newErrors.newPassword = 'New password is required';
      if (this.formData.newPassword.length < 8) newErrors.newPassword = 'New password must be at least 8 characters long';
      if (!this.formData.confirmNewPassword) newErrors.confirmNewPassword = 'Please confirm your new password';
      if (this.formData.newPassword !== this.formData.confirmNewPassword) newErrors.confirmNewPassword = 'Passwords do not match';
      this.errors = newErrors;
      return Object.keys(newErrors).length === 0;
    },
    async handleSubmit() {
      this.successMessage = '';
      this.errors.submit = '';  // Clear the error message before submission
      if (this.validateForm()) {
        this.isSubmitting = true;
        const payload = {
          current_password: this.formData.currentPassword,
          new_password: this.formData.newPassword
        };
        try {
          const response = await axios.post('/api/auth/users/set_password/', payload);
          this.successMessage = 'Password updated successfully!';
          this.formData = { currentPassword: '', newPassword: '', confirmNewPassword: '' };
          this.userStore.removeToken();

          
          setTimeout(() => {
            this.$router.push('/login');
          }, 1000); 
        } catch (error) {
          if (error.response && error.response.data) {
            const serverErrors = error.response.data
            Object.keys(serverErrors).forEach((field)=>{
              this.errors.submit = serverErrors[field][0]
            })
          } else {
            this.errors.submit = 'Failed to update password. Please try again.';
          }
        } finally {
          this.isSubmitting = false;
        }
      }
    }
  }
};
</script>


