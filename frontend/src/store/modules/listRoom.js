import axios from 'axios';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';
import { convertDate } from '@/lib/common.js';

const state = {
  listRooms: [],
  listEmptyRooms: [],
};
const getters = {
  listRooms(state) {
    return state.listRooms;
  },
  listEmptyRooms(state) {
    return state.listEmptyRooms;
  },
};

const actions = {
  updateListRooms({ commit }) {
    commit('UPDATE_LIST_ROOMS');
  },
  updateListEmptyRooms({ commit }) {
    commit('UPDATE_LIST_EMPTY_ROOMS');
  },
};

const mutations = {
  UPDATE_LIST_ROOMS(state) {
    axios({
      method: 'GET',
      url: ENDPOINT.LIST_ROOM,
      headers: {
        Authorization: `jwt ${userServices.userData().jwt}`,
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        state.listRooms = response.data.data;
      }).catch(() => {
      });
  },

  UPDATE_LIST_EMPTY_ROOMS(state) {
    axios({
      method: 'GET',
      url: ENDPOINT.LIST_ROOM,
      headers: {
        Authorization: `jwt ${userServices.userData().jwt}`,
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        const locations = response.data.data;
        const list = [];
        for (let j = 0; j < locations.length; j += 1) {
          axios({
            method: 'GET',
            url: `${ENDPOINT.GET_EMPTY_LOCATIONS}?location_id=${locations[j].id}&date=${convertDate(new Date(), 'YYYY-MM-DD')}`,
            headers: {
              Authorization: `jwt ${userServices.userData().jwt}`,
              'Content-Type': 'application/json',
            },
          }).then((res) => {
            const listByRoom = res.data.data[0].block;
            for (let i = 0; i < listByRoom.length; i += 1) {
              const emptyRoom = {
                locationId: '',
                locationName: '',
                room: {},
              };
              emptyRoom.locationId = locations[j].id;
              emptyRoom.room = listByRoom[i];
              emptyRoom.locationName = locations[j].name;
              list.push(emptyRoom);
            }
          });
        }
        state.listEmptyRooms = list;
      });
  },
};
export default {
  state,
  actions,
  mutations,
  getters,
};
