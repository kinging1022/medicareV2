<template>
    <div class="container mx-auto py-10 px-4">
      <h1 class="text-3xl font-bold mb-6">Edit Your Profile</h1>
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label for="fullName" class="block text-sm font-medium text-gray-700">Full Name</label>
          <input
            type="text"
            id="fullName"
            v-model="formData.fullName"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            required
          />
          <p v-if="errors.fullName" class="mt-1 text-sm text-red-600">{{ errors.fullName }}</p>
        </div>
  
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            required
          />
          <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
        </div>
  
        <div>
          <label for="dateOfBirth" class="block text-sm font-medium text-gray-700">Date of Birth</label>
          <input
            type="date"
            id="dateOfBirth"
            v-model="formData.dateOfBirth"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            required
          />
          <p v-if="errors.dateOfBirth" class="mt-1 text-sm text-red-600">{{ errors.dateOfBirth }}</p>
        </div>
  
        <div>
          <label for="phoneNumber" class="block text-sm font-medium text-gray-700">Phone Number</label>
          <input
            type="tel"
            id="phoneNumber"
            v-model="formData.phoneNumber"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            required
          />
          <p v-if="errors.phoneNumber" class="mt-1 text-sm text-red-600">{{ errors.phoneNumber }}</p>
        </div>
  
        <div>
          <label for="address" class="block text-sm font-medium text-gray-700">Address</label>
          <textarea
            id="address"
            v-model="formData.address"
            rows="3"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          ></textarea>
        </div>
  
        <div>
          <label for="medicalHistory" class="block text-sm font-medium text-gray-700">Medical History</label>
          <textarea
            id="medicalHistory"
            v-model="formData.medicalHistory"
            rows="4"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          ></textarea>
        </div>
  
        <div>
          <label for="allergies" class="block text-sm font-medium text-gray-700">Allergies</label>
          <input
            type="text"
            id="allergies"
            v-model="formData.allergies"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          />
        </div>
  
        <div>
          <label for="currentMedications" class="block text-sm font-medium text-gray-700">Current Medications</label>
          <textarea
            id="currentMedications"
            v-model="formData.currentMedications"
            rows="3"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          ></textarea>
        </div>
  
        <div>
          <label for="emergencyContact" class="block text-sm font-medium text-gray-700">Emergency Contact</label>
          <input
            type="text"
            id="emergencyContact"
            v-model="formData.emergencyContact"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          />
        </div>
  
        <div>
          <label for="preferredLanguage" class="block text-sm font-medium text-gray-700">Preferred Language</label>
          <select
            id="preferredLanguage"
            v-model="formData.preferredLanguage"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          >
            <option value="English">English</option>
            <option value="Spanish">Spanish</option>
            <option value="French">French</option>
            <option value="German">German</option>
            <option value="Chinese">Chinese</option>
          </select>
        </div>
  
        <div>
          <label for="communicationPreference" class="block text-sm font-medium text-gray-700">Preferred Communication Method</label>
          <select
            id="communicationPreference"
            v-model="formData.communicationPreference"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          >
            <option value="email">Email</option>
            <option value="phone">Phone</option>
            <option value="mail">Mail</option>
          </select>
        </div>
  
        <div class="flex items-center">
          <input
            type="checkbox"
            id="receiveNewsletters"
            v-model="formData.receiveNewsletters"
            class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label for="receiveNewsletters" class="ml-2 block text-sm text-gray-900">
            Receive Newsletters
          </label>
        </div>
  
        <div>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {{ isSubmitting ? "Updating Profile..." : "Update Profile" }}
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        formData: {
          fullName: "",
          email: "",
          dateOfBirth: "",
          phoneNumber: "",
          address: "",
          medicalHistory: "",
          allergies: "",
          currentMedications: "",
          emergencyContact: "",
          preferredLanguage: "English",
          communicationPreference: "email",
          receiveNewsletters: false,
        },
        errors: {},
        isSubmitting: false,
      };
    },
    methods: {
      handleSubmit() {
        if (this.validateForm()) {
          this.isSubmitting = true;
          setTimeout(() => {
            this.isSubmitting = false;
            console.log(this.formData);
            alert("Profile updated successfully!");
          }, 2000);
        }
      },
      validateForm() {
        this.errors = {};
        if (!this.formData.fullName)
          this.errors.fullName = "Full name is required";
        if (
          !this.formData.email ||
          !/\S+@\S+\.\S+/.test(this.formData.email)
        )
          this.errors.email = "Valid email is required";
        if (!this.formData.dateOfBirth)
          this.errors.dateOfBirth = "Date of birth is required";
        if (!this.formData.phoneNumber)
          this.errors.phoneNumber = "Phone number is required";
  
        return Object.keys(this.errors).length === 0;
      },
    },
  };
  </script>
  