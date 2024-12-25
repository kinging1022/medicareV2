import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      first_name: null,
      last_name: null,
      gender: null,
      display_age: null,
      email: null,
      access: null,
      refresh: null,
      role: null,
      dob: null,
      blood_type: null,
      height: null,
      weight: null,
      timezone: null,
      allergies: null,
      emergency_contact: null,
      unread_notification_count: 0,
    },
    notificationSocket: null,
    activeSessionStatus: null,
    latestAppointment: null,
    notifications: [],
    activeSession: {},
    notificationType: null,
    activeDoctor:{first_name:'', last_name:''},
    activePatient:{first_name:'', last_name:''},
  }),

  actions: {
    initWebsocket() {
      if (!this.user.access || this.notificationSocket) return;

      const ws = new WebSocket(`ws://localhost:8000/ws/notifications/?token=${this.user.access}`);
      this.notificationSocket = ws;

      ws.onopen = () => {
        ws.send(
          JSON.stringify({
            action: "list",
            request_id: new Date().getTime(),
          })
        );
      };

      ws.onmessage = (e) => {
        const data = JSON.parse(e.data);

        if (data.action === "list") {
          this.notifications = data.data;
          this.user.unread_notification_count = this.notifications.filter((n) => !n.is_read).length;
          this.saveUserToLocalStorage();
        } else if (data.action === "create") {
          const notification = data.data;
          if (notification.created_for.id === this.user.id) {
            this.notificationType = notification.type_of_notification;
            this.notifications.unshift(notification);
            this.user.unread_notification_count++;
            this.saveUserToLocalStorage();
          }
        }
      };

      ws.onclose = () => {
        this.notificationSocket = null;
      };
    },
    async updateTimezone() {
        try {
            const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            this.timezone = timezone;

            await axios.post('/api/user/update-timezone/', { timezone });
            this.saveUserToLocalStorage();
        } catch (error) {
        }
    },

    async getActiveSession() {

      try{
            const response = await axios.get('/api/consultation/active-session/')
            this.activeSession = response.data
            this.activeSessionStatus = response.data.status
            const users = response.data.users
            this.activePatient= users.find(user => user.role === "patient");
            this.activeDoctor = users.find(user => user.role === "doctor")
            
            
      }catch(error){
        if (error && error.response && error.status === 500){
          this.activeSession = {}
          this.activeSessionStatus = null
        }

      }


  },

    clearActiveSession(){
      this.activeSession = {}
      this.activeSessionStatus = 'ended'

    },

    markNotificationAsRead(id) {
      const notification = this.notifications.find((n) => n.id === id);
      if (notification) notification.is_read = true;
    },

    markNotificationsAsread() {
      this.notifications.forEach((notification) => {
        notification.is_read = true;
      });
    },

    incrementNotificationCount() {
      this.user.unread_notification_count += 1;
      this.saveUserToLocalStorage();
    },

    decrementNotificationCount(count = 1) {
      this.user.unread_notification_count = Math.max(this.user.unread_notification_count - count, 0);
      this.saveUserToLocalStorage();
    },

    resetNotificationCount() {
      this.user.unread_notification_count = 0;
      this.saveUserToLocalStorage();
    },

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
      this.initWebsocket();
      this.getActiveSession();
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
        display_age: null,
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
        unread_notification_count: 0,
        timezone: null
      };
      this.activeSession = {};
      this.activeDoctor = {}
      this.activePatient = {}
      this.notifications = [];
      if (this.notificationSocket) {
        this.notificationSocket.close();
        this.notificationSocket = null;
      }
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

