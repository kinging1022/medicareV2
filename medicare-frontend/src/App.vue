<template>
    <div class="flex flex-col min-h-screen bg-white">
      <header class="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-sm">
        <div class="container mx-auto px-4 md:px-6 lg:px-8 flex h-16 items-center justify-between">
          <router-link class="flex items-center justify-center" to="#">
            <span class="text-2xl ml-3 font-bold text-gray-900">Medicare</span>
          </router-link>
          <nav class="hidden md:flex items-center space-x-6 text-sm font-medium">
            <router-link v-for="item in navigations" :bind="item.name" :to="item.href" class="text-gray-600 text-lg hover:text-teal-500 transition-colors" to="#features">
              {{item.name}}
            </router-link>
            
          </nav>
          <div class="flex items-center space-x-4">
            <template v-if="!userStore.user.isAuthenticated">
            <Button @click="logIn" variant="ghost" customClass="text-gray-600 hover:text-teal-500 hidden md:inline-flex">Log In</Button>
            <Button @click="signUp" class="bg-teal-500 text-white hover:bg-teal-600 hidden md:inline-flex">Sign Up</Button>
          </template>
            <Button
              variant="ghost"
              size="icon"
              class="md:hidden"
              @click="toggleMenu"
            >
              <Menu class="h-6 w-6"/>
            </Button>
          </div>
        </div>
        <nav v-if="isMenuOpen" class="md:hidden p-4 bg-white border-t">
          <router-link v-for="item in navigations" :bind="item.name" :to="item.href" class="block py-2 text-gray-600 hover:text-teal-500">{{ item.name }}</router-link>
          <template v-if="!userStore.user.isAuthenticated">
          <Button @click="logIn" variant="ghost" class="w-full justify-start text-gray-600 hover:text-teal-500 mt-2">Log In</Button>
          <Button @click="signUp" class="w-full bg-teal-500 text-white hover:bg-teal-600 mt-2">Sign Up</Button>
          </template>
        </nav>
      </header>
      
  
      <RouterView />

      <Toast/>

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

  import { Menu } from "lucide-vue-next";
  import { useUserStore } from "./stores/user";
  import Toast  from "./components/Toast.vue";
  
  
  export default {
    setup(){
      const userStore = useUserStore()
      return {
        userStore
      }
    },
    
    beforeCreate(){
      this.userStore.initStore()
      
    },
    
    components: {
      Button,
      Menu,
      Toast
      
    },
    data() {
      return {
        isMenuOpen: false,
        navigations:[
          {name:'Service', href: '/'},
          {name:'Pharmacy', href: '/'},
          {name:'Plans', href: '/'},
          {name:'Testimonials', href: '/'},

      ]
        
      };
    },
    methods: {
      toggleMenu() {
        console.log("Toggle Menu clicked");
        this.isMenuOpen = !this.isMenuOpen;
      },
      signUp(){
        this.$router.push("/signup")
      },
      logIn(){
        this.$router.push("/login")
      }

    }
  };
  </script>
  
 