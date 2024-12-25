<template>
    <div class="flex-grow overflow-y-auto p-4 mt-16" ref="scrollArea">
      <div class="max-w-3xl mx-auto space-y-4 pb-20">
        <div v-for="message in messages" :key="message.id" 
             :class="{'flex justify-end': message.created_by.role === 'doctor' && message.type !== 'notification', 'flex justify-start': message.created_by.role !== 'doctor' && message.type !== 'notification', 'w-full': message.type === 'notification'}">
          <div v-if="message.type !== 'notification'"
               :class="{'bg-gradient-to-br from-blue-500 to-blue-600 text-white': message.created_by.role === 'doctor', 'bg-white text-gray-800': message.created_by.role !== 'doctor'}"
               class="rounded-lg p-3 max-w-[80%] shadow-md transition-all duration-300 hover:shadow-lg">
            <div v-if="message.type === 'text'" class="text-sm">
              {{ message.body }}
            </div>
            <div v-else-if="message.type === 'image'" class="chat-media-container relative">
              <img :src="message.get_image" alt="Uploaded image" class="chat-media rounded-md w-full h-full object-cover" />
              <div class="absolute top-2 right-2 bg-black bg-opacity-50 rounded-full p-1">
                <ImageIcon class="h-4 w-4 text-white" />
              </div>
            </div>
            <div v-else-if="message.type === 'video'" class="chat-media-container relative">
              <video 
                :src="message.get_video" 
                preload="metadata" 
                class="chat-media rounded-md w-full h-full object-cover"
                @click.stop
              >
                Your browser does not support the video tag.
              </video>
              <div class="absolute inset-0 flex items-center justify-center">
                <button @click="openExpandedVideo(message.get_video)" class="bg-black bg-opacity-50 rounded-full p-3 text-white hover:bg-opacity-75 transition-all duration-300">
                  <PlayIcon class="h-8 w-8" />
                </button>
              </div>
            </div>
            <div v-else-if="message.type === 'file'">
              <a :href="message.body" target="_blank" class="text-blue-200 hover:text-blue-100 underline flex items-center">
                <FileText class="h-4 w-4 mr-2" />
                Download File
              </a>
            </div>
            <p class="text-xs mt-1" :class="{'text-blue-200': message.created_by.role === 'doctor', 'text-gray-500': message.created_by.role !== 'doctor'}">
              {{ formatTimestamp(message.created_at_formatted) }}
            </p>
          </div>
          <div v-else class="w-full bg-yellow-100 py-2 px-4 rounded-md shadow-sm">
            <div class="flex justify-center items-center max-w-4xl mx-auto">
              <div class="text-yellow-700 flex items-center">
                <BellIcon class="h-4 w-4 mr-2 flex-shrink-0" />
                <span>{{ message.body }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <ExpandedVideo 
        v-if="expandedVideoSrc" 
        :videoSrc="expandedVideoSrc" 
        @close="closeExpandedVideo"
      />
    </div>
  </template>
  
  <script>
  import { PlusIcon, BellIcon, PlayIcon, ImageIcon, FileText } from 'lucide-vue-next';
  import { useUserStore } from '@/stores/user';
  import ExpandedVideo from './ExpandedVideo.vue';
  
  export default {
    name: 'ChatMessage',
    props: {
      messages: {
        type: Array,
        required: true,
      },
    },
    components: {
      PlusIcon,
      BellIcon,
      PlayIcon,
      ImageIcon,
      FileText,
      ExpandedVideo,
    },
    data() {
      return {
        userStore: useUserStore(),
        timestampInterval: null,
        expandedVideoSrc: null,
      };
    },
    mounted() {
      this.scrollToBottom();
      this.timestampInterval = setInterval(() => {
        this.$forceUpdate();
      }, 60000);
    },
    beforeUnmount() {
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
      scrollToBottom() {
        if (this.$refs.scrollArea) {
          this.$nextTick(() => {
            this.$refs.scrollArea.scrollTop = this.$refs.scrollArea.scrollHeight;
          });
        }
      },
      openExpandedVideo(videoSrc) {
        this.expandedVideoSrc = videoSrc;
      },
      closeExpandedVideo() {
        this.expandedVideoSrc = null;
      },
    },
    watch: {
      messages: {
        handler() {
          this.scrollToBottom();
        },
        deep: true,
      },
    },
  };
  </script>
  
  <style scoped>
  .chat-media-container {
    width: 100%;
    max-width: 300px;
    height: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    position: relative;
  }
  
  .chat-media {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  </style>
  