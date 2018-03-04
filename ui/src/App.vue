<template>
    <div id="app">
        <router-view/>
        <br><br><br>
        <div v-show="$root.token" @click="$root.logout" ><icon name="power-off"></icon> Logout</div>
    </div>
</template>

<script>
export default {
    name: 'App'
}
</script>

<style>
#app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>
