<template>
  <el-popover placement="bottom"
              trigger="hover">
    <div slot="reference"
         class="plan"
         :style="{'background-color':statusColor,'margin-top':0.1*cellHeight+'px'}"
         @click="onClick">
      <div class="runTime">
        <span style="font-weight: bold">Nội dung: </span>
        <span>{{item.meeting.name}}</span>
      </div>
    </div>
    <div class="detail">
      <detail-meeting :itemSelected="item"></detail-meeting>
    </div>
  </el-popover>
</template>

<script>
import dayjs from 'dayjs';
import { mapActions } from 'vuex';
import { convertDate, getDayInWeek } from '@/lib/common.js';
import DetailMeeting from '@/components/Meeting/DetailMeeting.vue';

const NOW_PLAN = '#D5F8EA';
const FUTHER_PLAN = '#BFF2FE';
const PAST_PLAN = '#F2F2F2';
export default {
  components: {
    DetailMeeting,
  },
  name: 'Test',
  props: {
    data: Object,
    item: Object,
    currentTime: dayjs,
    updateTimeLines: Function,
    cellHeight: Number,
    startTimeOfRenderArea: Number,
  },
  data() {
    return {
      dayjs,
      isConfirm: true,
    };
  },
  computed: {
    statusColor() {
      const { item, currentTime } = this;
      const start = dayjs(item.start);
      const end = dayjs(item.end);
      if (start.isBefore(currentTime) && end.isAfter(currentTime)) {
        return NOW_PLAN;
      } if (end.isBefore(currentTime)) {
        return PAST_PLAN;
      }
      return FUTHER_PLAN;
    },
    startToString() {
      return dayjs(this.item.start).format('HH:mm');
    },
    endToString() {
      return dayjs(this.item.end).format('HH:mm');
    },
  },
  methods: {
    getDayInWeek,
    convertDate,
    ...mapActions(['updateIsEditInfoMeeting']),
    onClick() {
      this.updateTimeLines(this.item.start, this.item.end);
    },
  },
};
</script>

<style lang="scss">
@import '@/assets/stylesheets/check-empty-room/test.scss';

</style>
