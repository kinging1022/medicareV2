<template>
  <section aria-labelledby="billing-title">
    <div class="rounded-lg bg-white overflow-hidden shadow">
      <div class="p-6">
        <h2 class="text-lg font-medium text-gray-900" id="billing-title">Billing History</h2>
        <div class="mt-6 flow-root">
          <ul class="-my-5 divide-y divide-gray-200">
            <li v-for="bill in billingHistory" :key="bill.id" class="py-5">
              <div class="flex items-center space-x-4">
                <div class="flex-shrink-0">
                  <DollarSign class="h-8 w-8 text-indigo-600" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">
                    {{ bill.message }}
                  </p>
                  <p class="text-sm text-gray-500 truncate">
                    {{ formatDate(bill.timestamp) }}
                  </p>
                </div>
                <div>
                  <span
                    :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      bill.type === 'credit' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    ]"
                  >
                    ${{ bill.amount }}
                  </span>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { DollarSign } from 'lucide-vue-next';
import { parseISO, format } from 'date-fns';
import axios from 'axios';

export default {
  name: "Billing",
  mounted() {
    this.getTransactions();
  },
  components: {
    DollarSign,
  },
  data() {
    return {
      billingHistory: [],
    };
  },
  methods: {
    async getTransactions() {
      try {
        const response = await axios.get('/payments/billing/');
        this.billingHistory = response.data;
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
    },
    formatDate(dateString) {
      try {
        return format(parseISO(dateString), 'MMMM dd, yyyy - hh:mm a'); // Example format: October 28, 2023
      } catch (error) {
        console.error('Date parsing error:', error);
        return 'Invalid Date';
      }
    },
  },
};
</script>
