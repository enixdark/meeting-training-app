<template >
  <el-container class="daily-meeting">
    <div class="weekdays-date">
      <p>
        {{getDayInWeek(dailyMeeting.date)}},
        Ngày: {{convertDate(dailyMeeting.date, 'DD-MM')}}
      </p>
    </div>
    <div class="div-daily-meeting">
      <el-card class="card-daily-meeting"
        v-for="itemFuture in dailyMeeting.meetings"
        :key="itemFuture.index"
        >
        <div class="div-margin">
          <div class="part1-daily-meeting">
            <div class="title-daily-meeting">
              <p @click="showDialogInfoMeeting(itemFuture)">
                {{itemFuture.meeting.name}}
              </p>
            </div>
            <div class="action-menu"
              @click="showActionMenu(itemFuture)"
              v-if="!itemFuture.isShowActionMenu">
              <i class="fas fa-ellipsis-v"></i>
            </div>
            <div
              class="action-menu-close"
              @click="itemFuture.isShowActionMenu = false"
              v-if="itemFuture.isShowActionMenu">
              <i class="el-icon-close"></i>
            </div>
          </div>
          <div class="part2-daily-meeting">
            <div class="start-stop">
              <i class="el-icon-time"></i>
              <p>
                từ {{convertDate(itemFuture.meeting.started_time, 'HH:mm')}}
                đến {{convertDate(itemFuture.meeting.finished_time, 'HH:mm')}}
              </p>
            </div>
            <div class="room">
              <i class="el-icon-location-outline"></i>
              <p>
                {{itemFuture.meeting.location.name}}
              </p>
            </div>
            <div class="peoples">
              <i class="fas fa-walking"></i>
              <el-dropdown :hide-on-click="false">
              <span class="el-dropdown-link">
                {{itemFuture.meeting.attendees.length}} người tham gia
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                  style="
                    font-size: 10px;
                    display: flex;
                    height: 25px;
                    align-items: center;"
                  v-for="attendee in itemFuture.meeting.attendees" :key="attendee.index">
                  <el-avatar :size="15" class="avatar"
                    style="margin-right: 10px;">
                    <img v-bind:src="attendee.user.avatar_url" />
                  </el-avatar>
                  <p>
                    {{attendee.user.email}}
                  </p>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            </div>
            <div class="isApproval" v-if="!itemFuture.meeting.state">
              <p>
                Chưa phê duyệt
              </p>
            </div>
          </div>
        </div>
        <action
          :itemSelected="itemFuture"
          @showInfoMeeting="showDialogInfoMeeting"
          @updateSelectedMeetingEdit="updateSelectedMeetingEditOfMenu"
          @removeMeeting="removeMeetingsEarly"
          @confirmAction="confirmActionOfUserInMeetingFuture"
          @approvalMeeting="approvalMeetingOfAdmin"
          @updateMeetingApproval="updateMeetingApproval"
          v-if="itemFuture.isShowActionMenu">
        </action>
      </el-card>
    </div>
  </el-container>
</template>
<script>
import { mapActions } from 'vuex';
import userServices from '@/lib/userServices.js';
import Action from '../Meeting/Action.vue';
import {
  getDayInWeek,
  convertDate,
} from '@/lib/common.js';

export default {
  name: 'DailyMeeting',
  components: {
    Action,
  },
  props: ['dailyMeeting'],
  data() {
    return {
      emailUser: userServices.userData().user.email,
    };
  },

  methods: {
    getDayInWeek,
    convertDate,
    ...mapActions([
      'updateIsShowInfoMeeting',
      'updateListActionWhenClickMenu',
    ]),
    showDialogInfoMeeting(meeting) {
      this.updateIsShowInfoMeeting(true);
      this.$emit('updateSelectedMeeting', meeting);
    },

    showActionMenu(item) {
      this.$emit('resetListMeetingAll');
      this.updateListActionWhenClickMenu(item.meeting);
      item.isShowActionMenu = true;
    },

    updateMeetingApproval(item) {
      this.$emit('updateSelectedApproval', item);
    },

    updateSelectedMeetingEditOfMenu(item, action) {
      this.$emit('updateSelectedMeetingEdit', item, action);
    },

    removeMeetingsEarly(meeting) {
      this.$emit('removeMeeting', meeting);
    },

    confirmActionOfUserInMeetingFuture(meeting, actionValue) {
      this.$emit('confirmAction', meeting, actionValue);
    },

    approvalMeetingOfAdmin(meeting) {
      this.$emit('approvalMeeting', meeting);
    },
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/stylesheets/home/daily-meeting.scss";
</style>
