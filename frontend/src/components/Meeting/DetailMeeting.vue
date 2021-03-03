<template>
  <div class="detail">
    <div class="div-meeting">
      <i class="el-icon-notebook-2"></i>
      <div class="content-div">
        <span style="font-weight: bold;" class="title">{{itemSelected.meeting.name}}</span>
        <p>{{getDayInWeek(itemSelected.meeting.started_time)}}
          Ngày {{convertDate(itemSelected.meeting.started_time, 'DD-MM')}}
        </p>
      </div>
    </div>
    <div class="div-meeting">
      <i class="el-icon-document"></i>
      <div class="content-div">
        <span class="title">Mô tả</span>
        <p>{{itemSelected.meeting.description}}</p>
      </div>
    </div>
    <div class="div-meeting">
      <i class="fas fa-user-friends" style="font-size:15px;color:gray"></i>
      <div class="content-div">
        <span class="title">Người tham gia ({{itemSelected.meeting.attendees.length}})</span>
        <div class="div-meeting"
          v-for="attendee in itemSelected.meeting.attendees" :key="attendee.id">
          <el-avatar :size="20" class="avatar">
            <img v-bind:src="attendee.user.avatar_url" />
          </el-avatar>
          <div class="icon-confirm">
            <i v-if="attendee.is_accepted" class="el-icon-success"
              style="font-size: 12px; color: #3a8ee6;">
            </i>
            <i v-if="!attendee.is_accepted" class="el-icon-error"
              style="font-size: 12px; color: #FF647C;">
            </i>
          </div>
          <div class="content-div">
            <span class="title" style="color: black; font-size: 12px;">
              {{attendee.user.email}}
            </span>
            <p v-if="attendee.is_coordinator">Điều phối viên</p>
          </div>
        </div>
      </div>
    </div>
    <div class="div-meeting">
      <i class="el-icon-user-solid"></i>
      <div class="content-div">
        <span class="title">Người tạo lịch</span>
        <p>{{itemSelected.meeting.creator.name}}</p>
      </div>
    </div>
  </div>
</template>
<script>
import { convertDate, getDayInWeek } from '@/lib/common.js';

export default {
  props: ['itemSelected'],
  methods: {
    convertDate, getDayInWeek,
  },
};
</script>
<style lang="scss" scoped>
@import '@/assets/stylesheets/check-empty-room/test.scss';
</style>
