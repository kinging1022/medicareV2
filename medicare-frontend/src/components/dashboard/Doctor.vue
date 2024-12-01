<template>
  <div class="container mx-auto p-4">
    <header class="mb-6">
      <h1 class="text-2xl md:text-3xl font-bold">Doctor Dashboard</h1>
      <p class="text-gray-600">
        Welcome back, {{ userStore.user.first_name }} {{ userStore.user.last_name }}
      </p>
    </header>

    <div class="space-y-6">
      <DahboardProfile />

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 lg:gap-8">
        <!-- Left column -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Patient Queue -->
          <section aria-labelledby="patient-queue-title" class="bg-white overflow-hidden shadow-xl rounded-2xl transition-all duration-300 hover:shadow-2xl">
            <div class="p-6">
              <h2 class="text-2xl font-semibold text-gray-900 mb-4" id="patient-queue-title">Patient Queue</h2>
              <div class="flow-root">
                <ul class="-my-5 divide-y divide-gray-200">
                  <li
                    v-for="consultation in patientQueue"
                    :key="consultation.id"
                    class="py-5"
                  >
                    <div class="flex flex-col sm:flex-row sm:items-center space-y-3 sm:space-y-0 sm:space-x-4">
                      <div class="flex-1 min-w-0">
                        <p class="text-lg font-medium text-gray-900 truncate">
                          {{ consultation.patient.first_name }}
                        </p>
                        <p class="text-sm text-gray-500 truncate">
                          Waiting since: {{ consultation.created_at_formatted }}
                        </p>
                      </div>
                      <div class="flex space-x-2">
                        <button
                          @click="openComplaintModal(consultation)"
                          class="w-full sm:w-auto inline-flex items-center justify-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
                        >
                          View Complaint
                        </button>
                        <button
                          v-if="userStore.activeSession.length === 0"
                          @click="createSession(consultation)"
                          class="w-full sm:w-auto inline-flex items-center justify-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-200"
                        >
                          Start Session
                        </button>
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
                  <li
                    v-for="record in recentPatientRecords"
                    :key="record.id"
                    class="py-5"
                  >
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
                        <a
                          href="#"
                          class="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
                        >
                          View
                        </a>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
              <div class="mt-6">
                <a
                  href="#"
                  class="w-full flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
                >
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

      <div
        v-if="showComplaintModal"
        class="fixed z-10 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
      >
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div
            class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
            aria-hidden="true"
            @click="closeComplaintModal"
          ></div>

          <span
            class="hidden sm:inline-block sm:align-middle sm:h-screen"
            aria-hidden="true"
            >&#8203;</span
          >

          <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                  <h3
                    class="text-lg leading-6 font-medium text-gray-900"
                    id="modal-title"
                  >
                    Patient Complaint
                  </h3>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      Patient:
                      {{
                        selectedConsultation
                          ? selectedConsultation.patient.first_name +
                            ' ' +
                            selectedConsultation.patient.last_name
                          : ''
                      }}
                    </p>
                    <p class="text-sm text-gray-700 mt-4">
                      Complaint:
                      {{
                        selectedConsultation
                          ? selectedConsultation.appointment.body
                          : ''
                      }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div
              class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse"
            >
              <button
                type="button"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
                @click="closeComplaintModal"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


 <script>
import { Bell, Calendar, Clock, Users, User, KeyRound, LogOut } from 'lucide-vue-next'
import { useUserStore } from '@/stores/user';
import { format, parseISO } from 'date-fns';
import DahboardProfile from './DahboardProfile.vue';
import axios from 'axios';

export default {
  name: 'DoctorDashboard',
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  mounted(){
    this.getOrUpdateConsultations()
  },
  components: {
    DahboardProfile,
    Bell,
    Calendar,
    Clock,
    Users,
    User,
    KeyRound,
    LogOut
  },
  data() {
    return {
      patientQueue:[],
      recentPatientRecords: [
        { id: 1, patientName: 'Eva White',  lastVisit: '2023-10-25' },
        { id: 2, patientName: 'Frank Miller',  lastVisit: '2023-10-23' },
        { id: 3, patientName: 'Grace Taylor',  lastVisit: '2023-10-20' },
      ],
      kpis: {
        totalPatients: '1,234',
        avgConsultationTime: '15 min'
      },
      showComplaintModal: false,
      selectedConsultation: null
    }
  },
  computed: {
    currentDateTime() {
      const now = new Date()
      return now.toLocaleString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    },
    initials() {
      return `${this.userStore.user.first_name} ${this.userStore.user.last_name}`
        .split(' ')
        .map(name => name.charAt(0).toUpperCase())
        .join('');
    }
  },
  methods: {
    formatDate(dateString) {
      try {
        return format(parseISO(dateString), 'MMMM dd, yyyy - hh:mm a');
      } catch (error) {
        console.error('Date parsing error:', error);
        return 'Invalid Date';
      }
    },
    getOrUpdateConsultations(){
      const token = this.userStore.user.access;
      const ws = new WebSocket(`ws://localhost:8000/ws/consultations/?token=${token}`)

      ws.onopen = () => {
        ws.send(
          JSON.stringify({
            action: 'list',
            request_id: new Date().getTime()
          })
        )
      }
      ws.onmessage = (e) => {
        const allData = JSON.parse(e.data);
        if (allData.action === 'list') {
          const consultations = allData.data;
          console.log(consultations)
          if (Array.isArray(consultations)) {
            this.patientQueue = consultations.filter(consultation => 
              consultation.status === 'sent'
            );
          } else {
            console.error("Unexpected format for consultations:", consultations);
          }
        } else if (allData.action === "create") {
          this.patientQueue.push(allData.data);
        }
      };
    },
    openComplaintModal(consultation) {
      this.selectedConsultation = consultation;
      this.showComplaintModal = true;
    },
    closeComplaintModal() {
      this.showComplaintModal = false;
      this.selectedConsultation = null;
    },
    logOut() {
      this.userStore.removeToken();
      this.$router.push('/login');
    },
    async createSession(consultation){
      this.selectedConsultation =  consultation
      const patientID = this.selectedConsultation.patient.id
      const consultationId = this.selectedConsultation.id
      try{
                const newResponse = await axios.post(`/api/consultation/sessions/create/${consultationId}/${patientID}/`)
                //console.log(newResponse.data)

                const sessionId = newResponse.data.id
                console.log(sessionId)

                this.$router.push(`/session/${sessionId}`)
                this.userStore.getActiveSession()



            }catch(error){
                 console.log(error)
            }
    }
  }
}
</script>
