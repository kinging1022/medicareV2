<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

  
      <div class="py-10">
        <header>
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 class="text-4xl font-extrabold text-gray-900 leading-tight">
              Welcome, Dr. {{ doctor.name }}
            </h1>
            <p class="mt-2 text-xl text-gray-600">{{ currentDateTime }}</p>
          </div>
        </header>
        <main>
          <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="px-4 py-8 sm:px-0">
              <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 lg:gap-8">
                <!-- Left column -->
                <div class="lg:col-span-2 space-y-6">
                  <!-- Upcoming Appointments -->
                  <section aria-labelledby="upcoming-appointments-title" class="bg-white overflow-hidden shadow-xl rounded-2xl transition-all duration-300 hover:shadow-2xl">
                    <div class="p-6">
                      <h2 class="text-2xl font-semibold text-gray-900 mb-4" id="upcoming-appointments-title">Upcoming Appointments</h2>
                      <div class="flow-root">
                        <ul class="-my-5 divide-y divide-gray-200">
                          <li v-for="appointment in upcomingAppointments" :key="appointment.id" class="py-5">
                            <div class="flex items-center space-x-4">
                              <div class="flex-1 min-w-0">
                                <p class="text-lg font-medium text-gray-900 truncate">
                                  {{ appointment.patientName }}
                                </p>
                                <p class="text-sm text-gray-500 truncate">
                                  {{ appointment.date }} at {{ appointment.time }}
                                </p>
                              </div>
                              <div>
                                <a href="#" class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200">
                                  View Details
                                </a>
                              </div>
                            </div>
                          </li>
                        </ul>
                      </div>
                      <div class="mt-6">
                        <a href="#" class="w-full flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200">
                          View all appointments
                        </a>
                      </div>
                    </div>
                  </section>
  
                  <!-- Patient Queue -->
                  <section aria-labelledby="patient-queue-title" class="bg-white overflow-hidden shadow-xl rounded-2xl transition-all duration-300 hover:shadow-2xl">
                    <div class="p-6">
                      <h2 class="text-2xl font-semibold text-gray-900 mb-4" id="patient-queue-title">Patient Queue</h2>
                      <div class="flow-root">
                        <ul class="-my-5 divide-y divide-gray-200">
                          <li v-for="patient in patientQueue" :key="patient.id" class="py-5">
                            <div class="flex items-center space-x-4">
                              <div class="flex-1 min-w-0">
                                <p class="text-lg font-medium text-gray-900 truncate">
                                  {{ patient.name }}
                                </p>
                                <p class="text-sm text-gray-500 truncate">
                                  Waiting since: {{ patient.waitingTime }}
                                </p>
                              </div>
                              <div>
                                <a href="#" class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-200">
                                  Start Session
                                </a>
                              </div>
                            </div>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </section>
                </div>
  
                <!-- Right column -->
                <div class="space-y-6">
                  <!-- Your Schedule -->
                  <section aria-labelledby="schedule-title" class="bg-white overflow-hidden shadow-xl rounded-2xl transition-all duration-300 hover:shadow-2xl">
                    <div class="p-6">
                      <h2 class="text-2xl font-semibold text-gray-900 mb-4" id="schedule-title">Your Schedule</h2>
                      <div class="flex flex-col items-center justify-center h-40 bg-gray-50 rounded-lg">
                        <Calendar class="h-12 w-12 text-indigo-500 mb-2" />
                        <span class="text-sm text-gray-500">Calendar integration coming soon</span>
                      </div>
                    </div>
                  </section>
  
                  <!-- Recent Patient Records -->
                  <section aria-labelledby="recent-patients-title" class="bg-white overflow-hidden shadow-xl rounded-2xl transition-all duration-300 hover:shadow-2xl">
                    <div class="p-6">
                      <h2 class="text-2xl font-semibold text-gray-900 mb-4" id="recent-patients-title">Recent Patient Records</h2>
                      <div class="flow-root">
                        <ul class="-my-5 divide-y divide-gray-200">
                          <li v-for="record in recentPatientRecords" :key="record.id" class="py-5">
                            <div class="flex items-center space-x-4">
                              <div class="flex-1 min-w-0">
                                <p class="text-sm font-medium text-gray-900 truncate">
                                  {{ record.patientName }}
                                </p>
                                <p class="text-xs text-gray-500 truncate">
                                  Last visit: {{ record.lastVisit }}
                                </p>
                              </div>
                              <div>
                                <a href="#" class="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200">
                                  View
                                </a>
                              </div>
                            </div>
                          </li>
                        </ul>
                      </div>
                      <div class="mt-6">
                        <a href="#" class="w-full flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200">
                          View all records
                        </a>
                      </div>
                    </div>
                  </section>
  
                  <!-- Key Performance Indicators -->
                  <section aria-labelledby="kpi-title" class="bg-white overflow-hidden shadow-xl rounded-2xl transition-all duration-300 hover:shadow-2xl">
                    <div class="p-6">
                      <h2 class="text-2xl font-semibold text-gray-900 mb-4" id="kpi-title">Key Performance Indicators</h2>
                      <div class="grid grid-cols-2 gap-4">
                        <div class="bg-gradient-to-br from-blue-500 to-indigo-600 p-4 rounded-xl text-white">
                          <div class="flex items-center justify-between">
                            <div>
                              <p class="text-sm font-medium opacity-75">Total Patients</p>
                              <p class="text-2xl font-bold mt-1">{{ kpis.totalPatients }}</p>
                            </div>
                            <Users class="h-8 w-8 opacity-75" />
                          </div>
                        </div>
                        <div class="bg-gradient-to-br from-green-500 to-teal-600 p-4 rounded-xl text-white">
                          <div class="flex items-center justify-between">
                            <div>
                              <p class="text-sm font-medium opacity-75">Avg. Consultation</p>
                              <p class="text-2xl font-bold mt-1">{{ kpis.avgConsultationTime }}</p>
                            </div>
                            <Clock class="h-8 w-8 opacity-75" />
                          </div>
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
  </template>
  
  <script>
  import { Bell, Calendar, Clock, Users } from 'lucide-vue-next'
  
  export default {
    name: 'DoctorDashboard',
    components: {
      Bell,
      Calendar,
      Clock,
      Users
    },
    data() {
      return {
        doctor: {
          name: 'Jane Smith',
          specialty: 'General Practitioner',
          
        },
        upcomingAppointments: [
          { id: 1, patientName: 'John Doe',  date: '2023-10-30', time: '09:00 AM' },
          { id: 2, patientName: 'Jane Smith',  date: '2023-10-30', time: '10:30 AM' },
          { id: 3, patientName: 'Bob Johnson', date: '2023-10-30', time: '02:00 PM' },
        ],
        patientQueue: [
          { id: 1, name: 'Alice Brown',  waitingTime: '10 minutes' },
          { id: 2, name: 'Charlie Davis',  waitingTime: '5 minutes' },
        ],
        recentPatientRecords: [
          { id: 1, patientName: 'Eva White',  lastVisit: '2023-10-25' },
          { id: 2, patientName: 'Frank Miller',  lastVisit: '2023-10-23' },
          { id: 3, patientName: 'Grace Taylor',  lastVisit: '2023-10-20' },
        ],
        kpis: {
          totalPatients: '1,234',
          avgConsultationTime: '15 min'
        }
      }
    },
    computed: {
      currentDateTime() {
        const now = new Date()
        return now.toLocaleString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })
      }
    },
    methods: {
      // Add any methods here if needed
    }
  }
  </script>