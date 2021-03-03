import Vue from 'vue';
import GAuth from 'vue-google-oauth2';
import ElementUI from 'element-ui';
import axios from 'axios';
import VueAxios from 'vue-axios';
import lang from 'element-ui/lib/locale/lang/en';
import locale from 'element-ui/lib/locale';
import vGanttChart from 'v-gantt-chart';
import App from './App.vue';
import router from './router';
import store from './store';
import GOOGLE from '@/config/google';

import 'element-ui/lib/theme-chalk/index.css';

locale.use(lang);

Vue.use(GAuth, {
  clientId: GOOGLE.CLIENT_ID,
  scope: 'profile email https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events',
  prompt: 'select_account',
});

Vue.use(VueAxios, axios);
Vue.use(ElementUI);
Vue.use(vGanttChart);

Vue.axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
