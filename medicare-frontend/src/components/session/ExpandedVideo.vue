<template>
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-4 w-1/2">
        <div class="relative">
          <video 
            :src="videoSrc" 
            controls 
            class="w-full h-auto"
            @click.stop
          >
            Your browser does not support the video tag.
          </video>
          <button 
            @click="$emit('close')" 
            class="absolute top-2 right-2 bg-black bg-opacity-50 text-white rounded-full p-2 hover:bg-opacity-75 transition-all duration-300"
          >
            <XIcon class="h-6 w-6" />
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { XIcon } from 'lucide-vue-next';
  
  defineProps({
    videoSrc: {
      type: String,
      required: true
    }
  });
  
  defineEmits(['close']);
  </script>
