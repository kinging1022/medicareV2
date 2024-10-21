<template>
    <div class="border rounded-lg shadow-md">
      <div
        @click="toggle"
        class="flex justify-between items-center bg-gray-100 p-4 cursor-pointer hover:bg-gray-200"
      >
        <h2 class="text-lg font-semibold">{{ title }}</h2>
        <svg
          :class="isOpen ? 'transform rotate-180' : ''"
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M5.23 7.21a.75.75 0 011.06 0L10 10.44l3.71-3.23a.75.75 0 011.06 1.06l-4.25 3.5a.75.75 0 01-.93 0l-4.25-3.5a.75.75 0 010-1.06z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <transition name="fade">
        <div v-show="isOpen" class="p-4 bg-white border-t">
          <slot name="content" />
        </div>
      </transition>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      title: {
        type: String,
        required: true,
      },
      isOpen: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        isOpen: this.isOpen,
      };
    },
    methods: {
      toggle() {
        this.isOpen = !this.isOpen;
        this.$emit('toggle', this.isOpen);
      },
    },
  };
  </script>
  
  <style scoped>
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s;
  }
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
  </style>
  