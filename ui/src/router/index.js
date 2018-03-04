import Vue from 'vue';
import Router from 'vue-router';
import dataResource from '@/util/resources';
import jwtDecode from 'jwt-decode';
import Home from '@/components/Home';
import Rooms from '@/components/Rooms';
import Room from '@/components/Room';
//import Games from '@/components/Games';
import Game from '@/components/Game';
import NotFound from '@/components/NotFound';
Vue.use(Router);


const router = new Router({
    mode: 'history',
    routes: [
        { 
            path: "*", 
            component: NotFound
        },
        { 
            path: '/', 
            name: "home", 
            component: Home,
            beforeEnter: (to, from, next) => {
                if (dataResource.getToken()) {
                    next('/rooms');
                } else {
                    next();
                }
            }
        },
        { 
            path: '/rooms', 
            name: "rooms", 
            component: Rooms,
            meta: { requiresAuth: true },
        },
        { 
            path: '/rooms/:room_id', 
            name: "room", 
            component: Room,
            meta: { requiresAuth: true },
        },
        { 
            path: '/rooms/:room_id/games/:game_id', 
            component: Game,
            meta: { requiresAuth: true },
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (to. matched.some(record => record.meta.requiresAuth)) {
        if (dataResource.getToken()){
            next();
        } else {
            next("/");
        }
    } else {
        next();
    }
});


export default router;
