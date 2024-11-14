import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore({
  id: "user",

  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      first_name: null,
      last_name: null,
      gender: null,
      age: null,
      email: null,
      access: null,
      refresh: null,
      role: null,
      dob: null,
      blood_type: null,
      height: null,
      weight: null,
      allergies: null,
      emergency_contact: null,
    },
  }),

  actions: {
    initStore() {
      const storedUser = localStorage.getItem("user");
      if (storedUser) {
        const parsedUser = JSON.parse(storedUser);
        this.user = { ...this.user, ...parsedUser, isAuthenticated: true };
      }
    },

    setToken(data) {
      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;
      this.saveUserToLocalStorage();
    },

    setUserInfo(user) {
      this.user = { ...this.user, ...user };
      this.saveUserToLocalStorage();
    },

    removeToken() {
      this.user = {
        isAuthenticated: false,
        id: null,
        first_name: null,
        last_name: null,
        gender: null,
        age: null,
        email: null,
        access: null,
        refresh: null,
        role: null,
        dob: null,
        blood_type: null,
        height: null,
        weight: null,
        allergies: null,
        emergency_contact: null,
      };
      localStorage.removeItem("user");
    },

    async refreshToken() {
      try {
        const response = await axios.post("api/auth/token/refresh/", {
          refresh: this.user.refresh,
        });
        this.user.access = response.data.access;
        this.saveUserToLocalStorage();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          console.log("Refresh token expired or invalid. Logging out.");
          this.removeToken();
        } else {
          throw new Error("Token refresh failed");
        }
      }
    },

    saveUserToLocalStorage() {
      localStorage.setItem("user", JSON.stringify(this.user));
    },
  },
});
