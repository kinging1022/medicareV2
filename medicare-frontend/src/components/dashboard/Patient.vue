<template>
  <div class="container mx-auto p-4">
    <header class="mb-6">
      <h1 class="text-2xl md:text-3xl font-bold">Patient Dashboard</h1>
      <p class="text-gray-600">
        Welcome back, {{ userStore.user.first_name }} {{ userStore.user.last_name }}
      </p>
    </header>

    <div class="space-y-6">
      <DahboardProfile />
      <div class="grid grid-cols-1 gap-4 items-start lg:grid-cols-2 lg:gap-8">
        <!-- Appointments -->
        <section aria-labelledby="appointments-title">
          <div class="rounded-lg bg-white overflow-hidden shadow">
            <div class="p-6">
              <h2 class="text-lg font-medium text-gray-900" id="appointments-title">Appointments</h2>
              <div class="mt-6 flow-root">
                <ul class="-my-5 divide-y divide-gray-200">
                  <li
                    v-for="appointment in appointments"
                    :key="appointment.id"
                    class="py-5"
                  >
                    <div class="flex items-center space-x-4">
                      <div class="flex-shrink-0">
                        <Calendar class="h-8 w-8 text-indigo-600" />
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">
                          Dr {{ appointment.created_for.first_name }} {{ appointment.created_for.last_name }}
                        </p>
                        <p class="text-sm text-gray-500 truncate">
                          {{ formatDate(appointment.created_at) }}
                        </p>
                      </div>
                      <div>
                        <span
                          :class="[
                            'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                            appointment.status === 'processed' ? 'bg-green-100 text-green-800' :
                            appointment.status === 'sent' ? 'bg-blue-100 text-blue-800' :
                            appointment.status === 'done' ? 'bg-blue-100 text-blue-800' :
                            'bg-red-100 text-red-800'
                          ]"
                        >
                          {{ appointment.status }}
                        </span>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <!-- Medications -->
        <section aria-labelledby="medications-title">
          <div class="rounded-lg bg-white overflow-hidden shadow">
            <div class="p-6">
              <h2 class="text-lg font-medium text-gray-900" id="medications-title">Medications</h2>
              <div class="mt-6 flow-root">
                <ul class="-my-5 divide-y divide-gray-200">
                  <li
                    v-for="medication in medications"
                    :key="medication.id"
                    class="py-5"
                  >
                    <div class="flex items-center space-x-4">
                      <div class="flex-shrink-0">
                        <Pill class="h-8 w-8 text-indigo-600" />
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">
                          {{ medication.name }}
                        </p>
                        <p class="text-sm text-gray-500 truncate">
                          {{ `${medication.weight}mg - ${medication.dosage}` }}
                        </p>
                      </div>
                      <div>
                        <button
                          @click="handleReminder(medication.id)"
                          class="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          Set Reminder
                        </button>
                      </div>
                    </div>
                    <div v-if="showReminder === medication.id" class="mt-2 text-sm text-green-600">
                      Reminder set for {{ medication.reminder }}
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <!-- Consultations History -->
        <section aria-labelledby="consultations-title">
          <div class="rounded-lg bg-white overflow-hidden shadow">
            <div class="p-6">
              <h2 class="text-lg font-medium text-gray-900" id="consultations-title">Consultations History</h2>
              <div class="mt-6 flow-root">
                <ul class="-my-5 divide-y divide-gray-200">
                  <li
                    v-for="consultation in consultations"
                    :key="consultation.id"
                    class="py-5"
                  >
                    <div class="flex items-center space-x-4">
                      <div class="flex-shrink-0">
                        <FileText class="h-8 w-8 text-indigo-600" />
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">
                          {{ consultation.doctor }}
                        </p>
                        <p class="text-sm text-gray-500 truncate">
                          {{ consultation.date }}
                        </p>
                        <p class="text-sm text-gray-500 truncate">
                          {{ consultation.diagnosis }}
                        </p>
                      </div>
                    </div>
                    <div class="mt-2">
                      <p class="text-sm text-gray-600">{{ consultation.notes }}</p>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <!-- Billing History -->
        <section aria-labelledby="billing-title">
          <div class="rounded-lg bg-white overflow-hidden shadow">
            <div class="p-6">
              <h2 class="text-lg font-medium text-gray-900" id="billing-title">Billing History</h2>
              <div class="mt-6 flow-root">
                <ul class="-my-5 divide-y divide-gray-200">
                  <li
                    v-for="bill in billingHistory"
                    :key="bill.id"
                    class="py-5"
                  >
                    <div class="flex items-center space-x-4">
                      <div class="flex-shrink-0">
                        <DollarSign class="h-8 w-8 text-indigo-600" />
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">
                          {{ bill.description }}
                        </p>
                        <p class="text-sm text-gray-500 truncate">
                          {{ bill.date }}
                        </p>
                      </div>
                      <div>
                        <span
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
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
      </div>
    </div>
  </div>
</template>

  
  <script>
