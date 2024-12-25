<template>
    <div class="container mx-auto p-4">
      <div class="space-y-6">
        <div class="grid grid-cols-1 gap-4 items-start lg:grid-cols-2 lg:gap-8">
           
            <Credit/>
          
            <!-- Billing History -->
             <Billing/>
          
            
        </div>
      </div>
    </div>
  </template>
  
    
<script>
  import {  DollarSign, } from 'lucide-vue-next';
  import Credit from '@/components/payment/Credit.vue';
  import Billing from '@/components/payment/Billing.vue';
  
  export default {
    name: "CreditView",
      mounted() {
       
      
    },
    components: {
      DollarSign,
      Credit,
      Billing
      
    },
    data() {
      return {
       
      };
    },
    computed: {
      
    },
    methods: {
        
       
    },
  };
  </script>
  
  <style scoped>
  /* Add any specific styles here */
  </style>
  
