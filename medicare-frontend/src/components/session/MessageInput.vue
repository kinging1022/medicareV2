<template>
  <div class="bg-white border-t border-gray-200 p-4" v-if="isMessageInputVisible">
    <div class="flex items-center">
      <button @click="openFileInput" class="p-2 rounded-full hover:bg-gray-200 transition-colors duration-200">
        <PaperclipIcon class="w-6 h-6 text-gray-600" />
      </button>
      <input 
        ref="fileInput" 
        type="file" 
        accept="image/*,video/*" 
        class="hidden" 
        @change="handleFileUpload"
      >
      <input 
        v-model="newMessage" 
        @keyup.enter="sendMessage" 
        type="text" 
        placeholder="Type a message..." 
        class="flex-1 border border-gray-300 rounded-full px-4 py-2 ml-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
      <button 
        @click="sendMessage" 
        class="ml-2 bg-blue-500 text-white rounded-full p-2 hover:bg-blue-600 transition-colors duration-200"
      >
        <SendIcon class="w-6 h-6" />
      </button>
    </div>
    <div v-if="selectedFile" class="mt-2 flex items-center">
      <span class="text-sm text-gray-600">{{ selectedFile.name }}</span>
      <button 
        @click="removeSelectedFile" 
        class="ml-2 text-red-500 hover:text-red-600"
      >
        <XCircleIcon class="w-4 h-4" />
      </button>
    </div>
  </div>
</template>

<script>
import { PaperclipIcon, SendIcon, PlusCircleIcon, XCircleIcon } from 'lucide-vue-next'

export default {
  name: 'MessageInput',
  components: {
    PaperclipIcon,
    SendIcon,
    PlusCircleIcon,
    XCircleIcon
  },
  props: {
    isMessageInputVisible: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      newMessage: '',
      selectedFile: null
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== '' || this.selectedFile) {
        const formData = new FormData();
        if (this.newMessage.trim() !== '') {
          formData.append('body', this.newMessage.trim());
          formData.append('type', 'text');
        }
        if (this.selectedFile) {
          formData.append('file', this.selectedFile);
        }
        this.$emit('sendmessage', formData);
        this.newMessage = '';
        this.removeSelectedFile();
      }
    },
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
      }
    },
    removeSelectedFile() {
      this.selectedFile = null;
      this.$refs.fileInput.value = '';
    }
  },
};
</script>

<style scoped>
/* Add any scoped styles here if needed */
</style>