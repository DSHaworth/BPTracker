import Vue from 'vue'
import VueRouter from 'vue-router'

// https://github.com/christiannwamba/vue-auth-vuex/blob/master/src/router.js
import store from '@/store'
import routes from './routes.js'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  linkActiveClass: "active",
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/')
  } else {
    next()
  }
})

export default router
