<template>
    <section aria-labelledby="consultations-title">
         <div class="rounded-lg bg-white overflow-hidden shadow">
           <div class="p-6">
             <h2 class="text-lg font-medium text-gray-900" id="consultations-title">Consultations History</h2>
             <div class="mt-6 flow-root">
               <ul class="-my-5 divide-y divide-gray-200">
                 <li
                   v-for="session in sessions"
                   :key="session.id"
                   class="py-5"
                 >
                   <div class="flex items-center space-x-4">
                     <RouterLink :to="{name: 'session-history', params:{id:session.id}}" class="flex-shrink-0">
                       <FileText class="h-8 w-8 text-indigo-600" />
                     </RouterLink>
                     <div class="flex-1 min-w-0">
                       <p class="text-sm font-medium text-gray-900 truncate">
                         Dr {{ session.consultation.created_for.first_name }}
                       </p>
                     </div>
                   </div>
                   <div class="mt-2">
                   </div>
                 </li>
               </ul>
             </div>
           </div>
         </div>
       </section>
</template>
<script>
import axios from 'axios';
import {FileText} from 'lucide-vue-next';
export default{
   name:'SessionHistory',
   components:{
       FileText

   },
   data(){
       return{
           sessions: [],
       }
   },
   mounted(){
       this.getSessionHistory()
   },
   methods:{
       async getSessionHistory(){

       try{
           const response = await axios.get('/api/consultation/session-history/')
           console.log(response)
           this.sessions = response.data
           
       }catch(error){

       }


       },

   }
}



</script>