import { LogOut, Bell, Calendar, Clock, FileText, Pill, KeyRound, User, DollarSign, PlusCircle } from 'lucide-vue-next';
import { parseISO, format } from 'date-fns';
import { useUserStore } from '@/stores/user';
import DahboardProfile from './DahboardProfile.vue';
import axios from 'axios';

export default {
  name: "Patient",
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
    mounted() {
    this.getMedications();
    this.getAndUpdateAppointments();
   
    
    
  },
  components: {
    User,
    LogOut,
    PlusCircle,
    KeyRound,
    Bell,
    Calendar,
    Clock,
    DollarSign,
    FileText,
    Pill,
    DahboardProfile
  },
  data() {
    return {
      medications: [],
      appointments: [],
      showReminder: null,
      socket: null,
      
      patientDetails: {
        name: 'Sarah Johnson',
        age: 35,
        email: 'sarah.johnson@example.com',
        phone: '+1 (555) 123-4567',
        imageUrl: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
      },
      dappointments: [
        { id: 1, date: '2023-10-28', time: '10:00 AM', doctor: 'Dr. Emily Clark', status: 'Upcoming' },
        { id: 2, date: '2023-10-15', time: '2:30 PM', doctor: 'Dr. Michael Lee', status: 'Completed' },
        { id: 3, date: '2023-09-30', time: '11:15 AM', doctor: 'Dr. Sarah Johnson', status: 'Cancelled' },
      ],
      nmedications: [
        { id: 1, name: 'Lisinopril', dosage: '10mg', frequency: 'Once daily', reminder: '8:00 AM' },
        { id: 2, name: 'Metformin', dosage: '500mg', frequency: 'Twice daily', reminder: '9:00 AM, 9:00 PM' },
        { id: 3, name: 'Simvastatin', dosage: '20mg', frequency: 'Once daily', reminder: '9:00 PM' },
      ],
      consultations: [
        { id: 1, date: '2023-10-15', doctor: 'Dr. Michael Lee', diagnosis: 'Hypertension', notes: 'Blood pressure slightly elevated. Adjusted medication dosage.' },
        { id: 2, date: '2023-09-01', doctor: 'Dr. Sarah Johnson', diagnosis: 'Annual Check-up', notes: 'All vitals normal. Recommended lifestyle changes for weight management.' },
        { id: 3, date: '2023-07-20', doctor: 'Dr. Robert Chen', diagnosis: 'Skin Rash', notes: 'Prescribed topical cream for eczema flare-up.' },
      ],
      billingHistory: [
        { id: 1, date: '2023-10-15', description: 'Consultation with Dr. Michael Lee', amount: 150 },
        { id: 2, date: '2023-09-01', description: 'Annual Check-up with Dr. Sarah Johnson', amount: 200 },
        { id: 3, date: '2023-07-20', description: 'Dermatology Consultation with Dr. Robert Chen', amount: 175 },
      ],
    };
  },
  computed: {
    initials() {
      return `${this.userStore.user.first_name} ${this.userStore.user.last_name}`
        .split(' ')
        .map(name => name.charAt(0).toUpperCase())
        .join('');
    },
    displayHeight() {
      let height = parseInt(this.userStore.user.height);
      let feet = Math.floor(height / 12);
      let remainingInches = height % 12;
      let heightDisplay = `${feet}' ${remainingInches}"`;

      return heightDisplay;
    },
  },
  methods: {
    getMedications(){
      const token = this.userStore.user.access
        const ws = new WebSocket(`ws://localhost:8000/ws/medications/?token=${token}`);
      
        ws.onopen = () => {

            ws.send(
                JSON.stringify({
                    action: "list",
                    request_id: new Date().getTime(),
                })
            );
        };
        ws.onmessage = (e) => {
            const allData = JSON.parse(e.data);
            if (allData.action === 'list'){
                this.medications = allData.data;
                
            }else if ( allData.action === "create" ){
                this.medications.push(allData.data);
            }
        }
      

    },

    getAndUpdateAppointments (){
        const token = this.userStore.user.access
        const ws = new WebSocket(`ws://localhost:8000/ws/appointments/?token=${token}`);
      
        ws.onopen = () => {

            ws.send(
                JSON.stringify({
                    action: "list",
                    request_id: new Date().getTime(),
                })
            );
        };
        ws.onmessage = (e) => {
            const allData = JSON.parse(e.data);
            if (allData.action === 'list'){
                this.appointments = allData.data;
                if(this.appointments.length > 0){
                  this.userStore.latestAppointment = allData.data[0].status;
                }else{
                  console.log('No appointment available ');
                  this.userStore.latestAppointment = null;
                }
                
                console.log(this.latestAppointment)
            }else if ( allData.action === "create" ){
                this.appointments.push(allData.data);
            }
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
    handleReminder(medicationId) {
      this.showReminder = medicationId;
      // In a real app, you would set up a notification or alarm here
      setTimeout(() => {
        this.showReminder = null;
      }, 3000); // Hide reminder after 3 seconds
    },
    logOut() {
      this.userStore.removeToken();
      this.$router.push('/');
    },
   
  },
};
</script>

<style scoped>
/* Add any specific styles here */
</style>
