<template>
    <div v-if="isModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md m-4">
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
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              v-model="prescription.weight"
              placeholder="Weight"
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <textarea
              v-model="prescription.dosage"
              placeholder="Dosage and notes"
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
          </div>
        </div>
        <button
          @click="addPrescription"
          class="mt-4 px-4 py-2 border rounded-md hover:bg-gray-100 flex items-center transition duration-300"
        >
          <PlusIcon class="h-4 w-4 mr-2" /> Add Another Prescription
        </button>
        <div class="flex justify-between mt-4">
          <button
            @click="$emit('close-modal')"
            class="px-4 py-2 border rounded-md hover:bg-gray-100 transition duration-300"
          >
            Cancel
          </button>
          <button
            @click="sendPrescriptions"
            class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 flex items-center transition duration-300"
          >
            <SendIcon class="h-4 w-4 mr-2" /> Send Prescriptions
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import {  PlusIcon,SendIcon } from 'lucide-vue-next';
  import { useUserStore } from "@/stores/user";
  
  export default {
    name: "Prescription",
    props: {
      isModalOpen: {
        type: Boolean,
        required: true,
      },
      sessionId: {
        type: String,
        required: true,
      },
    },
    components:{
        PlusIcon,
        SendIcon
    },
    data() {
      return {
        prescriptions: [{ medication: "", weight: "", dosage: "" }],
        newMessage: "",
        userStore: useUserStore()
      };
    },
    computed:{
        patientName() {
      return `${this.userStore.activePatient.first_name} ${this.userStore.activePatient.last_name}`;
    },
    doctorName() {
      return `Dr. ${this.userStore.activeDoctor.first_name}`;
    },
    },
    methods: {
      async sendPrescriptions() {
        try {
          const response = await axios.post(
            `/api/consultation/sessions/medications/${this.sessionId}/`,
            this.prescriptions
          );
          if (response.status === 201) {
            this.newMessage = response.data.message;
            this.$emit("notify", this.newMessage);
            this.$emit("close-modal");
          }
        } catch (error) {
          if (error.response?.data?.error) {
            const errorMessage = error.response.data.error;
            this.toastStore.showToast(5000, errorMessage, "bg-red-500");
          }
        }
      },
      addPrescription() {
        this.prescriptions.push({ medication: "", weight: "", dosage: "" });
      },
    },
  };
  </script>
  
