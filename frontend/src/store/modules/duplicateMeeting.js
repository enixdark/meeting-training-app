import axios from 'axios';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';

const state = {
  meetingApprovalCurrent: null,
  isShowDuplicatesTitle: true,
};

const getters = {
  meetingApprovalCurrent(state) {
    return state.meetingApprovalCurrent;
  },
  isShowDuplicatesTitle(state) {
    return state.isShowDuplicatesTitle;
  },
};

const actions = {
  updateMeetingApprovalCurrent({ commit }, meeting) {
    commit('UPDATE_MEETING_APPROVAL', meeting);
  },
};

const mutations = {
  UPDATE_MEETING_APPROVAL(state, item) {
    axios({
      method: 'GET',
      url: `${ENDPOINT.GET_ALL_MEETING_APPROVAL}?sort=created_at&order=desc&relations[]=attendees&relations[]=location`,
      headers: {
        Authorization: `jwt ${userServices.userData().jwt}`,
        'Content-Type': 'application/json',
      },
    }).then((res) => {
      const allMeetingFutures = res.data.data;
      const meetingFilter = allMeetingFutures.filter(
        p => p.meeting.id === item.id,
      );
      state.meetingApprovalCurrent = meetingFilter[0];
      if (state.meetingApprovalCurrent.duplicates.length === 0) {
        state.isShowDuplicatesTitle = false;
      } else {
        state.isShowDuplicatesTitle = true;
      }
    }).catch(() => {
    });
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
