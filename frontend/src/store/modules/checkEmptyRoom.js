import axios from 'axios';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';
import { listDataByRoom } from '@/lib/mock.js';

const state = {
  dataMeetings: [],
  timeLinesMeeting: [],
};
const getters = {
  dataMeetings(state) {
    return state.dataMeetings;
  },
  timeLinesMeeting(state) {
    return state.timeLinesMeeting;
  },
};

const actions = {
  updateDataMeetings({ commit }) {
    commit('UPDATE_DATA_MEETINGS');
  },
  updateTimeLinesMeeting({ commit }, time) {
    commit('UPDATE_TIME_LINES', time);
  },
};

const mutations = {
  UPDATE_DATA_MEETINGS(state) {
    axios({
      method: 'GET',
      url: ENDPOINT.LIST_ROOM,
      headers: {
        Authorization: `jwt ${userServices.userData().jwt}`,
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        const listRooms = response.data.data;
        const list = [];
        for (let i = 0; i < listRooms.length; i += 1) {
          const dataByRoom = {
            loactionAddress: '',
            locationName: '',
            ListMeetingByRoom: [],
          };
          axios({
            method: 'GET',
            url: `${ENDPOINT.GET_ALL_MEETING}?relations%5B%5D=creator&location_id=${listRooms[i].id}&relations%5B%5D=attendees`,
            headers: {
              Authorization: `jwt ${userServices.userData().jwt}`,
              'Content-Type': 'application/json',
            },
          // eslint-disable-next-line no-loop-func
          }).then((res) => {
            dataByRoom.locationName = listRooms[i].name;
            dataByRoom.loactionAddress = listRooms[i].address;
            const meetingTodays = res.data.data.today.filter(p => p.state === true);
            meetingTodays.forEach((p) => {
              dataByRoom.ListMeetingByRoom.push(p);
            });
            const meetingOnGoings = res.data.data.on_goings.filter(p => p.state === true);
            meetingOnGoings.forEach((p) => {
              dataByRoom.ListMeetingByRoom.push(p);
            });
            const meetingFutures = res.data.data.futures.filter(p => p.state === true);
            meetingFutures.forEach((p) => {
              dataByRoom.ListMeetingByRoom.push(p);
            });
            list.push(dataByRoom);
            state.dataMeetings = listDataByRoom(list);
            const meettingFist = list.slice(0, 1)[0].ListMeetingByRoom.slice(0, 1)[0];
            state.timeLinesMeeting = [
              { time: meettingFist.started_time, color: '#6979F8' },
              { time: meettingFist.finished_time, color: '#979797' },
            ];
          }).catch(() => {
          });
        }
      }).catch(() => {
      });
  },
  UPDATE_TIME_LINES(state, time) {
    state.timeLinesMeeting = [
      {
        time: time.timeA,
        color: '#6979F8',
      },
      {
        time: time.timeB,
        color: '#979797',
      },
    ];
  },
};
export default {
  state,
  actions,
  mutations,
  getters,
};
