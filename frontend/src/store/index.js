import Vue from 'vue';
import Vuex from 'vuex';
import auth from './modules/auth';
import listRoom from './modules/listRoom';
import listTimes from './modules/listTimes';
import listMeetings from './modules/listMeetings';
import listAction from './modules/listAction';
import checkEmptyRoom from './modules/checkEmptyRoom';
import duplicateMeeting from './modules/duplicateMeeting';


Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    listRoom,
    listTimes,
    listMeetings,
    listAction,
    checkEmptyRoom,
    duplicateMeeting,
  },
});
