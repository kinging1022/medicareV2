<template>
    <div class="flex flex-col items-center space-y-2 border p-4 rounded-lg">
      <component :is="icon" class="h-8 w-8 mb-2 text-primary" />
      <h3 class="text-xl font-bold">{{ title }}</h3>
      <p class="text-sm text-muted-foreground text-center">{{ description }}</p>
    </div>
  </template>
  
  <script>
  import { Users, CalendarRange, Stethoscope, Shield, Award, Heart} from "lucide-vue-next"; 
  
  export default {
    name: "FeatureCard",
    props: {
      icon: {
        type: String,
        required: true,
      },
      title: {
        type: String,
        required: true,
      },
      description: {
        type: String,
        required: true,
      },
    },
    components: {
        Users,
        CalendarRange,
        Stethoscope,
        Shield,
        Award,
        Heart
      
    },
    computed: {
      iconComponent() {
        return this.icon;
      }
    }
  };
  </script>
 
  
  
  