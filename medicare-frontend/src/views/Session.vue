<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <!-- Fixed Header Section -->
    <SessionHead
    :show-button ="showButton"
    @open-modal="handleModal"
    :patient="userStore.activePatient"
    :doctor="userStore.activeDoctor"
    :endsession="endSession"

    />
    <!-- Scrollable Chat Section -->
     <ChatMessage
     :messages="messages"
     />
    
    
    <!-- Fixed Message Input Section -->
    <MessageInput 
      :isMessageInputVisible="isMessageInputVisible"
      @sendmessage=handleSendMessage
    />

    <!-- Prescription Modal -->
     <Prescription
     :isModalOpen="isModalOpen"
     :sessionId="sessionId"
     @close-modal="isModalOpen = false"
     @notify="handleNotification"
     />
    
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user';
import Prescription from '@/components/modal/Prescription.vue';
import SessionHead from '@/components/session/SessionHead.vue';
import MessageInput from '@/components/session/MessageInput.vue';
import ChatMessage from '@/components/session/ChatMessage.vue';
import axios from 'axios';

export default {
  name: 'DoctorPatientChat',
  components: {
    Prescription,
    SessionHead,
    MessageInput,
    ChatMessage
  },
  data() {
    return {
      userStore: useUserStore(),
      messages: [],
      isModalOpen: false,
      showButton:true,
      sessionId: this.$route.params.id,
      activeSessionSocket: null,
  

    };
  },
  mounted() {
    this.getMessages();
    
  },
    beforeUnmount() {
    if (this.activeSessionSocket) {
      this.activeSessionSocket.close();
    }
    
  },
  computed: {
    isMessageInputVisible() {
      const status = this.userStore.activeSessionStatus || "inactive";
      const notification = this.userStore.notificationType || "none";
      return status === "started" && notification !== "session_stop" 
    },
  },
  
  methods: {
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

          if (!response.action) return;

          if (response.action === "list") {
            const data = response.data;
            console.log(data)
            if (Array.isArray(data) && data.length > 0) {
              this.messages = data[0].messages; 
            } else {
              console.error("No data or messages found.");
            }
          } else if (response.action === 'create') {
            const newMessage = response.data;
            this.messages.push(newMessage); 
            console.log('New message added:', newMessage);
            if(newMessage.type ==='notification' && this.userStore.notificationType === 'session_stop'){
              this.userStore.clearActiveSession()
            }
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
    handleModal(){
      this.isModalOpen = true
    },
    async endSession(){
      try{
        const response = await axios.post(`/api/consultation/sessions/end/${this.sessionId}/`)
        const message = response.data.message
        this.handleNotification(message)
        this.userStore.clearActiveSession()

      }catch(error){

      }
    },
    
    async handleSendMessage(formData) {
      try {
        const response = await axios.post(`/api/consultation/session/message/${this.sessionId}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Message sent successfully:', response.data);
      } catch (error) {
        console.error("Error sending message:", error);
      }
    },

    handleFileMessage(file) {
      const formData = new FormData();
      formData.append('file', file);
      this.handleSendMessage(formData);
    },

    handleNotification(message) {
      const formData = new FormData();
      formData.append('body', message.trim());
      formData.append('type', 'notification');
      this.handleSendMessage(formData);
    },

    async handleTextMessage(message) {
      const formData = new FormData();
      formData.append('body', message.trim());
      formData.append('type', 'text');
      this.handleSendMessage(formData);
    },
   
  },
  
};
</script>




