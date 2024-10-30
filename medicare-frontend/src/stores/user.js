import { defineStore } from "pinia";
import axios  from "axios";

export const useUserStore = defineStore({
    id: 'user',

    state: () =>({
        user:{
            isAuthenticated: false,
            id: null,
            first_name: null,
            last_name:null,
            gender : null,
            age : null,
            email: null,
            access: null,
            refresh: null,
            role: null,
            dob:null,
            blood_type:null,
            height: null,
            weight: null,
            allergies: null,
            emergency_contact: null

        }
    }),

    actions: {
        initStore(){
            console.log('initStore', localStorage.getItem('user.access'))

            if (localStorage.getItem('user.access')){
                console.log('User has access')
                this.user.access = localStorage.getItem('user.access')
                this.user.refresh = localStorage.getItem('user.refresh')
                this.user.id = localStorage.getItem('user.id')
                this.user.first_name = localStorage.getItem('user.first_name')
                this.user.last_name = localStorage.getItem('user.last_name')
                this.user.gender = localStorage.getItem('user.gender')
                this.user.age = localStorage.getItem('user.age')
                this.user.dob = localStorage.getItem('user.dob')
                this.user.blood_type = localStorage.getItem('user.blood_type')
                this.user.height = localStorage.getItem('user.height')
                this.user.weight = localStorage.getItem('user.weight')
                this.user.allergies = localStorage.getItem('user.allergies')
                this.user.emergency_contact = localStorage.getItem('user.emergency_contact')
                
                this.user.email = localStorage.getItem('user.email')
                this.user.role = localStorage.getItem('user.role')
                this.user.isAuthenticated = true

                console.log('Initialized user',this.user.first_name)
                

            }
        },
        setToken(data){
            console.log('setToken', data)
            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', data.access)
            localStorage.setItem('user.refresh', data.refresh)

            console.log('user.access:', localStorage.getItem('user.access'))
        },
        removeToken(){
            console.log ('removeToken')
            this.user.refresh = null
            this.user.access = null
            this.user.isAuthenticated = false
            this.user.id = null
            this.user.first_name = null
            this.user.last_name = null
            this.user.gender = null
            this.user.age = null
            this.user.email = null
            this.user.role = null
            this.user.dob = null
            this.user.blood_type = null,
            this.user.height = null,
            this.user.weight = null,
            this.user.allergies = null,
            this.user.emergency_contact = null

            localStorage.clear()

            
        },
        setUserInfo(user){
            
            this.user.id = user.id;
            this.user.first_name = user.first_name;
            this.user.last_name = user.last_name;
            this.user.gender = user.gender;
            this.user.age = user.display_age;
            this.user.email = user.email;
            this.user.role = user.role;
            this.user.dob = user.dob
            this.user.blood_type = user.blood_type
            this.user.height = user.height
            this.user.weight = user.weight
            this.user.allergies = user.allergies
            this.user.emergency_contact = user.emergency_contact

            localStorage.setItem('user.id', this.user.id)
            localStorage.setItem('user.first_name', this.user.first_name)
            localStorage.setItem('user.last_name', this.user.last_name)
            localStorage.setItem('user.gender', this.user.gender)
            localStorage.setItem('user.age', this.user.age)
            localStorage.setItem('user.email', this.user.email)
            localStorage.setItem('user.role', this.user.role)
            localStorage.setItem('user.dob',this.user.dob)
            localStorage.setItem('user.blood_type',this.user.blood_type)
            localStorage.setItem('user.height', this.user.height)
            localStorage.setItem('user.weight',this.user.weight)
            localStorage.setItem('user.allergies',this.user.allergies)
            localStorage.setItem('user.emergency_contact',this.user.emergency_contact)
            
            



        },
        async refreshToken(){
            try {
                const response = await axios.post('api/auth/token/refresh/', {
                    refresh: this.user.refresh
                });
                this.user.access = response.data.access;
                localStorage.setItem('user.access', response.data.access);
            } catch (error) {
                if (error.response && error.response.status === 400) {
                    console.log('Refresh token expired or invalid. Logging out.');
                    this.removeToken();
                } else {
                    throw new Error('Token refresh failed');
                }
            }
        }
        

    }

})