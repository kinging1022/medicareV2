<template>
    <div class="request-reset-container">
      <form @submit.prevent="requestReset" class="request-reset-form">
        <h2 class="form-title">Request Password Reset</h2>
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            placeholder="Enter your email address" 
            required
          >
        </div>
        <button type="submit" class="request-button">Request Reset</button>
      </form>
      <p v-if="message" :class="['message', { 'error': isError }]">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'RequestPasswordReset',
    data() {
      return {
        email: '',
        message: '',
        isError: false
      }
    },
    methods: {
      async requestReset() {
        try {
          const response = await axios.post('/api/auth/users/reset_password/', {
            email: this.email
          })
  
          this.message = 'Password reset email has been sent. Please check your inbox.'
          this.isError = false
  
        } catch (err) {
          if (err.response && err.response.data) {
            this.message = err.response.data.detail || 'An error occurred. Please try again.'
          } else {
            this.message = 'An error occurred. Please try again.'
          }
          this.isError = true
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .request-reset-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f5f5f5;
  }
  
  .request-reset-form {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
  }
  
  .form-title {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #333;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #555;
  }
  
  input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .request-button {
    width: 100%;
    padding: 0.75rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .request-button:hover {
    background-color: #45a049;
  }
  
  .message {
    margin-top: 1rem;
    text-align: center;
  }
  
  .message.error {
    color: #ff0000;
  }
  </style>