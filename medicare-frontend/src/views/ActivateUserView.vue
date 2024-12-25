<template>
    <div>
        <h2>Account Activation</h2>
        <div>
            <p>{{ activationMessage }}</p>

        </div>
    </div>

</template>

<script>
import axios  from 'axios';
export default {
    data(){
        return {
            activationMessage : "Activating your account...",
            
        }
    },
    mounted(){
        this.activateUser()
    },
    methods: {
        activateUser(){
            const uid = this.$route.params.uid
            const token = this.$route.params.token
            axios
                .post("/api/auth/users/activation/",{
                    uid: uid,
                    token: token
                })
                .then(response =>{
                    if (response.status === 204){
                        this.$router.push('/activation/success')
                    }else{
                        this.activationMessage("Invalid or expired token validation, Try again!!")
                    }
                })
                .catch(error =>{
                    console.error("Activation error failed", error)
                    this.$router.push('/login')
                })
        }
    }
}

</script>