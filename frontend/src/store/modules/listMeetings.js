  import axios from 'axios';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';
import {
  getListMeetingInToday,
  groupMeetingByDates,
  getMyMeetings,
  shearchMeetings,
} from '@/lib/listMeetings.js';
// import { convertDate } from '@/lib/common.js';

const state = {
  meetingHappening: {
    title: 'ĐANG DIỄN RA',
    meetings: [],
  },
  isShowMeetingHappening: true,
  meetingEarly: {
    title: 'LỊCH HỌP SẮP TỚI',
    meetings: [],
  },
  isShowMeetingEarly: true,
  meetingFutures: [],
  isShowDailyMeeting: true,
  isShowBtn: true,
  btnName: 'Xem thêm',
  isShowHome: true,
  isComponent: 2,
  isShowApproval: true,
  titleHome: null,
  isShearch: false,
};

const getters = {
  meetingHappening(state) {
    return state.meetingHappening;
  },
  isShowMeetingHappening(state) {
    return state.isShowMeetingHappening;
  },
  meetingEarly(state) {
    return state.meetingEarly;
  },
  isShowMeetingEarly(state) {
    return state.isShowMeetingEarly;
  },
  meetingFutures(state) {
    return state.meetingFutures;
  },
  isShowDailyMeeting(state) {
    return state.isShowDailyMeeting;
  },
  isShowBtn(state) {
    return state.isShowBtn;
  },
  btnName(state) {
    return state.btnName;
  },
  isShowHome(state) {
    return state.isShowHome;
  },
  isComponent(state) {
    return state.isComponent;
  },
  isShowApproval(state) {
    return state.isShowApproval;
  },
  titleHome(state) {
    return state.titleHome;
  },
  isShearch(state) {
    return state.isShearch;
  },
};

const actions = {
  updateIsShowHome({ commit }, isShowHome) {
    commit('UPDATE_IS_SHOW_HOME', isShowHome);
  },
  updateIsComponent({ commit }, component) {
    commit('UPDATE_IS_COPONENT', component);
  },
  updateIsShearch({ commit }, isShearch) {
    commit('UPDATE_IS_SHEARCH', isShearch);
  },
  loadDataMeetings({ commit }, dataShearch) {
    commit('LOAD_DATA_MEETINGS', dataShearch);
  },
};

