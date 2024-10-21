<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-teal-50 to-green-50 flex items-center justify-center p-4">
      <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
        <div class="text-center mb-6">
          <div class="mx-auto w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mb-4">
            <CheckCircle class="h-10 w-10 text-primary" color="teal"/>
          </div>
          <h1 class="text-2xl font-bold text-teal-700">Account Activated!</h1>
          <p class="text-gray-500">Your email has been successfully verified.</p>
        </div>
        <div class="text-center mb-6">
          <p class="text-gray-600">
            Thank you for verifying your email address. Your account is now fully activated and you can start using our services.
          </p>
        </div>
        <div class="flex flex-col space-y-2">
          <Button class="w-full bg-teal-500 hover:bg-teal-600 text-white">
            <router-link to="/login" class="flex items-center justify-center w-full">
              Proceed to Login
            </router-link>
          </Button>
          <Button variant="outline" class="w-full border-teal-500 text-teal-500 hover:bg-teal-50">
            <router-link to="/" class="flex items-center justify-center w-full">
              Go to Homepage
            </router-link>
          </Button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import Button from '@/components/ui/button.vue'
  import { CheckCircle } from 'lucide-vue-next';
 
  </script>
  
  <style scoped>

  </style>
  