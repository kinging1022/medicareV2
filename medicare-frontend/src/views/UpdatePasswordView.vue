<template>
    <div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Update Your Password</h2>
      </div>
      <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
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
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {{ isSubmitting ? "Updating..." : "Update Password" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { EyeIcon, EyeOffIcon } from 'lucide-vue';
  
  export default {
    components: {
      EyeIcon,
      EyeOffIcon
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
        if (this.validateForm()) {
          this.isSubmitting = true;
          try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 2000));
            console.log('Password updated:', this.formData);
            this.successMessage = 'Password updated successfully!';
            this.formData = { currentPassword: '', newPassword: '', confirmNewPassword: '' };
          } catch (error) {
            this.errors.submit = 'Failed to update password. Please try again.';
          } finally {
            this.isSubmitting = false;
          }
        }
      }
    }
  };
  </script>
  