const mutations = {
  UPDATE_IS_SHOW_HOME(state, isShowHome) {
    state.isShowHome = isShowHome;
  },
  UPDATE_IS_COPONENT(state, component) {
    state.isComponent = component;
  },
  UPDATE_IS_SHEARCH(state, isShearch) {
    state.isShearch = isShearch;
  },
  LOAD_DATA_MEETINGS(state, dataShearch) {
    const amountStart = 2;
    let allMeetingFutures = null;
    if (state.isComponent !== 3) {
      axios({
        method: 'GET',
        url: `${ENDPOINT.GET_ALL_MEETING}?relations%5B%5D=creator&relations%5B%5D=location&relations%5B%5D=attendees`,
        headers: {
          Authorization: `jwt ${userServices.userData().jwt}`,
          'Content-Type': 'application/json',
        },
      }).then((response) => {
        const allMeeting = response.data.data;
        let meetingHappeningSelected = null;
        let meetingEarlySelected = null;
        const meetingOnGoings = allMeeting.on_goings.filter(p => p.state === true);
        const meetingTodays = allMeeting.today.filter(p => p.state === true);
        const meetingFutures = response.data.data.futures.filter(p => p.state === true);
        if (state.isShearch && dataShearch.data !== null) {
          meetingHappeningSelected = shearchMeetings(
            state.isComponent,
            dataShearch.data,
            meetingOnGoings,
          );
          meetingEarlySelected = shearchMeetings(
            state.isComponent,
            dataShearch.data,
            meetingTodays,
          );
          allMeetingFutures = shearchMeetings(
            state.isComponent,
            dataShearch.data,
            meetingFutures,
          );
        } else {
          meetingHappeningSelected = meetingOnGoings;
          meetingEarlySelected = meetingTodays;
          allMeetingFutures = meetingFutures;
        }

        if (state.isComponent === 2) {
          meetingHappeningSelected = getMyMeetings(meetingHappeningSelected);
          meetingEarlySelected = getMyMeetings(meetingEarlySelected);
        }
        if (meetingHappeningSelected.length === 0) {
          state.isShowMeetingHappening = false;
        } else {
          state.isShowMeetingHappening = true;
          state.meetingHappening.title = 'ĐANG DIỄN RA';
          state.meetingHappening.meetings = getListMeetingInToday(meetingHappeningSelected);
        }

        if (meetingEarlySelected.length === 0) {
          state.isShowMeetingEarly = false;
        } else {
          state.isShowMeetingEarly = true;
          state.meetingEarly.title = 'LỊCH HỌP SẮP TỚI';
          state.meetingEarly.meetings = getListMeetingInToday(meetingEarlySelected);
        }
        if (state.isComponent === 2) {
          allMeetingFutures = getMyMeetings(allMeetingFutures);
        }
        if (allMeetingFutures.length !== 0) {
          state.isShowDailyMeeting = true;
        } else {
          state.isShowDailyMeeting = false;
        }
        const allMeetingFuturesNew = getListMeetingInToday(allMeetingFutures);
        const allMeetingFuturesByDate = groupMeetingByDates(allMeetingFuturesNew);
        const count = allMeetingFuturesByDate.length;
        if (count > amountStart) {
          state.isShowBtn = true;
          if (dataShearch.amount < count) {
            if (state.btnName === 'Xem thêm') {
              state.btnName = 'Xem thêm';
            } else if (dataShearch.amount <= amountStart) {
              state.btnName = 'Xem thêm';
            } else {
              state.btnName = 'Ẩn bớt';
            }
            state.meetingFutures = allMeetingFuturesByDate.slice(0, dataShearch.amount);
          } else {
            state.btnName = 'Ẩn bớt';
            state.meetingFutures = allMeetingFuturesByDate;
          }
        } else {
          state.meetingFutures = allMeetingFuturesByDate;
          state.isShowBtn = false;
        }
        if (!state.isShowMeetingHappening && !state.isShowMeetingEarly
          && !state.isShowDailyMeeting) {
          state.isShowApproval = true;
          state.titleHome = 'DANH SÁCH LỊCH HỌP TRỐNG!';
        } else if (state.isShowDailyMeeting && state.isComponent === 3) {
          state.titleHome = 'DANH SÁCH LỊCH HỌP ĐANG CHỜ PHÊ DUYỆT!';
        } else {
          state.isShowApproval = false;
        }
      }).catch(() => {
      });
    }
    if (state.isComponent === 3) {
      state.isShowApproval = true;
      state.isShowMeetingHappening = false;
      state.isShowMeetingEarly = false;
      axios({
        method: 'GET',
        url: `${ENDPOINT.GET_ALL_MEETING_APPROVAL}?sort=created_at&order=desc&relations[]=attendees&relations[]=location`,
        headers: {
          Authorization: `jwt ${userServices.userData().jwt}`,
          'Content-Type': 'application/json',
        },
      }).then((res) => {
        const meetingFutures = res.data.data;
        console.log(meetingFutures);
        if (state.isShearch && dataShearch.data !== null) {
          allMeetingFutures = shearchMeetings(
            state.isComponent,
            dataShearch.data,
            meetingFutures,
          );
        } else {
          allMeetingFutures = meetingFutures;
        }
        if (allMeetingFutures.length !== 0) {
          state.isShowDailyMeeting = true;
        } else {
          state.isShowDailyMeeting = false;
        }
        const allMeetingFuturesNew = getListMeetingInToday(allMeetingFutures);
        const allMeetingFuturesByDate = groupMeetingByDates(allMeetingFuturesNew);
        const count = allMeetingFuturesByDate.length;
        if (count > amountStart) {
          state.isShowBtn = true;
          if (dataShearch.amount < count) {
            if (state.btnName === 'Xem thêm') {
              state.btnName = 'Xem thêm';
            } else if (dataShearch.amount <= amountStart) {
              state.btnName = 'Xem thêm';
            } else {
              state.btnName = 'Ẩn bớt';
            }
            state.meetingFutures = allMeetingFuturesByDate.slice(0, dataShearch.amount);
          } else {
            state.btnName = 'Ẩn bớt';
            state.meetingFutures = allMeetingFuturesByDate;
          }
        } else {
          state.meetingFutures = allMeetingFuturesByDate;
          state.isShowBtn = false;
        }
        if (!state.isShowMeetingHappening && !state.isShowMeetingEarly
            && !state.isShowDailyMeeting) {
          state.titleHome = 'DANH SÁCH LỊCH HỌP CHỜ PHÊ DUYỆT TRỐNG!';
        } else if (state.isShowDailyMeeting && state.isComponent === 3) {
          state.titleHome = 'DANH SÁCH LỊCH HỌP ĐANG CHỜ PHÊ DUYỆT!';
        }
      }).catch(() => {
      });
    }
  },
};
export default {
  state,
  actions,
  mutations,
  getters,
};
