<template>
    <div class="container mx-auto p-4">
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold">Administrator Dashboard</h1>
        <p class="text-gray-600">Welcome back, {{userStore.user.first_name  }}  {{userStore.user.last_name}}</p>
      </header>
  
      <div class="space-y-6">
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-2xl font-semibold mb-4">Personal Information</h2>
          <div class="flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4 mb-4">
            <div class="w-20 h-20 bg-gray-300 rounded-full flex items-center justify-center text-2xl font-bold">
              {{ initials }}
            </div>
            <div class="text-center sm:text-left">
              <h3 class="text-xl font-semibold">{{userStore.user.first_name  }}  {{userStore.user.last_name}}</h3>
              <p class="text-gray-600">
                {{ userStore.user.age }} years old • {{ userStore.user.gender }}
              </p>
            </div>
          </div>
          <div class="flex flex-col sm:flex-row justify-start space-y-4 sm:space-y-0 sm:space-x-4">
            <button
              @click="handleRequestAppointment"
              class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
            >
            <PlusCircle class="inline-block mr-2 h-4 w-4" />
              Request Appointment
            </button>
            <RouterLink :to="{name:'updatepassword'}" class="px-4 py-2 bg-emerald-500 text-white rounded-md hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-center focus:ring-opacity-50">
                <KeyRound class="inline-block mr-2 h-4 w-4" />
                Edit Password
            </RouterLink>
            <button @click="logOut()" class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50">
                <LogOut class="inline-block mr-2 h-4 w-4" />
                Logout
            </button>
          </div>
        </div>
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
                          <li v-for="appointment in appointments" :key="appointment.id" class="py-5">
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
                                  @click="handleAssignDoctor(appointment.id, doctors[0].id)"
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
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { LogOut, Bell, Calendar, CheckCircle, Clock, Users, Video, XCircle, Download, KeyRound, FileText, User, Syringe, Activity, Pill, DollarSign, Menu, PlusCircle, ChevronDown, ChevronUp, KeyRoundIcon } from 'lucide-vue-next';

  import { useUserStore } from '@/stores/user';
  export default {
    name: "Admin",
    setup(){
        const userStore = useUserStore()

        return{
            userStore
        }
    },
    mounted(){
        this.getAppointments()
    },
    components: {
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
        appointments:[],
            mockAppointments :[
                { id: 1, patientName: 'Alice Johnson', date: '2023-10-26', time: '09:00', reason: 'Follow-up checkup' },
                { id: 2, patientName: 'Bob Smith', date: '2023-10-26', time: '10:30', reason: 'Chronic pain consultation' },
                { id: 3, patientName: 'Carol Williams', date: '2023-10-26', time: '14:00', reason: 'Annual physical' },
                { id: 4, patientName: 'David Brown', date: '2023-10-27', time: '11:00', reason: 'Skin rash examination' },
            ],
            
            mockDoctors :[
                { id: 1, name: 'Dr. Emily Clark', specialty: 'General Practitioner', status: 'Available' },
                { id: 2, name: 'Dr. Michael Lee', specialty: 'Cardiologist', status: 'In Session' },
                { id: 3, name: 'Dr. Sarah Johnson', specialty: 'Pediatrician', status: 'Available' },
                { id: 4, name: 'Dr. Robert Chen', specialty: 'Dermatologist', status: 'Away' },
            ]
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
        logOut(){
           this.userStore.removeToken();
           this.$router.push('/login') ;

        },
        getAppointments(){
            const ws = new WebSocket('ws://localhost:8000/ws/appointments/')

            ws.onopen = () => {
                ws.send(
                    JSON.stringify({
                        action: 'list',
                        request_id : new Date().getTime()

                    })
                )
            }
            ws.onmessage = (e) => {
                const allData = JSON.parse(e.data)
                if (allData.action === 'list'){
                    //console.log(allData)
                    this.appointments = allData.data
                } else if(allData.action === "create") {
                    console.log(allData)
                    this.appointments.push(allData.data)
                }
            }
            
        },
        handleRequestAppointment() {
            alert('Request an appointment feature coming soon!');
        },
        handleAssignDoctor(appointmentId, doctorId) {
            // In a real app, you would make an API call here
            this.appointments = this.appointments.filter(app => app.id !== appointmentId)
            console.log(`Assigned appointment ${appointmentId} to doctor ${doctorId}`)
        },
        handleRejectAppointment(appointmentId) {
            // In a real app, you would make an API call here
            this.appointments = this.appointments.filter(app => app.id !== appointmentId)
            console.log(`Rejected appointment ${appointmentId}`)
        }
    },
  };
  </script>
  
  <style scoped>
  /* Add any specific styles here */
  </style>
  