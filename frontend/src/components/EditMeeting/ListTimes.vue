<template>
  <div>
    <el-carousel class="list-btn-date" indicator-position="none" :autoplay="false">
      <el-carousel-item v-for="items in chunkInefficient(listDates, 4)" :key="items.index">
        <div class="choose__day">
          <div class="blockDate"
            :class="item.statusDate"
            v-for="item in items"
            :key="item.index"
            @click="chooseDate(item)">
            <p>
              {{item.dayOfWeek}}
            </p>
            <p>
              {{convertDate(item.date, 'DD-MM')}}
            </p>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
    <div class="check__time">
      <div class="blockTime" :class="item.statusTime"
        v-for="item in listTimes"
        :key="item.index"
        @click="chooseTime(item)">
          {{item.start}}-{{item.stop}}
      </div>
    </div>
    <div class="div-time-periodic" v-if="isShowPeriodTimes">
      <p>Ngày kết thúc</p>
      <el-date-picker class="date-picker"
        v-model="stopDate"
        @change="selectedTimeMeetingPeriodic"
        type="date"
        :clear-icon="iconClose"
        placeholder="Chọn ngày">
      </el-date-picker>
      <p style="width: 8%; margin-right: 20px">Chu kì </p>
      <el-select class="select"
        style="width: 11.5%; margin-right: 18px;"
        v-model="repeatedDays"
        placeholder
        @change="selectedTimeMeetingPeriodic"
        >
        <el-option
          class="room-option"
          v-for="item in listNumbers()"
          :label="item.name"
          :key="item.name"
          :value="item.name"
        ></el-option>
      </el-select>
      <el-select class="select" style="width: 23%"
                v-model="period"
                placeholder
                @change="selectedTimeMeetingPeriodic"
                >
                <el-option
                  class="room-option"
                  v-for="item in listPeriods()"
                  :label="item.name"
                  :key="item.id"
                  :value="item.id"
                ></el-option>
      </el-select>
    </div>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex';
import {
  chunkInefficient,
  convertDate,
  convertTime,
  getCurrentDate,
} from '@/lib/common.js';
import { listNumbers, listPeriods } from '@/lib/listTimes.js';

