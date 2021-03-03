<template>
<div v-if="isShowBookRoom">
    <el-carousel indicator-position="none" :autoplay="true" :arrow="isShowarrow">
      <el-carousel-item v-for="items in chunkInefficient(listEmptyRooms, 2)" :key="items.index">
        <div class="item-carousel">
          <div class="item-card">
            <el-card v-for="item in items" :key="item.index">
              <div class="book-room">
                <p style="color: #3a8ee6; font-weight: bold">
                  {{ item.locationName }}
                </p>
                <p>
                  Trống từ: {{convertTime(item.room.start, 'HH:mm')}}
                  đến: {{convertTime(item.room.finish, 'HH:mm')}}
                </p>
                <el-button
                  @click="bookRoomNow(
                  convertTime(item.room.start, 'HH:mm'),
                  convertTime(item.room.finish, 'HH:mm'),
                  item.locationId)">
                  Đặt ngay
                </el-button>
              </div>
            </el-card>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { chunkInefficient, convertTime, fomatDateTime } from '@/lib/common.js';

export default {
  name: 'BookRoom',
  computed: {
    ...mapGetters(['listEmptyRooms']),
  },
  data() {
    return {
      isShowBookRoom: false,
      isShowarrow: 'always',
      meeting: {
        started_time: '',
        finished_time: '',
        location: {
          id: '',
        },
      },
    };
  },

  watch: {
    listEmptyRooms: 'updateIsShowBookRoom',
  },

  methods: {
    chunkInefficient,
    convertTime,
    ...mapActions(['updateIsEditInfoMeeting']),
    updateIsShowBookRoom() {
      if (this.listEmptyRooms.length > 0) {
        this.isShowBookRoom = true;
      } else if (this.listEmptyRooms.length === 0) {
        this.isShowBookRoom = false;
      }
      if (this.listEmptyRooms.length <= 2) {
        this.isShowarrow = 'never';
      } else if (this.listEmptyRooms.length >= 2) {
        this.isShowarrow = 'always';
      }
    },

    bookRoomNow(startTime, stopTime, roomId) {
      this.updateIsEditInfoMeeting(true);
      this.meeting.started_time = fomatDateTime(new Date(), startTime);
      this.meeting.finished_time = fomatDateTime(new Date(), stopTime);
      this.meeting.location.id = roomId;
      this.$emit('updateSelectedMeeting', this.meeting, 'bookNow');
    },
  },
};
</script>
<style lang="scss">
@import '@/assets/stylesheets/home/book-room.scss';
</style>
