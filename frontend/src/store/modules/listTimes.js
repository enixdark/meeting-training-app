import axios from 'axios';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';
import { convertDate } from '@/lib/common.js';
import {
  getListDates,
  setBackgroundBeyondTimes,
  setBackgroundVisibleTimesByDate,
  setBackgroundVisibleTimesByTime,
  getListTimeInDay,
} from '@/lib/listTimes.js';

const state = {
  listDates: [],
  listTimes: [],
  isShowPeriodTimes: false,
};

const getters = {
  listDates(state) {
    return state.listDates;
  },
  listTimes(state) {
    return state.listTimes;
  },
  isShowPeriodTimes(state) {
    return state.isShowPeriodTimes;
  },
};

const actions = {
  updateListDates({ commit }, date) {
    commit('UPDATE_LIST_DATES', date);
  },
  updateListTimes({ commit }, time) {
    commit('UPDATE_LIST_TIMES', time);
  },
  updateIsShowPeriodTimes({ commit }, isShowPeriodTimes) {
    commit('UPDATE_IS_SHOW_PERIOD_TIMES', isShowPeriodTimes);
  },
};

const mutations = {
  UPDATE_LIST_DATES(state, date) {
    const list = getListDates();
    for (let j = 0; j < list.length; j += 1) {
      if (date === list[j].date) {
        list[j].statusDate = 'choosed';
      } else {
        list[j].statusDate = 'not-choose';
      }
    }
    state.listDates = list;
  },

  UPDATE_LIST_TIMES(state, infomation) {
    const list = getListTimeInDay();
    const dateSelected = infomation.date;
    const locationIdSelected = infomation.locationId;
    const meetingSelected = infomation.meeting;
    axios({
      method: 'GET',
      url: `${ENDPOINT.GET_EMPTY_LOCATIONS}?location_id=${locationIdSelected}&date=${dateSelected}&include_meeting=true`,
      headers: {
        Authorization: `jwt ${userServices.userData().jwt}`,
        'Content-Type': 'application/json',
      },
    }).then((response) => {
      const b = response.data.data[0].block;
      const meetingInDate = b.filter(p => p.meeting != null);
      for (let j = 0; j < meetingInDate.length; j += 1) {
        setBackgroundVisibleTimesByTime(
          list,
          meetingInDate[j].start,
          meetingInDate[j].finish,
          'notVisible',
        );
      }
      if (meetingSelected !== null) {
        const meetingDate = convertDate(meetingSelected.started_time, 'YYYY-MM-DD');
        if (meetingDate === dateSelected && meetingSelected.location.id === locationIdSelected) {
          setBackgroundVisibleTimesByDate(
            list,
            meetingSelected.started_time,
            meetingSelected.finished_time,
            'visible',
          );
        }
      }
      setBackgroundBeyondTimes(list, dateSelected);
    }).catch(() => {
      setBackgroundBeyondTimes(list, dateSelected);
    });
    state.listTimes = list;
  },

  UPDATE_IS_SHOW_PERIOD_TIMES(state, isShowPeriodTimes) {
    state.isShowPeriodTimes = isShowPeriodTimes;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
