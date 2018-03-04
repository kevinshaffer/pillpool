<template>
    <div id="rooms">
        <h2> Hello {{ $root.user.username }} </h2>
        <div>
            <br>
            <div v-show="!join_room_input" @click="join_room_input = !join_room_input">Join Game</div>
            <label v-show="join_room_input" for= "join_room_input">Room: </label> 
            <input v-show="join_room_input" name="join_room_input" placeholder="Enter to Submit" @keyup.enter="joinRoom" v-model="room_name"/> 
            <br>
            <!--<div v-show="join_room_input" @click="joinRoom">Join</div>-->
            <div v-show="!join_room_input" @click="createRoom">Create Game</div>
        </div>
    </div>
</template>

<script>
import dataResource from '@/util/resources';
export default {
    name: 'rooms',
    data(){
        return {
            join_room_input: false,
            room_name: "",
        }
    },
    methods: {
        createRoom(){
            return dataResource.API.post('/rooms', {})
                .then((response) => {
                    this.room_name = response.body.name;
                    this.joinRoom();
            });
        },
        joinRoom(){
            dataResource.API.post(`/rooms/${this.room_name}/join`,{})
                .then((response) => {
                this.$router.push(`/rooms/${this.room_name}`);
            });
        }

    },
    created(){
        console.log('Rooms is loaded');
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
