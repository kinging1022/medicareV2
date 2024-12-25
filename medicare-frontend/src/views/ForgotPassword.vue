<template>
    <div class="forgot-password-container">
      <form @submit.prevent="resetPassword" class="forgot-password-form">
        <h2 class="form-title">Reset Password</h2>
        <div class="form-group">
          <label for="password">New Password</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            placeholder="Enter your new password" 
            required
          >
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm New Password</label>
          <input 
            id="confirmPassword"
            v-model="confirmPassword" 
            type="password" 
            placeholder="Confirm your new password" 
            required
          >
        </div>
        <button type="submit" class="reset-button">Reset Password</button>
      </form>
      <p v-if="message" :class="['message', { 'error': isError }]">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'ForgotPassword',
    data() {
      return {
        password: '',
        confirmPassword: '',
        message: '',
        isError: false
      }
    },
    methods: {
      async resetPassword() {
        if (this.password !== this.confirmPassword) {
          this.message = 'Passwords do not match.'
          this.isError = true
          return
        }
  
        try {
          const token = this.$route.params.token
          const uid = this.$route.params.uid
          
  
          if (!token || !uid) {
            this.message = 'Invalid reset link.'
            this.isError = true
            return
          }
  
          const response = await axios.post('/api/auth/users/reset_password_confirm/', {
            new_password: this.password,
            re_new_password: this.confirmPassword,
            token: token,
            uid: uid
          })
  
          this.message = 'Password has been reset successfully.'
          this.isError = false
          setTimeout(() => {
            this.$router.push('/login')
          }, 3000)
  
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
  .forgot-password-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f5f5f5;
  }
  
  .forgot-password-form {
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
  
  .reset-button {
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
  
  .reset-button:hover {
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