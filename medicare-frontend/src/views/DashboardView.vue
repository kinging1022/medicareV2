
<template>
    <div class="container mx-auto p-4">
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold">Patient Dashboard</h1>
        <p class="text-gray-600">Welcome back, {{ patientData.name }}</p>
      </header>
  
      <div class="space-y-6">
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-2xl font-semibold mb-4">Personal Information</h2>
          <div class="flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4 mb-4">
            <div class="w-20 h-20 bg-gray-300 rounded-full flex items-center justify-center text-2xl font-bold">
              {{ initials }}
            </div>
            <div class="text-center sm:text-left">
              <h3 class="text-xl font-semibold">{{ patientData.name }}</h3>
              <p class="text-gray-600">
                {{ patientData.age }} years old • {{ patientData.gender }}
              </p>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
              <p class="font-semibold">Blood Type</p>
              <p>{{ patientData.bloodType }}</p>
            </div>
            <div>
              <p class="font-semibold">Height</p>
              <p>{{ patientData.height }}</p>
            </div>
            <div>
              <p class="font-semibold">Weight</p>
              <p>{{ patientData.weight }}</p>
            </div>
            <div>
              <p class="font-semibold">Allergies</p>
              <p>{{ patientData.allergies.join(', ') }}</p>
            </div>
          </div>
          <div class="mb-4">
            <p class="font-semibold">Emergency Contact</p>
            <p>{{ patientData.emergencyContact }}</p>
          </div>
          <div class="flex flex-col sm:flex-row justify-start space-y-4 sm:space-y-0 sm:space-x-4">
            <button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                <User class="inline-block mr-2 h-4 w-4" />
                Update Profile
            </button>
            <button
              @click="handleRequestAppointment"
              class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
            >
            <PlusCircle class="inline-block mr-2 h-4 w-4" />
              Request Appointment
            </button>
            <button @click="logOut()" class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50">
                <LogOut class="inline-block mr-2 h-4 w-4" />
                Logout
            </button>
          </div>
        </div>
  
        <div class="space-y-4">
          <!-- Consultations -->
          <ExpandableSection title="Consultations" :isOpen="isSectionOpen('consultations')" @toggle="toggleSection('consultations')">
            <template #content>
              <div class="space-y-4 max-h-[400px] overflow-y-auto">
                <div v-for="(consultation, index) in patientData.consultations" :key="index" class="p-4 border rounded-lg">
                  <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-2">
                    <p class="font-semibold">{{ consultation.date }}</p>
                    <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">{{ consultation.doctor }}</span>
                  </div>
                  <p><strong>Diagnosis:</strong> {{ consultation.diagnosis }}</p>
                  <p><strong>Prescription:</strong> {{ consultation.prescription }}</p>
                </div>
              </div>
            </template>
          </ExpandableSection>
  
          <!-- Lab Reports -->
          <ExpandableSection title="Lab Reports" :isOpen="isSectionOpen('lab-reports')" @toggle="toggleSection('lab-reports')">
            <template #content>
              <div class="space-y-4 max-h-[400px] overflow-y-auto">
                <div v-for="(report, index) in patientData.labReports" :key="index" class="p-4 border rounded-lg flex flex-col sm:flex-row justify-between items-start sm:items-center">
                  <div>
                    <p class="font-semibold">{{ report.date }}</p>
                    <p>{{ report.test }}</p>
                    <p><strong>Result:</strong> {{ report.result }}</p>
                  </div>
                  <button class="mt-2 sm:mt-0 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                    Download
                  </button>
                </div>
              </div>
            </template>
          </ExpandableSection>
  
          <!-- Medical History -->
          <ExpandableSection title="Medical History" :isOpen="isSectionOpen('medical-history')" @toggle="toggleSection('medical-history')">
            <template #content>
              <div class="grid gap-4 md:grid-cols-2">
                <div>
                  <h3 class="text-lg font-semibold mb-2">Vaccination Records</h3>
                  <div class="space-y-4 max-h-[200px] overflow-y-auto">
                    <div v-for="(vaccination, index) in patientData.vaccinations" :key="index" class="p-4 border rounded-lg">
                      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-2">
                        <p class="font-semibold">{{ vaccination.name }}</p>
                        <span class="px-2 py-1 bg-green-100 text-green-800 rounded-full text-sm">{{ vaccination.date }}</span>
                      </div>
                      <p><strong>Next Due:</strong> {{ vaccination.nextDue }}</p>
                    </div>
                  </div>
                </div>
                <div>
                  <h3 class="text-lg font-semibold mb-2">Current Medications</h3>
                  <div class="space-y-4 max-h-[200px] overflow-y-auto">
                    <div v-for="(medication, index) in patientData.medications" :key="index" class="p-4 border rounded-lg">
                      <p class="font-semibold">{{ medication.name }}</p>
                      <p><strong>Dosage:</strong> {{ medication.dosage }}</p>
                      <p><strong>Frequency:</strong> {{ medication.frequency }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </ExpandableSection>
  
          <!-- Upcoming Appointments -->
          <ExpandableSection title="Upcoming Appointments" :isOpen="isSectionOpen('appointments')" @toggle="toggleSection('appointments')">
            <template #content>
              <div class="space-y-4 max-h-[400px] overflow-y-auto">
                <div v-for="(appointment, index) in patientData.upcomingAppointments" :key="index" class="p-4 border rounded-lg">
                  <div class="flex justify-between items-center mb-2">
                    <p class="font-semibold">{{ appointment.date }}</p>
                    <span class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">{{ appointment.doctor }}</span>
                  </div>
                  <p><strong>Time:</strong> {{ appointment.time }}</p>
                  <p><strong>Reason:</strong> {{ appointment.reason }}</p>
                </div>
              </div>
            </template>
          </ExpandableSection>
  
          <!-- Billing & Insurance -->
          <ExpandableSection title="Billing & Insurance" :isOpen="isSectionOpen('billing')" @toggle="toggleSection('billing')">
            <template #content>
              <div class="space-y-4 max-h-[400px] overflow-y-auto">
                <div v-for="(bill, index) in patientData.billing" :key="index" class="p-4 border rounded-lg">
                  <div class="flex justify-between items-center mb-2">
                    <p class="font-semibold">{{ bill.date }}</p>
                    <span class="px-2 py-1 bg-red-100 text-red-800 rounded-full text-sm">{{ bill.amount }}</span>
                  </div>
                  <p><strong>Status:</strong> {{ bill.status }}</p>
                  <p><strong>Insurance:</strong> {{ bill.insurance }}</p>
                </div>
              </div>
            </template>
          </ExpandableSection>
  
          <!-- Activity Log -->
          <ExpandableSection title="Activity Log" :isOpen="isSectionOpen('activity-log')" @toggle="toggleSection('activity-log')">
            <template #content>
              <div class="space-y-4 max-h-[400px] overflow-y-auto">
                <div v-for="(log, index) in patientData.activityLog" :key="index" class="p-4 border rounded-lg">
                  <p class="font-semibold">{{ log.date }}: {{ log.activity }}</p>
                </div>
              </div>
            </template>
          </ExpandableSection>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ExpandableSection from '@/components/ExpandableSection.vue';
  import { CalendarDays,LogOut , Download, FileText, User, Syringe, Activity, Pill, Bell, DollarSign, Video, Clock, Calendar, Menu, PlusCircle, ChevronDown, ChevronUp } from 'lucide-vue-next'
  import { useUserStore } from '@/stores/user';
  export default {
    name: "Patient",
    setup(){
        const userStore = useUserStore()

        return{
            userStore
        }
    },
    components: {
      ExpandableSection,
      User,
      LogOut,
      PlusCircle
    },
    data() {
      return {
        openSections: ['consultations'],
        patientData: {
          name: 'John Doe',
          age: 35,
          gender: 'Male',
          bloodType: 'O+',
          height: '5\'11"',
          weight: '180 lbs',
          allergies: ['Peanuts', 'Penicillin'],
          emergencyContact: 'Jane Doe - (555) 123-4567',
          consultations: [
            { date: '2023-01-10', doctor: 'Dr. Smith', diagnosis: 'Flu', prescription: 'Tamiflu' },
            { date: '2022-11-15', doctor: 'Dr. Johnson', diagnosis: 'Back Pain', prescription: 'Ibuprofen' },
          ],
          labReports: [
            { date: '2023-02-20', test: 'Blood Test', result: 'Normal' },
            { date: '2023-05-12', test: 'X-Ray', result: 'No Issues' },
          ],
          vaccinations: [
            { name: 'Tetanus', date: '2020-08-01', nextDue: '2025-08-01' },
            { name: 'Flu Shot', date: '2022-09-15', nextDue: '2023-09-15' },
          ],
          medications: [
            { name: 'Lisinopril', dosage: '10mg', frequency: 'Once a day' },
            { name: 'Metformin', dosage: '500mg', frequency: 'Twice a day' },
          ],
          upcomingAppointments: [
            { date: '2023-10-25', doctor: 'Dr. Williams', time: '10:00 AM', reason: 'Check-up' },
            { date: '2023-11-05', doctor: 'Dr. Evans', time: '2:30 PM', reason: 'Follow-up' },
          ],
          billing: [
            { date: '2023-09-10', amount: '$250', status: 'Paid', insurance: 'Blue Cross' },
            { date: '2023-10-01', amount: '$500', status: 'Pending', insurance: 'Aetna' },
          ],
          activityLog: [
            { date: '2023-10-10', activity: 'Checked into hospital' },
            { date: '2023-10-11', activity: 'Lab tests conducted' },
          ],
        },
      };
    },
    computed: {
      initials() {
        return this.patientData.name
          .split(' ')
          .map(name => name.charAt(0).toUpperCase())
          .join('');
      },
    },
    methods: {
        logOut(){
           this.userStore.removeToken();
           this.$router.push('/login') ;

        },
      toggleSection(section) {
        const index = this.openSections.indexOf(section);
        if (index !== -1) {
          this.openSections.splice(index, 1);
        } else {
          this.openSections.push(section);
        }
      },
      isSectionOpen(section) {
        return this.openSections.includes(section);
      },
      handleRequestAppointment() {
        alert('Request an appointment feature coming soon!');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add any specific styles here */
  </style>
  