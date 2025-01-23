<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <!-- Chat Header -->
    <SessionHead
      :show-button ="showButton"
      :patient="patient"
      :doctor="doctor"

  />

    <!-- Chat Messages -->
     <ChatMessage
     :messages="messages"
     />

    

    <!-- Chat Input -->
   
  </div>
</template>


<script>
import { useUserStore } from '@/stores/user';
import SessionHead from '@/components/session/SessionHead.vue';
//import MessageInput from '@/components/session/MessageInput.vue';
//import ChatMessage from '@/components/session/ChatMessage.vue';
import ChatMessage from '@/components/session/ChatMessage.vue';
import { PaperclipIcon, SendIcon, PlusCircleIcon, XCircleIcon } from 'lucide-vue-next'

import axios from 'axios';

export default {
  name: 'DoctorPatientChat',
  components: {
    //Prescription,
    SessionHead,
    //MessageInput,
    ChatMessage,
    //SessionHead
    PaperclipIcon,
    SendIcon,
    PlusCircleIcon,
    XCircleIcon
  },
  data() {
    return {
      userStore: useUserStore(),
      messages: [],
      showButton:false,
      newMessage: '',
      isModalOpen: false,
      sessionId: this.$route.params.id,
      activeSessionSocket: null,
      patient:{first_name:'', last_name:''},
      doctor: {first_name:'', last_name:''},

    };
  },
  mounted() {
    this.getMessages();
    this.scrollToBottom()
    
  },
  computed: {
    isMessageInputVisible() {
      const status = this.userStore.activeSessionStatus || "inactive";
      const notification = this.userStore.notificationType || "none";
      return status === "started" && notification !== "session_stop" 
    },
    initials() {
    return `${this.userStore.user.first_name} ${this.userStore.user.last_name}`
      .split(' ')
      .map(name => name.charAt(0).toUpperCase())
      .join('');
  },
  },

  
  methods: {
      async getMessages(){

      try{
          const response = await axios.get(`/api/consultation/${this.sessionId}/`)
          console.log('new',response.data)
          const users = response.data.users
          this.patient = users.find(user => user.role === "patient");
          this.doctor = users.find(user => user.role === "doctor")
          this.messages = response.data.messages
          
      }catch(error){

      }


      },
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
    scrollToBottom() {
      this.$nextTick(() => {
        this.$refs.chatContainer.scrollTop = this.$refs.chatContainer.scrollHeight
      })
    },
    
   
  },
  
};
</script>
 <style scoped>
 /* Custom scrollbar styles */
 .overflow-y-auto {
   scrollbar-width: thin;
   scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
 }
 
 .overflow-y-auto::-webkit-scrollbar {
   width: 6px;
 }
 
 .overflow-y-auto::-webkit-scrollbar-track {
   background: transparent;
 }
 
 .overflow-y-auto::-webkit-scrollbar-thumb {
   background-color: rgba(156, 163, 175, 0.5);
   border-radius: 3px;
 }
 </style>








