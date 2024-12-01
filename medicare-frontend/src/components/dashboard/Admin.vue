<template>
    <div class="container mx-auto p-4">
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold">Administrator Dashboard</h1>
        <p class="text-gray-600">Welcome back, {{userStore.user.first_name}} {{userStore.user.last_name}}</p>
      </header>
  
      <div class="space-y-6">
        <!-- Personal Information Section -->
        <DahboardProfile/>
        <!-- Dashboard Section -->
        <div class="py-10">
          <header>
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <h1 class="text-3xl font-bold leading-tight text-gray-900">Dashboard</h1>
            </div>
          </header>
          <main>
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
              <div class="px-4 py-8 sm:px-0">
                <div class="grid grid-cols-1 gap-4 items-start lg:grid-cols-3 lg:gap-8">
                  <!-- Left column -->
                  <div class="grid grid-cols-1 gap-4 lg:col-span-2">
                    <!-- Incoming Appointments -->
                    <section aria-labelledby="incoming-appointments-title">
                      <div class="rounded-lg bg-white overflow-hidden shadow">
                        <div class="p-6">
                          <h2 class="text-lg font-medium text-gray-900" id="incoming-appointments-title">Incoming Appointments</h2>
                          <div class="mt-6 flow-root">
                            <ul class="-my-5 divide-y divide-gray-200">
                              <li v-for="appointment in appointmentList" :key="appointment.id" class="py-5">
                                <div class="flex items-center space-x-4">
                                  <div class="flex-shrink-0">
                                    <Calendar class="h-8 w-8 text-indigo-600" />
                                  </div>
                                  <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium text-gray-900 truncate">{{ appointment.created_by.first_name}} {{ appointment.created_by.last_name}}</p>
                                    <p class="text-sm text-gray-500 truncate">{{ appointment.created_at_formatted }}</p>
                                    <p v-if="appointment.created_for" class="text-sm text-gray-500 truncate"> For - Dr {{ appointment.created_for.first_name }} {{ appointment.created_for.last_name }}</p>
                                  </div>
                                  <div>
                                    <button
                                      @click="openAssignModal(appointment)"
                                      class="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                    >
                                      Assign Doctor
                                    </button>
                                    <button
                                      @click="handleRejectAppointment(appointment.id)"
                                      class="ml-2 inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                                    >
                                      Reject
                                    </button>
                                  </div>
                                </div>
                              </li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </section>
  
                    <!-- Hospital Stats -->
                    <section aria-labelledby="hospital-stats-title">
                      <div class="rounded-lg bg-white overflow-hidden shadow">
                        <div class="p-6">
                          <h2 class="text-lg font-medium text-gray-900" id="hospital-stats-title">Hospital Stats</h2>
                          <div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                            <div class="bg-indigo-50 overflow-hidden shadow rounded-lg">
                              <div class="p-5">
                                <div class="flex items-center">
                                  <div class="flex-shrink-0">
                                    <Users class="h-6 w-6 text-indigo-600" aria-hidden="true" />
                                  </div>
                                  <div class="ml-5 w-0 flex-1">
                                    <dl>
                                      <dt class="text-sm font-medium text-gray-500 truncate">Total Patients</dt>
                                      <dd class="text-lg font-medium text-gray-900">12,345</dd>
                                    </dl>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div class="bg-indigo-50 overflow-hidden shadow rounded-lg">
                              <div class="p-5">
                                <div class="flex items-center">
                                  <div class="flex-shrink-0">
                                    <Video class="h-6 w-6 text-indigo-600" aria-hidden="true" />
                                  </div>
                                  <div class="ml-5 w-0 flex-1">
                                    <dl>
                                      <dt class="text-sm font-medium text-gray-500 truncate">Active Telemedicine Sessions</dt>
                                      <dd class="text-lg font-medium text-gray-900">24</dd>
                                    </dl>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div class="bg-indigo-50 overflow-hidden shadow rounded-lg">
                              <div class="p-5">
                                <div class="flex items-center">
                                  <div class="flex-shrink-0">
                                    <Clock class="h-6 w-6 text-indigo-600" aria-hidden="true" />
                                  </div>
                                  <div class="ml-5 w-0 flex-1">
                                    <dl>
                                      <dt class="text-sm font-medium text-gray-500 truncate">Average Wait Time</dt>
                                      <dd class="text-lg font-medium text-gray-900">15 minutes</dd>
                                    </dl>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </section>
                  </div>
  
                  <!-- Right column -->
                  <div class="grid grid-cols-1 gap-4">
                    <!-- Available Doctors -->
                    <section aria-labelledby="available-doctors-title">
                      <div class="rounded-lg bg-white overflow-hidden shadow">
                        <div class="p-6">
                          <h2 class="text-lg font-medium text-gray-900" id="available-doctors-title">Available Doctors</h2>
                          <div class="mt-6 flow-root">
                            <ul class="-my-5 divide-y divide-gray-200">
                              <li v-for="doctor in mockDoctors" :key="doctor.id" class="py-4">
                                <div class="flex items-center space-x-4">
                                  <div class="flex-shrink-0">
                                    <User class="h-8 w-8 text-indigo-600" />
                                  </div>
                                  <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium text-gray-900 truncate">{{ doctor.name }}</p>
                                    <p class="text-sm text-gray-500 truncate">{{ doctor.specialty }}</p>
                                  </div>
                                  <div>
                                    <span v-if="doctor.status === 'Available'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                      <CheckCircle class="mr-1 h-4 w-4" />
                                      Available
                                    </span>
                                    <span v-else-if="doctor.status === 'In Session'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                      <Clock class="mr-1 h-4 w-4" />
                                      In Session
                                    </span>
                                    <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                      <XCircle class="mr-1 h-4 w-4" />
                                      Away
                                    </span>
                                  </div>
                                </div>
                              </li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </section>
  
                    <!-- Quick Actions -->
                    <section aria-labelledby="quick-actions-title">
                      <div class="rounded-lg bg-white overflow-hidden shadow">
                        <div class="p-6">
                          <h2 class="text-lg font-medium text-gray-900" id="quick-actions-title">Quick Actions</h2>
                          <div class="mt-6 grid grid-cols-1 gap-3">
                            <button
                              type="button"
                              class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                            >
                              Generate Daily Report
                            </button>
                            <button
                              type="button"
                              class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                            >
                              Manage Doctor Schedules
                            </button>
                            <button
                              type="button"
                              class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                            >
                              View Emergency Cases
                            </button>
                          </div>
                        </div>
                      </div>
                    </section>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
  
      <!-- Assign Doctor Modal -->
      <div v-if="showModal" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="closeModal"></div>
  
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
  
          <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                  <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                    
                    Assign Doctor to Patient
                  </h3>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      Patient: {{ selectedAppointment ? `${selectedAppointment.created_by.first_name} ${selectedAppointment.created_by.last_name}` : '' }}
                    </p>
                    <p class="text-sm text-gray-500">
                      created: {{ selectedAppointment ? selectedAppointment.created_at_formatted : '' }}
                    </p>
                  </div>
                  <div  class="mt-4">
                    <label for="doctor-select" class="block text-sm font-medium text-gray-700">Select Doctor</label>
                    <select id="doctor-select" v-model="selectedDoctor" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                      <option v-for="doctor in doctors" :key="doctor.id" :value="doctor">
                        Dr {{ doctor.first_name }} - {{ doctor.last_name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button @click="assignDoctor" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm">
                Assign and Create Consultation
              </button>
              <button @click="closeModal" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { LogOut, Bell, Calendar, CheckCircle, Clock, Users, Video, XCircle,  KeyRound,  User,  PlusCircle,  } from 'lucide-vue-next';
  
  import { useUserStore } from '@/stores/user';
  import DahboardProfile from './DahboardProfile.vue';
  export default {
    name: "Admin",
    setup() {
      const userStore = useUserStore()
  
      return {
        userStore
      }
    },
    mounted() {
      this.getAppointments(),
      this.getDoctors()
    },
    components: {
      DahboardProfile,
      User,
      LogOut,
      PlusCircle,
      KeyRound,
      Bell,
      Calendar,
      CheckCircle,
      Clock,
      User,
      Users,
      Video,
      XCircle
    },
    data() {
      return {
        appointmentList: [],
        doctors: [],
        mockAppointments: [
          { id: 1, patientName: 'Alice Johnson', date: '2023-10-26', time: '09:00', reason: 'Follow-up checkup' },
          { id: 2, patientName: 'Bob Smith', date: '2023-10-26', time: '10:30', reason: 'Chronic pain consultation' },
          { id: 3, patientName: 'Carol Williams', date: '2023-10-26', time: '14:00', reason: 'Annual physical' },
          { id: 4, patientName: 'David Brown', date: '2023-10-27', time: '11:00', reason: 'Skin rash examination' },
        ],
        mockDoctors: [
          { id: 1, name: 'Dr. Emily Clark', specialty: 'General Practitioner', status: 'Available' },
          { id: 2, name: 'Dr. Michael Lee', specialty: 'Cardiologist', status: 'In Session' },
          { id: 3, name: 'Dr. Sarah Johnson', specialty: 'Pediatrician', status: 'Available' },
          { id: 4, name: 'Dr. Robert Chen', specialty: 'Dermatologist', status: 'Away' },
        ],
        showModal: false,
        selectedAppointment: null,
        selectedDoctor: null,
      };
    },
    computed: {
      initials() {
        return `${this.userStore.user.first_name} ${this.userStore.user.last_name}`
          .split(' ')
          .map(name => name.charAt(0).toUpperCase())
          .join('');
      },
    },
    methods: {
      getDoctors(){
            const ws = new WebSocket('ws://localhost:8000/ws/users/')

            ws.onopen = () =>{
                ws.send(
                    JSON.stringify({
                        action:'list',
                        request_id : new Date().getTime()
                    })
                )
            }
            ws.onmessage = (e) => {

            
                const response = JSON.parse(e.data);
                if (response.action === 'list') {
                    let users = response.data;
                    this.doctors = []; 
                    for (const user of users) { 
                        if (user.role === 'doctor') {
                            this.doctors.push(user); 
                            }
                        }
                        console.log(this.doctors);
                    }
                };
            },
    getAppointments() {
        const token = this.userStore.user.access
        const ws = new WebSocket(`ws://localhost:8000/ws/appointments/?token=${token}`);
  
        ws.onopen = () => {
          console.log('WebSocket connection established');
          ws.send(
            JSON.stringify({
              action: 'list',
              request_id: new Date().getTime()
            })
          )
        }
        ws.onmessage = (e) => {
          const allData = JSON.parse(e.data)
          if (allData.action === 'list') {
            const appointments = allData.data
            console.log(appointments)
            if(Array.isArray(appointments)){
                this.appointmentList = appointments.filter(appointment => appointment.status === 'sent')
            }else {
            console.error("Unexpected format for consultations:", appointments);
          }
            
           
          } else if (allData.action === "create") {
            this.appointmentList.push(allData.data)
          }
        }
      },
      handleRequestAppointment() {
        alert('Request an appointment feature coming soon!');
      },
      openAssignModal(appointment) {
        this.selectedAppointment = appointment;
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
        this.selectedAppointment = null;
        this.selectedDoctor = null;
      },
      async assignDoctor() {
        if (this.selectedDoctor && this.selectedAppointment) {
            
            const appointmentID = this.selectedAppointment.id
          
            try{
                const newResponse = await axios.post(`/api/consultation/create/${appointmentID}/`)
                console.log(newResponse.data)

            }catch(error){
                 console.log(error)
            }
          
          // Remove the appointment from the list
          this.appointmentList = this.appointmentList.filter(app => app.id !== this.selectedAppointment.id);
          
          this.closeModal();
        } else {
          alert('Please select a doctor');
        }
      },
      handleRejectAppointment(appointmentId) {
        this.appointments = this.appointments.filter(app => app.id !== appointmentId);
        console.log(`Rejected appointment ${appointmentId}`);
      }
    },
  };
  </script>
  
  <style scoped>
  /* Add any specific styles here */
  </style>