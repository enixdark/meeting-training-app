<template>
  <div class="check-empty-room">
    <div class="top-bar">
      <label for="cellWidth">Chiều rộng</label>
      <input type="range"
             min="50"
             max="200"
             v-model.number="cellWidth">
      <label for="cellHeight">Chiều cao</label>
      <input type="range"
             min="20"
             max="300"
             v-model.number="cellHeight">
      <label for="titleWith">Ẩn phòng họp</label>
      <input type="range"
             min="0"
             max="250"
             v-model.number="titleWidth">
    </div>
    <div class="container">
    <v-gantt-chart :startTime="startTime"
                     :endTime="endTime"
                     :cellWidth="cellWidth"
                     :cellHeight="cellHeight"
                     :timeLines="timeLinesMeeting"
                     :titleHeight="titleHeight"
                     :scale="scale"
                     :titleWidth="titleWidth"
                     showCurrentTime
                     :datas="dataMeetings">
        <template v-slot:left="{data}">
          <TestLeft :data="data"></TestLeft>
        </template>
        <template v-slot:title>
          Phòng họp
        </template>
        <template v-slot:block="{data,item}">
          <Test :data="data"
                :updateTimeLines="updateTimeLines"
                :cellHeight="cellHeight"
                :currentTime="currentTime"
                :item="item"
                ></Test>
        </template>
      </v-gantt-chart>
    </div>
  </div>
</template>

<script>
import dayjs from 'dayjs';
import { mapActions, mapGetters } from 'vuex';
import Test from '../CheckEmptyRoom/Test';
import TestLeft from '../CheckEmptyRoom/TestLeft';
import { listDataByRoom } from '@/lib/mock.js';
import 'vue-cal/dist/vuecal.css';
import { getListDates } from '@/lib/listTimes.js';

export default {
  name: 'CheckEmptyRoom',
  components: { Test, TestLeft },
  props: ['meetingFutures'],
  computed: {
    ...mapGetters(['dataMeetings', 'timeLinesMeeting']),
  },
  data() {
    return {
      cellWidth: 100,
      cellHeight: 150,
      titleHeight: 50,
      titleWidth: 250,
      scale: 30,
      currentTime: dayjs(),
      startTime: dayjs(),
      endTime: dayjs().add(getListDates().length, 'day').toString(),
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    listDataByRoom,
    getListDates,
    ...mapActions(['updateDataMeetings', 'updateTimeLinesMeeting']),
    updateTimeLines(timeA, timeB) {
      this.updateTimeLinesMeeting({ timeA, timeB });
    },
    loadData() {
      this.updateDataMeetings();
    },
  },
};
</script>
<style lang="scss" scoped>
@import '@/assets/stylesheets/home/check-empty-room.scss';
</style>
