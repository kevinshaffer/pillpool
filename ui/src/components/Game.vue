<!-- TODO: Validate whether or not the player actually is allowed in this game via routing stuff -->
<template>
    <div id="game">
        <div v-show="Object.keys(balls).length" id="balls">
            <div style="text-align:center">
                <span class="ball1 ballz" @click="toggleBall(1)" v-bind:class="ballClass(1)"></span>
            </div>
            <div style="text-align:center">
                <span class="ball2 ballz" @click="toggleBall(2)" v-bind:class="ballClass(2)"></span>
                <span class="ball3 ballz" @click="toggleBall(3)" v-bind:class="ballClass(3)"></span>
            </div>
            <div style="text-align:center">
                <span class="ball4 ballz" @click="toggleBall(4)" v-bind:class="ballClass(4)"></span>
                <span class="ball8 ballz" @click="toggleBall(8)" v-bind:class="ballClass(8)"></span>
                <span class="ball5 ballz" @click="toggleBall(5)" v-bind:class="ballClass(5)"></span>
            </div>
            <div style="text-align:center">
                <span class="ball6 ballz" @click="toggleBall(6)" v-bind:class="ballClass(6)"></span>
                <span class="ball7 ballz" @click="toggleBall(7)" v-bind:class="ballClass(7)"></span>
                <span class="ball9 ballz" @click="toggleBall(9)" v-bind:class="ballClass(9)"></span>
                <span class="ball10 ballz" @click="toggleBall(10)" v-bind:class="ballClass(10)"></span>
            </div>
            <div style="text-align:center">
                <span class="ball11 ballz" @click="toggleBall(11)" v-bind:class="ballClass(11)"></span>
                <span class="ball12 ballz" @click="toggleBall(12)" v-bind:class="ballClass(12)"></span>
                <span class="ball13 ballz" @click="toggleBall(13)" v-bind:class="ballClass(13)"></span>
                <span class="ball14 ballz" @click="toggleBall(14)" v-bind:class="ballClass(14)"></span>
                <span class="ball15 ballz" @click="toggleBall(15)" v-bind:class="ballClass(15)"></span>
            </div>
        </div><hr>
        <table id='playerList'>
            <tbody>
                <tr :key="player.username" v-for="player in players">
                    <td class="player-emoji" v-html="player.emoji"></td> 
                    <td>{{ player.username }}</td> 
                    <td v-for="ball in player.balls.map(x => x === null ? 0 : x).sort(sortNumber)">
                        <span class="player-ballz" v-bind:class="playerBallClass(ball)"></span>
                    </td>
                </tr>
            </tbody>
        </table>
        <hr>
        <h1 v-show="winner" >{{ winner_username}} Won!</h1>
    </div>
</template>

