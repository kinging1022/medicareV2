<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <div class="flex items-center justify-between px-4 py-3 bg-white shadow-md">
      <div class="flex items-center">
        <div class="ml-3">
          <p class="font-semibold">John Doe</p>
          <p class="text-sm text-gray-500">Patient</p>
        </div>
      </div>
      <div class="flex space-x-2">
        <button class="p-2 rounded-md border border-gray-300 hover:bg-gray-100" aria-label="Start voice call">
          <Phone class="h-4 w-4" />
        </button>
        <button class="p-2 rounded-md border border-gray-300 hover:bg-gray-100" aria-label="Start video call">
          <Video class="h-4 w-4" />
        </button>
        <button class="p-2 rounded-md border border-gray-300 hover:bg-gray-100" aria-label="Add prescription">
          <FileText class="h-4 w-4 mr-2" />
          <span class="hidden sm:inline">Add Prescription</span>
        </button>
      </div>
    </div>

    <div class="flex-grow p-4 overflow-auto" ref="scrollArea">
            <div v-for="message in messages" :key="message.id">
        <!-- Check if the message was created by the doctor -->
        <div 
          v-if="message.created_by.id === doctorId" 
          class="flex mb-4 justify-end"
        >
          <div class="rounded-lg p-3 max-w-[80%] bg-blue-100">
            <p class="text-sm">{{ message.body }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ message.created_at_formatted }}</p>
          </div>
        </div>

        <!-- Check if the message was created by someone other than the doctor -->
        <div 
          v-else 
          class="flex mb-4 justify-start"
        >
          <div class="rounded-lg p-3 max-w-[80%] bg-white">
            <p class="text-sm">{{ message.body }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ message.created_at_formatted }}</p>
          </div>
        </div>
      </div>

    </div>

    <div class="border-t border-gray-200"></div>

    <form @submit.prevent="sendMessage" class="p-4 bg-white">
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
  </div>
</template>

<script>
import { Phone, Video, FileText, Send } from 'lucide-vue-next'
import { useUserStore } from '@/stores/user';



export default {
  name: 'DoctorPatientChat',
  components: {
    Phone,
    Video,
    FileText,
    Send
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  data() {
    return {
      chatSocket: null,
      messages : [],
      doctorId: null,
      newMessage: ''
    }
  },
  mounted() {
      this.initializeWebSocket();
      this.scrollToBottom();
    },
    beforeDestroy() {
        if (this.chatSocket) {
          this.chatSocket.close();
        }
    },
  methods: {
    initializeWebSocket() {
        const token = this.userStore.user.access;
        console.log(token)
        const sessionId = this.$route.params.id;
        this.chatSocket = new WebSocket(`ws://127.0.0.1:8000/ws/session-chat/?token=${token}`);
        this.chatSocket.onopen = () => {
          const requestId = new Date().getTime();
          this.chatSocket.send(JSON.stringify({ pk: sessionId, action: "join_room", request_id: requestId }));
          this.chatSocket.send(JSON.stringify({ pk: sessionId, action: "retrieve", request_id: requestId }));
          this.chatSocket.send(JSON.stringify({ pk: sessionId, action: "subscribe_to_messages_in_room", request_id: requestId }));
          this.chatSocket.send(JSON.stringify({ pk: sessionId, action: "subscribe_instance", request_id: requestId }));
        };
        this.chatSocket.onmessage = this.handleSocketMessage;
        this.chatSocket.onclose = this.handleSocketClose;
  },
  handleSocketMessage(e) {
    const data = JSON.parse(e.data);
      console.log('message data',data.data)
      switch (data.action) {
        case "retrieve":
          console.log(data.data)
          console.log(data.data.messages)
          //this.roomData = data.data;
          this.messages = data.data.messages;
          const users = data.data.users
          for ( const user of users){
            if(user === this.userStore.user.id){
              this.doctorId = user
            }
          }
          console.log(this.doctorId)
          
          break;
        case "create":
        console.log(data.data)
        const newMessage = data.data
        if(newMessage && newMessage.created_by && newMessage.created_by.id){
          this.messages.push(newMessage)
          this.$nextTick(this.scrollToBottom);
        }else{
          console.warn("New message structure is missing required fields:", newMessage);
        }
          
  
          break;
      }
  },
  handleSocketClose(e) {
    console.error("Chat socket closed unexpectedly. Attempting to reconnect...");
    setTimeout(this.initializeWebSocket, 1000); // Attempt reconnection after 1 second
  },
  sendMessage() {
    if (this.newMessage.trim() === '') return;
    console.log(this.newMessage)
    const message = this.newMessage.trim();
    const requestId = new Date().getTime();
    this.chatSocket.send(JSON.stringify({
      message: message,
      action: "create_message",
      request_id: requestId 
    }));
    this.newMessage = '';
  },

    scrollToBottom() {
      if (this.$refs.scrollArea) {
        this.$refs.scrollArea.scrollTop = this.$refs.scrollArea.scrollHeight
      }
    }
  },

  updated() {
    this.scrollToBottom()
  }
}
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>