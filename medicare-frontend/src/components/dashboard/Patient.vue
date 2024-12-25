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
        <Appointment
        :appointments="appointments"
        :format-date="formatDate"
        />

        <!-- Medications -->
         <Medication
         :medications="medications"
         @medics="handleReminderOpen"
         />
         
       

        <!-- Consultations History -->
         <Consultation
         
         />

         <!--Reminder-->

         <Reminder
         :is-open="isOpen"
         :medication-id="medicationId"
         @close="handleReminderClose"
         @reminderSuccess="handleReminderSuccess"
         />
       

       
      </div>
    </div>
  </div>
</template>

  
  <script>
import { LogOut, Bell, Calendar, Clock, FileText, Pill, KeyRound, User,  PlusCircle } from 'lucide-vue-next';
import { parseISO, format } from 'date-fns';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import DahboardProfile from './DahboardProfile.vue';
import axios from 'axios';
import Medication from '../patient/Medication.vue';
import Consultation from '../patient/Consultation.vue';
import Reminder from '../modal/Reminder.vue';
import Appointment from '../patient/Appointment.vue';

export default {
  name: "Patient",
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
    FileText,
    Pill,
    DahboardProfile,
    Medication,
    Consultation,
    Reminder,
    Appointment
  },
  data() {
    return {
      medications: [],
      appointments: [],
      showReminder: null,
      socket: null,
      isOpen:false,
      medicationId:null,
      userStore:useUserStore(),
      toastStore: useToastStore(),
      
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
    async getMedications(){
      try{

        const response = await axios.get('/api/account/medications/')
        console.log(response.data)
        this.medications = response.data



      }catch(error){

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
        return format(parseISO(dateString), 'MMMM dd, yyyy - hh:mm a'); 
      } catch (error) {
        console.error('Date parsing error:', error);
        return 'Invalid Date';
      }
    },
    handleReminderOpen(medicationId) {
      this.isOpen = true
      this.medicationId = medicationId;
      
    },
    handleReminderClose() {
      this.isOpen = false
      this.medicationId = null;
      
    },
    handleReminderSuccess(medicationId) {
      const medication = this.medications.find(med => med.id === medicationId);
      if (medication) {
        medication.has_reminder = true;
        this.isOpen = false;
        this.toastStore.showToast(5000, "Reminder set sucessfully", "bg-teal-500");
      } else {
        console.error(`Medication with ID ${medicationId} not found.`);
      }
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
