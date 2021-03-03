const state = {
  authenticated: false,
  isShowInfoMeeting: false,
  isEditInfoMeeting: false,
  dialogVisible: false,
  isShowDialogDuplicateMeetings: false,
  isShowExprotXLS: false,
};

const getters = {
  authenticated(state) {
    return state.authenticated;
  },
  isShowInfoMeeting(state) {
    return state.isShowInfoMeeting;
  },
  isEditInfoMeeting(state) {
    return state.isEditInfoMeeting;
  },
  dialogVisible(state) {
    return state.dialogVisible;
  },
  isShowDialogDuplicateMeetings(state) {
    return state.isShowDialogDuplicateMeetings;
  },
  isShowExprotXLS(state) {
    return state.isShowExprotXLS;
  },
};

const actions = {
  updateAuthenticateStatus({ commit }, status) {
    commit('UPDATE_AUTHENTICATE_STATUS', status);
  },
  updateIsShowInfoMeeting({ commit }, isShowInfoMeeting) {
    commit('UPDATE_IS_SHOW_INFOR_MEETING', isShowInfoMeeting);
  },
  updateIsEditInfoMeeting({ commit }, isEditInfoMeeting) {
    commit('UPDATE_IS_EDIT_INFOR_MEETING', isEditInfoMeeting);
  },
  updateDialogVisible({ commit }, dialogVisible) {
    commit('UPDATE_DIALOG_VISIBLE', dialogVisible);
  },
  updateIsShowDuplicateMeetings({ commit }, isShowDialogDuplicateMeetings) {
    commit('UPDATE_IS_SHOW_DIALOG_DUPLICATE_MEETINGS', isShowDialogDuplicateMeetings);
  },
  updateIsShowExprotXLS({ commit }, isShowExprotXLS) {
    commit('UPDATE_IS_SHOW_EXPORT_XLS', isShowExprotXLS);
  },
};

const mutations = {
  UPDATE_AUTHENTICATE_STATUS(state, status) {
    state.authenticated = status;
  },
  UPDATE_IS_SHOW_INFOR_MEETING(state, isShowInfoMeeting) {
    state.isShowInfoMeeting = isShowInfoMeeting;
  },
  UPDATE_IS_EDIT_INFOR_MEETING(state, isEditInfoMeeting) {
    state.isEditInfoMeeting = isEditInfoMeeting;
  },
  UPDATE_DIALOG_VISIBLE(state, dialogVisible) {
    state.dialogVisible = dialogVisible;
  },
  UPDATE_IS_SHOW_DIALOG_DUPLICATE_MEETINGS(state, isShowDialogDuplicateMeetings) {
    state.isShowDialogDuplicateMeetings = isShowDialogDuplicateMeetings;
  },
  UPDATE_IS_SHOW_EXPORT_XLS(state, isShowExprotXLS) {
    state.isShowExprotXLS = isShowExprotXLS;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
