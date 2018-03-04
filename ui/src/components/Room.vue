<template>
    <div id="rooms">
        <div v-show="!room_id">
            Room {{ room_id }} does not exist. <br>
            <div @click="$router.push('/rooms')">Back</div>
        </div>
        <div v-show="room_id && !joining_game && ball_choices.length === 0">
            <!-- Hello {{ $root.user.username }}, -->
            Welcome to Room {{ room_id }} <br><br>
            <div class="start" @click="ballSelector">Start Game</div>
        </div>
        <div  v-show="ball_choices.length > 0">
            <h3>Select balls per player</h3>
        <table id="ballSelector">
            <tr>
                <td :key="ball" v-for="ball in ball_choices">
                    <span class="ballz" @click="balls_per_player=ball" v-bind:class="ballClass(ball)"></span>
                </td>
            </tr>
        </table>
        </div>
        <table id='playerList'>
            <tbody>
                <tr :key="player.username" v-for="player in players">
                    <td class="player-emoji" v-html="player.emoji"></td> 
                    <td>{{ player.username }}</td> 
                </tr>
            </tbody>
        </table>
        <div v-show="joining_game">Game is Starting...</div>
    </div>
</template>

<script>
import dataResource from '@/util/resources';
export default {
    name: 'room',
    data(){
        return {
            room_id: this.$route.params.room_id,
            game_id: null,
            balls_per_player: null,
            players: null,
            game_starting_status: null,
            joining_game: false,
            ball_choices: [],
            poll_game_timer: 5000,
            join_game_delay: 1500,
        }
    },
    beforeDestroy(){
        clearInterval(this.game_starting_status);
    },
    watch: {
        // Redirect the player to the game that is already in progress
        game_id: function(_game_id){
            if (_game_id != null){
                clearInterval(this.game_starting_status);
                this.joinGame();
            }
        },
        // If this changes from null to a number, start the game!
        balls_per_player: function(_new, _old) {
            if (_old == null && _new !== null){
                this.startGame();
            }
        }
    },
    methods: {
        // Checks to see if there is a live game for this room by calling getGame
        pollGame(){
            let reload = this.getRoom;
            reload();
            this.game_starting_status = setInterval(
                function(){
                    reload();
                }.bind(this),
                this.poll_game_timer
            );
        },      
        // Return the class of the ball based on the number (ball0, ball1, etc..)  
        ballClass(_ball_number){
            let _key = "ball"+_ball_number
            let _obj = {}
            _obj[_key] = true;
            return _obj;
        },
        // Looks to see if there is a running game, and if so sets game_id, which is being watched. 
        getGame(){
            return dataResource.API.get(`rooms/${this.room_id}/games/live`)
                .then((response) => { 
                    this.game_id = response.body.game_id;
                })
                .catch((response) => {
                });

        },
        // Get the details for this room.
        getRoom(){
            return dataResource.API.get(`/rooms/${this.room_id}`)
                .then((response) => { 
                    this.game_id = response.body.game_id;
                    this.players = response.body.players;
                })
                .catch((response) => {
                    this.room_id = null;
                    clearInterval(this.game_starting_status);
                });
        },
        // Throw the balls on the screen for the user to select how many should be assigned per player.
        ballSelector(){
            this.getRoom();
            let _num_players = Object.keys(this.players).length;
            let _num_balls = Math.min(5, Math.floor(15 / _num_players)); 
            let _ball_choices = new Array(_num_balls);
            for(var i=0;i<_ball_choices.length;i++){
                _ball_choices[i] = i+1;
            }
            this.ball_choices = _ball_choices;
            //this.startGame();
        }, 
        // Creates a new game, and then sets game_id
        // If a game already exists, it just grabs that ID and sends you in.
        startGame(){
            this.join_game_delay = 0;
            return dataResource.API.post(`/rooms/${this.room_id}/games`, {
                    body: {
                        balls: this.balls_per_player
                    }
                }).then((response) => {
                    this.game_id = response.body.id;
                }).catch((response) => {
                    this.game_id = response.body.error.game_id;
                });
        },
        // After the delay, routes you to the live game.
        joinGame(){
            this.joining_game = true;
            setTimeout(
                function(){
                    this.$router.push(`${this.$route.path}/games/${this.game_id}`);
                }.bind(this), 
                this.join_game_delay
            );
        }
    },
    created(){
        this.pollGame();
    }, 
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.start {
    font-size: 1.5em;
}
.player-emoji{
    display:inline;
    font-size: 2em;
    margin:5px;
}
#playerList {
    margin-left: auto;
    margin-right: auto;
}
#ballSelector {
    margin-left: auto;
    margin-right: auto;
}


.ballz {
    display:inline-block;
    border-color:white;
    height: 35px;
    width: 35px;
}

.ball0{
	background-image: url('../assets/balls/0.svg');
}

.ball1{
	background-image: url('../assets/balls/1.svg');
}

.ball2{
	background-image: url('../assets/balls/2.svg');
}

.ball3{
	background-image: url('../assets/balls/3.svg');
}

.ball4{
	background-image: url('../assets/balls/4.svg');
}

.ball5{
	background-image: url('../assets/balls/5.svg');
}

.ball6{
	background-image: url('../assets/balls/6.svg');
}

.ball7{
	background-image: url('../assets/balls/7.svg');
}

.ball8{
	background-image: url('../assets/balls/8.svg');
}

.ball9{
	background-image: url('../assets/balls/9.svg');
}

.ball10{
	background-image: url('../assets/balls/10.svg');
}

.ball11{
	background-image: url('../assets/balls/11.svg');
}

.ball12{
	background-image: url('../assets/balls/12.svg');
}

.ball13{
	background-image: url('../assets/balls/13.svg');
}

.ball14{
	background-image: url('../assets/balls/14.svg');
}

.ball15{
	background-image: url('../assets/balls/15.svg');
}

</style>
