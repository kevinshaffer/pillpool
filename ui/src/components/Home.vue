<template>
    <div id="home">
        <!--
        <button v-show="!guestNameInput" type="button" @click="guestNameInput = !guestNameInput">
            Continue as guest
        </button>-->
        Welcome! <br>
        <input v-show="!guestNameInput" placeholder="Enter Name"  @keyup.enter="guestLogin" v-model="guestName"/>
    </div>
</template>

<script>
import jwtDecode from 'jwt-decode';
import dataResource from '@/util/resources';
import requestPromiseNative from 'request-promise-native';
export default {
    name: 'home',
    data(){
        return {
            "guestNameInput": false,
            "guestName": ""
        }
    },
    methods: {
        login(username, password=null, email=null, first_name=null, last_name=null){
            return requestPromiseNative.post(`${dataResource.apiPrefix}/users`, {
                body: {
                    username: username,
                    password: password,
                    email: email,
                    first_name: first_name,
                    last_name: last_name
                }, 
                    json: true
            }).then((response) => {
                dataResource.setToken(response);
                this.$root.token = response;
                this.$root.payload = jwtDecode(response);
                this.$root.user = this.$root.payload.user;
                this.$root.user.username = this.guestName;
                this.$router.push('/rooms');
            });
        },
        guestLogin(){
            this.login(this.guestName);
        }

    },
    created(){
        console.log('Home is loaded');
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
