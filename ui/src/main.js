// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueResource from 'vue-resource';
import App from './App'
import router from './router'
import jwtDecode from 'jwt-decode';
import 'vue-awesome/icons';
import Icon from 'vue-awesome/components/Icon';
 
Vue.use(VueResource);
Vue.component('icon', Icon);
Vue.config.productionTip = false



/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: { App },
    template: '<App/>',
    data() {
        return {
            apiUrlPrefix: 'http://localhost:6540',
            user: {
                username: null
            },
            token: null
        };
    },
    methods: {
        logout(){
            this.token = null;
            localStorage.removeItem('token');
            location.href = '/';
        }
    },
    created() {
        this.token = localStorage.getItem("token");
        if (this.token) {
            // TODO: Check to see if this person is currently in a room/game?
            this.payload = jwtDecode(this.token);
            this.user = this.payload.user;
            if (this.$route.path === '/'){
                this.$router.push('/rooms');
            }
            this.$router.push(this.$route.path);
        }
        console.log("Main is loaded");
    }
});
