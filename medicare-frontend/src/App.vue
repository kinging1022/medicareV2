<template>
  <div class="flex flex-col min-h-screen bg-white">
    <header class="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-sm">
      <div class="container mx-auto px-4 md:px-6 lg:px-8 flex h-16 items-center justify-between">
        <router-link class="flex items-center justify-center" to="#">
          <span class="text-2xl ml-3 font-bold text-gray-900">Medicare</span>
        </router-link>
        <nav class="hidden md:flex items-center space-x-6 text-sm font-medium">
          <router-link
            v-for="item in navigations"
            :key="item.name"
            :to="item.href"
            class="text-gray-600 text-lg hover:text-teal-500 transition-colors"
          >
            {{ item.name }}
          </router-link>
        </nav>
        <div class="flex items-center space-x-4">
          <template v-if="!userStore.user.isAuthenticated">
            <Button @click="logIn" variant="ghost" customClass="text-gray-600 hover:text-teal-500 hidden md:inline-flex">Log In</Button>
            <Button @click="signUp" class="bg-teal-500 text-white hover:bg-teal-600 hidden md:inline-flex">Sign Up</Button>
          </template>
          <div class="flex items-center space-x-4">

              <router-link v-if="sessionId" :to="{name: 'startsession', params:{id:sessionId}}" variant="ghost" size="icon" class="text-gray-600 hover:text-teal-500 relative flex items-center">
                <MailOpen class="h-6 w-6" />
                <span
                  v-if="sessionCount > 0"
                  class="absolute -top-1 -right-1 bg-green-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
                >
                  {{ sessionCount }}
                </span>
              </router-link>
              <router-link to="/dashboard" v-else  variant="ghost" size="icon" class="text-gray-600 hover:text-teal-500 relative flex items-center">
                <Mail class="h-6 w-6" />
            
              </router-link>
              <router-link to="/notification" variant="ghost" size="icon" class="text-gray-600 hover:text-teal-500 relative flex items-center">
                <Bell class="h-6 w-6" />
                <span
                  v-if="notificationCount > 0"
                  class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
                >
                  {{ notificationCount }}
                </span>
              </router-link>

          
        </div>

          <Button
            variant="ghost"
            size="icon"
            class="md:hidden"
            @click="toggleMenu"
          >
            <Menu class="h-6 w-6" />
          </Button>
        </div>
      </div>
      <nav v-if="isMenuOpen" class="md:hidden p-4 bg-white border-t">
        <router-link
          v-for="item in navigations"
          :key="item.name"
          :to="item.href"
          class="block py-2 text-gray-600 hover:text-teal-500"
        >
          {{ item.name }}
        </router-link>
        <template v-if="!userStore.user.isAuthenticated">
          <Button @click="logIn" variant="ghost" class="w-full justify-start text-gray-600 hover:text-teal-500 mt-2">Log In</Button>
          <Button @click="signUp" class="w-full bg-teal-500 text-white hover:bg-teal-600 mt-2">Sign Up</Button>
        </template>
      </nav>
    </header>

    <RouterView />

    <Toast />

    <footer class="border-t bg-white">
      <div class="container mx-auto px-4 md:px-6 lg:px-8 flex flex-col gap-2 py-6 md:flex-row md:gap-4">
        <p class="text-center text-sm leading-loose text-gray-600 md:text-left">
          © 2024 Medicare. All rights reserved.
        </p>
        <nav class="flex justify-center gap-4 md:ml-auto">
          <router-link class="text-sm text-gray-600 hover:text-teal-500 transition-colors" to="#">
            Terms
          </router-link>
          <router-link class="text-sm text-gray-600 hover:text-teal-500 transition-colors" to="#">
            Privacy
          </router-link>
          <router-link class="text-sm text-gray-600 hover:text-teal-500 transition-colors" to="#">
            Contact
          </router-link>
        </nav>
      </div>
    </footer>
  </div>
</template>

<script>
import Button from "./components/ui/button.vue";
import { Menu, Bell , MessageCircleIcon, MailOpen, Mail} from "lucide-vue-next";
import { useUserStore } from "./stores/user";
import Toast from "./components/Toast.vue";

export default {
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
    };
  },

  mounted() {
    this.userStore.initStore();
    this.userStore.initWebsocket();
    this.userStore.getActiveSession();

},


  components: {
    Button,
    MessageCircleIcon,
    Menu,
    Bell,
    Toast,
    MailOpen,
    Mail
  },

  data() {
    return {
      isMenuOpen: false,
      navigations: [
        { name: 'Service', href: '/' },
        { name: 'Dashboard', href: '/dashboard' },
        { name: 'Plans', href: '/' },
        { name: 'Testimonials', href: '/' },
      ],
    };
  },

  computed: {
  notificationCount() {
    return this.userStore.user.unread_notification_count
  },

  sessionCount(){
    return Array.isArray(this.userStore.activeSession)?
    this.userStore.activeSession.length 
    :0;
  },
  sessionId() {
  return Array.isArray(this.userStore.activeSession) && this.userStore.activeSession.length > 0
    ? this.userStore.activeSession[0].id
    : null;
},


},

  methods: {
    toggleMenu() {
      console.log("Toggle Menu clicked");
      this.isMenuOpen = !this.isMenuOpen;
    },
    signUp() {
      this.$router.push("/signup");
    },
    logIn() {
      this.$router.push("/login");
    },
  },
};
</script>