import Vue from 'vue';
import Router from 'vue-router';
import PageNotFound from './views/404/index';
import InternalServerError from './views/500/index';
import userServices from './lib/userServices.js';
import Home from './views/Home/index';
import SignIn from './views/SignIn/index';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/Login',
      name: 'Login',
      component: SignIn,
      meta: {
        auth: false,
      },
    },
    {
      path: '*',
      name: 'PageNotFound',
      component: PageNotFound,
      meta: {
        title: 'Page Not Found',
      },
    },
    {
      path: '/500',
      name: 'ServerError',
      component: InternalServerError,
      meta: {
        title: '500',
      },
    },

    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {
        auth: true,
      },
    },
  ],
});
router.beforeEach((to, _from, next) => {
  const isSignedIn = userServices.isSignedIn();
  if (to.meta && to.meta.auth !== undefined) {
    if (to.meta.auth) {
      if (!isSignedIn) {
        router.push('/Login');
      } else {
        next();
      }
    } else if (!isSignedIn) {
      next();
    } else {
      router.push({ name: 'Home' });
    }
  } else {
    next();
  }
});
export default router;
