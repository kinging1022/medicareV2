<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <!-- Header Section -->
    <div class="flex items-center justify-between px-4 py-3 bg-white shadow-md">
      <div class="flex items-center">
        <div class="ml-3">
          <p class="font-semibold">John Doe</p>
          <p class="text-sm text-gray-500">Patient</p>
        </div>
      </div>
      <div v-if="userStore.user.role === 'doctor'" class="flex space-x-2">
        <button class="p-2 rounded-md border border-gray-300 hover:bg-gray-100" aria-label="Start voice call">
          <Phone class="h-4 w-4" />
        </button>
        <button class="p-2 rounded-md border border-gray-300 hover:bg-gray-100" aria-label="Start video call">
          <Video class="h-4 w-4" />
        </button>
        <button
          @click="isModalOpen = true"
          class="p-2 rounded-md border border-gray-300 hover:bg-gray-100"
          aria-label="Add prescription"
        >
          <FileText class="h-4 w-4 mr-2" />
          <span class="hidden sm:inline">Add Prescription</span>
        </button>
        <button
          @click="endSession"
          class="p-2 rounded-md border border-gray-300 hover:bg-gray-100"
          aria-label="End session"
        >
          <X class="h-4 w-4"  color="red"/>
        </button>
      </div>
    </div>

    <!-- Chat Section -->
    <div class="flex-grow p-4 overflow-auto" ref="scrollArea">
      <div v-for="message in messages" :key="message.id">
        <!-- Doctor's Message -->
        <div v-if="message.created_by.role === 'doctor'" class="flex mb-4 justify-end">
          <div v-if="message.type === 'text'" class="rounded-lg p-3 max-w-[80%] bg-blue-100">
            <p class="text-sm">{{ message.body }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ formatTimestamp(message.created_at_formatted) }}</p>
          </div>
          <div v-else class="w-full bg-yellow-100 py-2">
            <div class="flex justify-center items-center max-w-4xl mx-auto">
              <div class="text-yellow-700 px-4">
                <bell-icon class="inline-block mr-2 h-4 w-4" />
                {{ message.body }}
              </div>
            </div>
          </div>
        </div>

        <!-- Other User's Message -->
        <div v-else class="flex mb-4 justify-start">
          <div class="rounded-lg p-3 max-w-[80%] bg-white">
            <p class="text-sm">{{ message.body }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ formatTimestamp(message.created_at_formatted) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Input Section -->
    <form v-if="isMessageInputVisible" @submit.prevent="sendMessage" class="p-4 bg-white">
      <div class="flex space-x-2">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type your message..."
          class="flex-grow px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600" aria-label="Send message">
          <Send class="h-4 w-4 mr-2" />
          <span class="hidden sm:inline">Send</span>
        </button>
      </div>
    </form>

    <!-- Prescription Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-2xl font-bold mb-4">Add Prescription</h2>
        <div class="mb-4">
          <p>Patient: {{ patientName }}</p>
          <p>Doctor: {{ doctorName }}</p>
        </div>
        <div class="h-[300px] overflow-y-auto pr-4 space-y-4">
          <div v-for="(prescription, index) in prescriptions" :key="index" class="space-y-2">
            <input
              v-model="prescription.medication"
              placeholder="Medication name"
              class="w-full px-4 py-2 border rounded-md"
            />
            <input
              v-model="prescription.weight"
              placeholder="Weight"
              class="w-full px-4 py-2 border rounded-md"
            />
            <textarea
              v-model="prescription.dosage"
              placeholder="Dosage and notes"
              class="w-full px-4 py-2 border rounded-md"
            ></textarea>
          </div>
        </div>
        <button @click="addPrescription" class="mt-4 px-4 py-2 border rounded-md hover:bg-gray-100">
          <plus-icon class="inline-block mr-2 h-4 w-4" /> Add Another Prescription
        </button>
        <div class="flex justify-between mt-4">
          <button @click="isModalOpen = false" class="px-4 py-2 border rounded-md hover:bg-gray-100">
            Cancel
          </button>
          <button @click="sendPrescriptions" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
            <send-icon class="inline-block mr-2 h-4 w-4" /> Send Prescriptions
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { Phone, Video, FileText, Send, PlusIcon, SendIcon, BellIcon, X } from 'lucide-vue-next';
import { useUserStore } from '@/stores/user';
import axios from 'axios';


export default {
  name: 'DoctorPatientChat',
  components: {
    Phone,
    Video,
    FileText,
    Send,
    PlusIcon,
    SendIcon,
    BellIcon,
    X,
  },
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
    };
  },
  data() {
    return {
      messages: [],
      newMessage: '',
      isModalOpen: false,
      prescriptions: [{ medication: '', weight: '', dosage: '' }],
      sessionId: this.$route.params.id,
      activeSessionSocket: null,
      isProcessing: false,
      
    };
  },
  computed: {
  isMessageInputVisible() {
    const status = this.userStore.activeSessionStatus || "inactive";
    const notification = this.userStore.notificationType || "none";
    return status === "started" && notification !== "session_stop" && !this.isProcessing;
  },
},

  mounted() {
    this.scrollToBottom();
    this.getMessages();
    this.timestampInterval = setInterval(() => {
    this.$forceUpdate(); // Trigger re-render
  }, 60000);
  },
  beforeDestroy() {
    if (this.activeSessionSocket) {
      this.activeSessionSocket.close();
    };
    
    if (this.timestampInterval) {
    clearInterval(this.timestampInterval);
  }

  },
  methods: {
    formatTimestamp(timestamp) {
      
      const createdAt = new Date(timestamp);
      if (isNaN(createdAt.getTime())) {
        console.error("Invalid timestamp:", timestamp);
        return "Invalid date";
      }

      const now = new Date();
      const diffInMinutes = Math.floor((now - createdAt) / (1000 * 60)); 

      if (diffInMinutes < 1) return "Just now";
      if (diffInMinutes === 1) return "1 minute ago";
      if (diffInMinutes < 60) return `${diffInMinutes} minutes ago`;

      const diffInHours = Math.floor(diffInMinutes / 60);
      if (diffInHours === 1) return "1 hour ago";
      if (diffInHours < 24) return `${diffInHours} hours ago`;

      const diffInDays = Math.floor(diffInHours / 24);
      if (diffInDays === 1) return "1 day ago";
      if (diffInDays < 7) {
        return `${createdAt.toLocaleDateString(undefined, { weekday: "long" })}, ${createdAt.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })}`;
      }

      return createdAt.toLocaleDateString(undefined, { month: "long", day: "numeric" });
    },

    getMessages() {
      const ws = new WebSocket(`ws://localhost:8000/ws/session-chat/?token=${this.userStore.user.access}`);
      this.activeSessionSocket = ws;

      ws.onopen = () => {
        ws.send(
          JSON.stringify({
            action: "list",
            request_id: new Date().getTime(),
          })
        );
      };

      ws.onmessage = (e) => {
        try {
          const response = JSON.parse(e.data);
          console.log('WebSocket response:', response);

          if (!response.action) return;

          if (response.action === "list") {
            const data = response.data;
            console.log(data)
            if (Array.isArray(data) && data.length > 0) {
              this.messages = data[0].messages; 
              console.log(this.messages)
            } else {
              console.error("No data or messages found.");
            }
          } else if (response.action === 'create') {
            const newMessage = response.data;
            this.messages.push(newMessage); 
            console.log('New message added:', newMessage);
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      ws.onclose = (e) => {
        console.warn("WebSocket closed:", e.reason || "No reason provided");
        this.activeSessionSocket = null;
        
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    },

    async endSession() {
      try {
        this.isProcessing = true;
        const response = await axios.post(`/api/consultation/sessions/end/${this.sessionId}/`);
        if (response.status === 200) {
          this.newMessage = response.data.message;
          this.sendNotificationMessage()
          this.userStore.getActiveSession()
        }
      } catch (error) {
        console.error("Error ending session:", error);
        if (error.response?.data?.error) {
          console.log(error.response.data.error);
        }
      }finally {
        this.isProcessing = false;
        if(this.isMessageInputVisible){
          this.$router.push('/dashboard')
        }
      }
    },

    async sendPrescriptions() {
      try {
        const response = await axios.post(`/api/consultation/sessions/medications/${this.sessionId}/`, this.prescriptions);
        if (response.status === 201) {
          this.newMessage = response.data.message;
          this.sendNotificationMessage()
          this.isModalOpen = false;
        }
      } catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
          const errorMessage = error.response.data.error;
          this.toastStore.showToast(5000, errorMessage, 'bg-red-500');
        }
      }
    },

    async sendNotificationMessage() {
      if (this.newMessage.trim() === '') return;
      console.log(this.newMessage);
      const message = this.newMessage.trim();
      try {
        const response = await axios.post(`/api/consultation/session/message/${this.sessionId}/`, {
          body: message,
          type: 'notification'
        });
      } catch (error) {
        console.error("Error sending message:", error);
      }
      this.newMessage = '';
    },


    async sendMessage() {
      if (this.newMessage.trim() === '') return;
      console.log(this.newMessage);
      const message = this.newMessage.trim();
      try {
        const response = await axios.post(`/api/consultation/session/message/${this.sessionId}/`, {
          body: message,
          type: 'text'
        });
      } catch (error) {
        console.error("Error sending message:", error);
      }
      this.newMessage = '';
    },

    addPrescription() {
      this.prescriptions.push({ medication: '', weight: '', dosage: '' });
    },
    scrollToBottom() {
      if (this.$refs.scrollArea) {
        this.$refs.scrollArea.scrollTop = this.$refs.scrollArea.scrollHeight;
      }
    },
  },

  updated() {
    this.scrollToBottom();
  },
};
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>

   