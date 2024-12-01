<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">Notifications</h1>
      <div class="bg-white shadow-sm rounded-lg overflow-hidden">
        <div class="p-4 bg-gray-50 border-b border-gray-200">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-2 sm:space-y-0">
            <span class="text-lg font-medium text-gray-700">
              {{ unreadCount }} unread notifications
            </span>
            <button
              @click="markAllAsRead"
              class="w-full sm:w-auto px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Mark all as read
            </button>
          </div>
        </div>
        <ul class="divide-y divide-gray-200">
          <li
            v-for="notification in userStore.notifications"
            :key="notification.id"
            :class="[
              'p-4 hover:bg-gray-50 transition duration-150 ease-in-out',
              { 'bg-white': notification.is_read, 'bg-blue-50': !notification.is_read }
            ]"
          >
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center">
              <div class="flex-1">
                <p
                  :class="[
                    'text-sm',
                    { 'font-medium': !notification.is_read, 'text-gray-900': !notification.is_read, 'text-gray-700': notification.is_read }
                  ]"
                >
                  {{ notification.body }}
                </p>
                <p class="text-sm text-gray-500 mt-1">{{ notification.created_at_formatted }}</p>
              </div>

              <!-- Conditional Button -->
              <div class="flex items-center">
                <button
                  v-if="notification.type_of_notification === 'session_start' "
                  @click="joinSession(notification.id)"
                  class="flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 w-full sm:w-auto"
                >
                  <Phone  class="mr-2 w-4 h-4" /> Join Session
                </button>
                <button
                  v-else-if="!notification.is_read"
                  @click="markAsRead(notification.id)"
                  class="ml-4 text-sm text-blue-600 hover:text-blue-800 focus:outline-none focus:underline hidden sm:block"
                >
                  Mark as read
                </button>
              </div>
            </div>

          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

  <script>
import { useUserStore } from '@/stores/user';
import {Phone} from 'lucide-vue-next';
import axios from 'axios';

  export default {
    setup(){
        const userStore = useUserStore();

        return{
            userStore,
        }

    },
    components:{
      Phone 
    },
    data() {
      return {
      
        };
    },
    computed: {
    unreadCount() {
        return this.userStore.user.unread_notification_count
    },
    },
    methods: {
      async joinSession(id) {
          try {
            await this.userStore.getActiveSession();
            const activeSession = this.userStore.activeSession[0];

            if (activeSession) {
              this.$router.push(`/session/${activeSession.id}`);
              this.markAsRead(id)
            } else {
              console.warn("No active session available.");
            }
          } catch (error) {
            console.error("Error while fetching active session:", error);
            alert("Failed to join the session. Please try again later.");
          }
        },

        async markAsRead(id) {
            const notification = this.userStore.notifications.find(n => n.id === id);
            
            if (!notification) {
                console.warn(`Notification with id ${id} not found.`);
                return;
            }

            if (!notification.is_read) {
                try {
                    const response = await axios.post(`/api/notifications/read/${notification.id}/`);

                    if (response && response.status === 200) {
                        this.userStore.markNotificationAsRead(id); 
                        this.userStore.decrementNotificationCount();
                    }
                } catch (error) {
                    if (error.response && error.response.data && error.response.data.error) {
                        console.log(error.response.data.error);
                    } else {
                        console.error('An unexpected error occurred:', error.message || error);
                    }
                }
            }
        },

      
      
      async markAllAsRead() {
        try {
            const response = await axios.post('/api/notifications/read/');

                    if (response && response.status === 200) {
                        this.userStore.markNotificationsAsread()
                        this.userStore.resetNotificationCount()
                    }
                } catch (error) {
                    if (error.response && error.response.data && error.response.data.error) {
                        console.log(error.response.data.error);
                    } else {
                        console.error('An unexpected error occurred:', error.message || error);
                    }
                }
         
      }
    }
  };
  </script>