export default {
  props: [
    'meeting',
    'typeAction',
    'locationId',
    'startTimeInEdit',
    'stopTimeInEdit',
    'date',
    'meetingType',
    'endDate',
    'numberPeriodic',
    'periodicId',
  ],
  computed: {
    ...mapGetters(['listDates', 'listTimes', 'isShowPeriodTimes']),
  },
  data() {
    return {
      selectedDate: this.date,
      startTime: '',
      stopTime: '',
      repeatedDays: this.numberPeriodic,
      period: this.periodicId,
      stopDate: this.endDate,
      iconClose: '',
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    chunkInefficient,
    convertDate,
    convertTime,
    listNumbers,
    listPeriods,
    getCurrentDate,
    ...mapActions(['updateListDates', 'updateListTimes']),
    loadData() {
      this.updateListDates(this.date);
      this.updateListTimes({ date: this.date, locationId: this.locationId, meeting: this.meeting });
    },

    chooseDate(item) {
      if (this.meetingType === true) {
        if (convertDate(this.stopDate, 'YYYY-MM-DD') < convertDate(item.date, 'YYYY-MM-DD')) {
          this.$emit('showMessage', 'Ngày kết thúc phải Lớn hơn ngày đã chọn', 'warning');
          return;
        }
      }
      if (this.meeting !== null && this.typeAction === 'Update') {
        if (item.date === convertDate(this.meeting.started_time, 'YYYY-MM-DD') && this.locationId === this.meeting.location_id) {
          const startTime = convertDate(this.meeting.started_time, 'HH:mm');
          const stopTime = convertDate(this.meeting.finished_time, 'HH:mm');
          this.$emit('selectedTimeMeeting', item.date, startTime, stopTime);
        } else {
          this.$emit('selectedTimeMeeting', item.date, '', '');
        }
      } else {
        this.$emit('selectedTimeMeeting', item.date, '', '');
      }
      this.updateListDates(item.date);
      this.updateListTimes({ date: item.date, locationId: this.locationId, meeting: this.meeting });
      this.selectedDate = item.date;
      this.$emit('selectedDateMeeting', item.date);
    },

    chooseTime(item) {
      const times = this.listTimes.filter(p => p.statusTime === 'visible');
      const beforItem = this.listTimes.filter(p => p.id === item.id - 1);
      const afterItem = this.listTimes.filter(p => p.id === item.id + 1);
      if (times.length === 0) {
        if (item.statusTime === 'empty') {
          item.statusTime = 'visible';
          this.selectedInfoMeeting();
          return;
        }
      }
      if (item.statusTime === 'visible') {
        if (beforItem.length === 0 || afterItem.length === 0) {
          item.statusTime = 'empty';
          this.selectedInfoMeeting();
          return;
        }
        if (beforItem[0].statusTime !== 'visible' || afterItem[0].statusTime !== 'visible') {
          item.statusTime = 'empty';
          this.selectedInfoMeeting();
          return;
        }
        if (beforItem[0].statusTime === 'visible' && afterItem[0].statusTime === 'visible') {
          this.clearTimes();
          item.statusTime = 'visible';
          this.selectedInfoMeeting();
          return;
        }
      }
      if (item.statusTime === 'empty') {
        if (beforItem.length === 0 && afterItem[0].statusTime === 'visible') {
          item.statusTime = 'visible';
          this.selectedInfoMeeting();
          return;
        }
        if (beforItem.length === 0 && afterItem[0].statusTime !== 'visible') {
          this.clearTimes();
          item.statusTime = 'visible';
          this.selectedInfoMeeting();
          return;
        }
        if (afterItem.length === 0 && beforItem[0].statusTime === 'visible') {
          item.statusTime = 'visible';
          this.selectedInfoMeeting();
          return;
        }
        if (afterItem.length === 0 && beforItem[0].statusTime !== 'visible') {
          this.clearTimes();
          item.statusTime = 'visible';
          this.selectedInfoMeeting();
          return;
        }
        if (beforItem[0].statusTime !== 'visible' && afterItem[0].statusTime !== 'visible') {
          this.clearTimes();
          item.statusTime = 'visible';
          this.selectedInfoMeeting();
        } else {
          item.statusTime = 'visible';
          this.selectedInfoMeeting();
        }
      }
    },
    selectedTimeMeetingPeriodic() {
      if (convertDate(this.stopDate, 'YYYY-MM-DD') < this.convertDate(this.date, 'YYYY-MM-DD')) {
        this.$emit('showMessage', 'Ngày kết thúc phải Lớn hơn ngày đã chọn', 'warning');
        this.stopDate = null;
      } else {
        this.$emit('inputTimePeriodics', this.stopDate, this.repeatedDays, this.period);
      }
    },

    selectedInfoMeeting() {
      const listTimeSelected = this.listTimes.filter(p => p.statusTime === 'visible');
      let startTimeSelected = '';
      let stopTimeSelected = '';
      if (listTimeSelected.length !== 0) {
        startTimeSelected = listTimeSelected[0].start;
        stopTimeSelected = listTimeSelected[listTimeSelected.length - 1].stop;
      }
      this.$emit('selectedTimeMeeting', this.selectedDate, startTimeSelected, stopTimeSelected);
    },

    clearTimes() {
      for (let i = 0; i < this.listTimes.length; i += 1) {
        if (this.listTimes[i].statusTime === 'visible') {
          this.listTimes[i].statusTime = 'empty';
        }
      }
    },
  },
};
</script>
<style lang="scss">
@import "@/assets/stylesheets/dialog/dialog-time.scss";
</style>