<script>
import dataResource from '@/util/resources';
export default {
    name: 'game',
    data(){
        return {
            room_id: null,
            game_id: null,
            winner: null,
            winner_username: null,
            players: {},
            balls: {},
            my_balls: [],
            remaining_players: [],
            ball_hash: null,
            date_created: null,
            date_modified: null,
            spectator: false,
            poll_ball_status: null,
            end_game_timeout: 10000,
            poll_balls_timer: 5000,
        }
    },
    watch: {
        /* When all of my balls run out, turn me into spectator mode */
        remaining_players: function(_new, _old) {
            if (_new.indexOf(this.$root.user.id) === -1){
                this.spectator = true;
            }
        },
        winner: { 
            immediate: true, 
            handler(_new, _old){
                if (_old === undefined){
                    this.pollBalls();
                } else if (_new != null){
                    clearInterval(this.poll_ball_status);
                    // Make it say "You won!" if it's on your version of the game;
                    if (this.winner === this.$root.user.id){
                        this.winner_username = "You";
                    }
                    /* If you're on the game page during the game, it'll redirect you */
                    /* Otherwise you can stay on the page to see the end result */
                    if (_new != null && !(_old === undefined)){
                        setTimeout(
                            function(){
                                this.$router.push(`/rooms/${this.room_id}`);
                            }.bind(this),
                            this.end_game_timeout
                        );
                    }
                    // TODO: make winner screen pretty!
                    // TODO: set 15 second timer to move you back to the room.
                }
            }
        }
    },
    computed: {
    },
    beforeDestroy(){
        clearInterval(this.poll_ball_status);
    },
    methods: {
        sortNumber(a,b) {
            return a - b;
        },
        pollBalls(){
            let reload = this.getGame;
            reload();
            this.poll_ball_status = setInterval(
                function(){
                    reload();
                }.bind(this),
                this.poll_balls_timer
            );
        },
        playerBallClass(ball_number){
            let _ball_number = ball_number || 0;
            let _key = "ball"+_ball_number
            let _obj = {}
            _obj[_key] = true;
            _obj.potted = (_ball_number === 0) ? false : this.balls[_ball_number].state === "potted";
            return _obj;
        },
        ballClass(ball_number){
            if (!Object.keys(this.balls).length){ 
                return {}
            }
            return {
                live: this.balls[ball_number].state === "live",
                potted: this.balls[ball_number].state === "potted",
                "my-ball": this.my_balls.indexOf(ball_number) >= 0
            }
        },
        getGame(){
            let _query = (this.date_modified) ? `?last_modified=${this.date_modified}` : ``;
            return dataResource.API.get(`${this.$route.path}${_query}`)
                .then((response) => {
                    if (response.statusCode === 200){
                        this.updateProperties(response.body);
                    }
                })
                .catch((response) => {
                    this.$router.push(`/rooms/${this.room_id}`);
                });
        },
        updateProperties(properties){
            this.winner = properties.winner;
            this.winner_username = properties.winner_username;
            this.players = properties.players;
            this.balls = properties.balls;
            this.my_balls = properties.my_balls;
            this.remaining_players = properties.remaining_players;
            this.ball_hash = properties.ball_hash;
            this.date_created = properties.date_created;
            this.date_modified = properties.date_modified;
        },
        potBall(ball_number){
            return dataResource.API.put(`${this.$route.path}/balls/${ball_number}/pot`)
                .then((response) => {
                    console.log('Successful Pot Ball Response');
                    this.updateProperties(response.body);
                })
                .catch((response) => {
                    console.log('Error Pot Ball Response');
                });
        },
        unPotBall(ball_number){
            return dataResource.API.put(`${this.$route.path}/balls/${ball_number}/unpot`)
                .then((response) => {
                    console.log('Successful unPot Ball Response');
                    this.updateProperties(response.body);
                })
                .catch((response) => {
                    console.log('Error unPot Ball Response');
                });
        },
        toggleBall(ball_number){
            if (this.winner != null){
                return;
            }
            if (this.balls[ball_number].state === "live"){
                return this.potBall(ball_number);
            } else {
                return this.unPotBall(ball_number);
            }
            // figure out the state of the ball, and call pot or unpot accordingly... Or maybe handle this on the ball object in the html
        }

    },
    created(){
        this.room_id = this.$route.params.room_id;
        this.game_id = this.$route.params.game_id;
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

#playerList {
    margin-left: auto;
    margin-right: auto;
}

.player-emoji {
    font-size: 2em;
}
.player-ballz {
    display:inline-block;
    height: 35px;
    width: 35px;
}

.ballz {
    display:inline-block;
    border-color:white;
    border-width:thick;
    border-style:solid;
    border-radius:50%;
    height: 50px;
    width: 50px;
}
.potted {
    opacity: .15;
    /*position: relative;*/
}
/*
.potted:before {
  position: absolute;
  content: "";
  left: 0%;
  top: 46%;
  right: 0;
  border-top: 5px solid;
  border-color: black;
  
  -webkit-transform:rotate(-45deg);
  -moz-transform:rotate(-45deg);
  -ms-transform:rotate(-45deg);
  -o-transform:rotate(-45deg);
  transform:rotate(-45deg);
}*/

.my-ball {
    border-color:black;
    border-style:solid;
}
.my-ball.potted {
    border-color:red;
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
