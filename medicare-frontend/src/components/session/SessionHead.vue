<template>
  <div class="bg-white shadow-md p-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <button @click="goBack" class="mr-2 p-2 rounded-full hover:bg-gray-200 transition-colors duration-200">
          <ArrowLeftIcon class="w-6 h-6 text-gray-600" />
        </button>
        <div :class="[
          'w-12 h-12 rounded-full flex items-center justify-center text-white font-bold mr-4',
          userStore.user.role === 'doctor' ? 'bg-blue-500' : 'bg-green-500'
        ]">
          {{ initials }}
        </div>
        <div>
          <h2 class="text-xl font-semibold text-gray-800">
            {{ userStore.user.role === 'doctor' 
              ? `${patient.first_name} ${patient.last_name}` 
              : `Dr. ${doctor.first_name} ${doctor.last_name}` }}
          </h2>
        </div>
      </div>
      <div class="flex space-x-2" v-if="showButton && userStore.user.role==='doctor'">
        <button 
          @click="addPrescription" 
          class="p-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors duration-200"
        >
          <PlusCircleIcon class="w-6 h-6 sm:w-4 sm:h-4" />
          <span class="hidden sm:inline ml-2">Add Prescription</span>
        </button>
        <button 
          @click="endsession" 
          class="p-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors duration-200"
        >
          <XCircleIcon class="w-6 h-6 sm:w-4 sm:h-4" />
          <span class="hidden sm:inline ml-2">Cancel Session</span>
        </button>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import { PaperclipIcon, SendIcon, PlusCircleIcon, XCircleIcon, ArrowLeftIcon } from 'lucide-vue-next';

  import { useUserStore } from '@/stores/user';
  
  export default {
    name: 'DoctorPatientChat',
    components: {
      PaperclipIcon,
      SendIcon,
      PlusCircleIcon,
      XCircleIcon,
      ArrowLeftIcon
    },
    props: {
      showButton: {
        type: Boolean,
        default: true,
      },
      patient: {
        type: Object,
        required: true,
      },
      doctor: {
        type: Object,
        required: true,
      },
      endsession: {
        type: Function,
      },
    },
    data() {
      return {
        userStore: useUserStore(),
      };
    },
    computed: {
      initials() {
        const target = this.userStore.user.role === 'doctor' ? this.patient : this.doctor;
        return `${target.first_name} ${target.last_name}`
          .split(' ')
          .map((name) => name.charAt(0).toUpperCase())
          .join('');
      },
    },
    methods: {
      addPrescription() {
        this.$emit('openModal');
      },
      goBack() {
      this.$router.go(-1);
    },
    },
  };
  </script>
  
  <style scoped>
  </style>
  