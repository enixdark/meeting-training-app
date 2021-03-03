import userServices from '@/lib/userServices.js';

const state = {
  isShowAcitonUserView: true,
  isShowAcitonCordiratorUpdate: true,
  isShowAcitonCordiratorChange: true,
  isShowAcitonCordiratorRemove: true,
  isShowAcitonAttendeeNotConfirm: true,
  isShowAcitonAttendeeConfirmed: true,
  isShowAcitonAdminApprove: true,
  isShowAcitonAdminRemoveApprove: true,
};
const getters = {
  isShowAcitonCordiratorUpdate(state) {
    return state.isShowAcitonCordiratorUpdate;
  },
  isShowAcitonCordiratorChange(state) {
    return state.isShowAcitonCordiratorChange;
  },
  isShowAcitonCordiratorRemove(state) {
    return state.isShowAcitonCordiratorRemove;
  },
  isShowAcitonUserView(state) {
    return state.isShowAcitonUserView;
  },
  isShowAcitonAttendeeNotConfirm(state) {
    return state.isShowAcitonAttendeeNotConfirm;
  },
  isShowAcitonAttendeeConfirmed(state) {
    return state.isShowAcitonAttendeeConfirmed;
  },
  isShowAcitonAdminApprove(state) {
    return state.isShowAcitonAdminApprove;
  },
  isShowAcitonAdminRemoveApprove(state) {
    return state.isShowAcitonAdminRemoveApprove;
  },
};

const actions = {
  updateListActionWhenClickMenu({ commit }, meeting) {
    commit('UPDATE_LIST_ACTION_WHEN_CLICK_MENU', meeting);
  },
  updateListActionChangeCoordirator({ commit }) {
    commit('UPDATE_LIST_ACTION_CHANGE_COORDIRATOR');
  },
};

const mutations = {
  UPDATE_LIST_ACTION_WHEN_CLICK_MENU(state, meeting) {
    const emailUser = userServices.userData().user.email;
    const role = userServices.userData().user.roles;
    const isAdmin = role.length !== 0 ? role[0].role_type : '';
    const listAtendees = meeting.attendees;
    const cordirator = listAtendees.filter(p => p.is_coordinator === true);
    const emailCordirator = cordirator[0].user.email;
    const isAttendees = listAtendees.filter(p => p.user.email === emailUser);

    state.isShowAcitonUserView = true;
    if (isAttendees.length !== 0) {
      if (emailUser === emailCordirator) {
        state.isShowAcitonCordiratorUpdate = true;
        state.isShowAcitonCordiratorRemove = true;
        state.isShowAcitonAttendeeNotConfirm = false;
        state.isShowAcitonAttendeeConfirmed = false;
        state.isShowAcitonCordiratorChange = true;
      } else {
        if (isAdmin === 'admin') {
          state.isShowAcitonCordiratorUpdate = true;
          state.isShowAcitonCordiratorRemove = true;
        } else {
          state.isShowAcitonCordiratorUpdate = false;
          state.isShowAcitonCordiratorRemove = false;
        }
        state.isShowAcitonCordiratorChange = false;
        if (isAttendees[0].is_accepted) {
          state.isShowAcitonAttendeeNotConfirm = true;
          state.isShowAcitonAttendeeConfirmed = false;
        } else if (!isAttendees[0].is_response) {
          state.isShowAcitonAttendeeNotConfirm = true;
          state.isShowAcitonAttendeeConfirmed = true;
        } else {
          state.isShowAcitonAttendeeNotConfirm = false;
          state.isShowAcitonAttendeeConfirmed = true;
        }
      }
    } else {
      if (isAdmin === 'admin') {
        state.isShowAcitonCordiratorUpdate = true;
        state.isShowAcitonCordiratorRemove = true;
      } else {
        state.isShowAcitonCordiratorUpdate = false;
        state.isShowAcitonCordiratorRemove = false;
      }
      state.isShowAcitonCordiratorChange = false;
      state.isShowAcitonAttendeeNotConfirm = false;
      state.isShowAcitonAttendeeConfirmed = false;
      state.isShowAcitonAdminApprove = false;
    }
    if (meeting.state === false && isAdmin === 'admin') {
      state.isShowAcitonAdminApprove = true;
    } else {
      state.isShowAcitonAdminApprove = false;
    }
  },
  UPDATE_LIST_ACTION_CHANGE_COORDIRATOR(state) {
    state.isShowAcitonCordiratorUpdate = false;
    state.isShowAcitonCordiratorChange = true;
    state.isShowAcitonCordiratorRemove = false;
    state.isShowAcitonAttendeeNotConfirm = false;
    state.isShowAcitonAttendeeConfirmed = false;
    state.isShowAcitonUserView = false;
    state.isShowAcitonAdminApprove = false;
  },
};
export default {
  state,
  actions,
  mutations,
  getters,
};
