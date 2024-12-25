<template>
    <section aria-labelledby="credits-title">

      <div class="w-full max-w-md bg-white rounded-lg shadow-xl overflow-hidden">
        <div class="p-8">
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Purchase Credits</h2>
          <p class="text-gray-600 mb-6" v-if="creditPrice !== null">1 credit costs ${{ creditPrice.toFixed(2) }}</p>
          <p class="text-gray-600 mb-6" v-else>Loading price...</p>
          
          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium text-gray-600">Credit Price:</span>
              <span class="text-lg font-bold text-gray-800">{{ creditPrice !== null ? '$' + creditPrice.toFixed(2) : 'Loading...' }}</span>
            </div>
            
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium text-gray-600">Quantity:</span>
              <select 
                v-model="quantity" 
                class="block w-32 bg-gray-100 border border-gray-300 text-gray-700 py-2 px-3 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
              >
                <option v-for="option in quantityOptions" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
            </div>
            
            <div class="flex justify-between items-center pt-4 border-t border-gray-200">
              <span class="text-sm font-medium text-gray-600">Total Amount:</span>
              <span class="text-2xl font-bold text-gray-800">{{ creditPrice !== null ? '$' + totalAmount.toFixed(2) : 'Loading...' }}</span>
            </div>
          </div>
          
          <button 
            @click="purchaseCredits" 
            class="mt-6 w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150 ease-in-out"
            :disabled="creditPrice === null"
          >
            Purchase Credits
          </button>
        </div>
      </div>
      </section>
  </template>
  
  <script>
  import axios from 'axios';
  import { loadStripe } from '@stripe/stripe-js';
  export default {
    name: 'CreditPurchase',
    data() {
      return {
        creditPrice: null,
        quantity: 1,
        quantityOptions: [1, 2, 5, 10, 20, 50, 100],
        stripe:null,
        checkoutSessionId: null,

      }
    },
    async mounted() {
        this.stripe = await loadStripe('stripe publishable key')
        await this.fetchCreditPrice();
  },
    computed: {
      totalAmount() {
        return this.creditPrice ?  this.creditPrice * this.quantity : 0;
      }
    },
    methods: {
    async fetchCreditPrice() {
      try {
        const response = await axios.get('/payment/credit-price/');
        this.creditPrice = response.data.credit_price;
      } catch (error) {
        console.error('Error fetching credit price:', error);
        this.creditPrice = null;
      }
    },
      async purchaseCredits() {
        try {
        const response = await axios.post('/create-checkout-session/', {
          quantity: this.quantity,
          price : this.creditPrice
        });
        await this.stripe.redirectToCheckout({ sessionId: response.data.sessionId });
      } catch (error) {
        console.error('Error during Stripe checkout:', error);
      }
        
      }
    }
  }
  </script>
