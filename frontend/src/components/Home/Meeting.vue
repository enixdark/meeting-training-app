<template>
  <el-container class="meeting">
    <el-card class="card-meeting" v-for="item in meeting.meetings" :key="item.index">
      <div class="div-meeting">
        <div class="part1-meeting">
          <div class="time-meeting">
            <div class="time">
              <div class="time-text">
                <p>
                  từ
                </p>
              </div>
              <p>
                {{convertDate(item.meeting.started_time, 'HH:mm')}}
              </p>
            </div>
            <div class="time">
              <div class="time-text">
                <p>
                  đến
                </p>
              </div>
              <p>
                {{convertDate(item.meeting.finished_time, 'HH:mm')}}
              </p>
            </div>
          </div>
          <div class="contens-meeting" @click="showInfoMeeting(item)">
            <p>
              {{item.meeting.name}}
            </p>
          </div>
          <div class="action-menu"
            @click="showActionMenu(item)" v-if="!item.isShowActionMenu">
            <i class="fas fa-ellipsis-v"></i>
          </div>
          <div
            class="action-menu-close"
            @click="item.isShowActionMenu = false"
            v-if="item.isShowActionMenu">
            <i class="el-icon-close"></i>
          </div>
        </div>
        <div class="part2-meeting">
          <div class="confirm" :class="item.isConfirmAction">
            <p v-if="item.notConfirm">
              Chưa xác nhận
            </p>
            <p v-if="item.notAdhere">
              Không phận sự
            </p>
            <p v-if="item.accepted">
              Tham gia
            </p>
            <p v-if="item.notAccepted">
              Không tham gia
            </p>
            <p v-if="!item.meeting.state">
              Chưa phê duyệt
            </p>
          </div>
          <div>
          </div>
          <div class="peoples">
            <i class="fas fa-walking"></i>
            <el-dropdown :hide-on-click="false">
              <span class="el-dropdown-link">
                {{item.meeting.attendees.length}} người tham gia
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                  style="
                    font-size: 10px;
                    display: flex;
                    height: 25px;
                    align-items: center;"
                  v-for="attendee in item.meeting.attendees" :key="attendee.index">
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
          <div class="room">
            <i class="el-icon-location-outline"></i>
            <p>
              {{item.meeting.location.name}}
            </p>
          </div>
          <div class="distance">
            <i class="el-icon-time"></i>
            <p>
              {{getTime(item.meeting.started_time, item.meeting.finished_time)}} Phút
            </p>
          </div>
        </div>
      </div>
      <action style="margin-top: -32px"
        :itemSelected="item"
        @showInfoMeeting="showInfoMeeting"
        @updateSelectedMeetingEdit="updateSelectedMeetingEditOfMenu"
        @removeMeeting="removeMeetingsInfo"
        @confirmAction="confirmActionOfUser"
        @approvalMeeting="approvalMeetingOfAdmin"
        v-if="item.isShowActionMenu">
      </action>
    </el-card>
  </el-container>
</template>
<script>
import { mapActions } from 'vuex';
import { convertDate, getTime } from '@/lib/common.js';
import Action from '../Meeting/Action.vue';

export default {
  name: 'Meeting',
  components: {
    Action,
  },
  props: ['meeting'],
  data() {
    return {
      iconfirmAction: true,
    };
  },
  methods: {
    convertDate,
    getTime,
    ...mapActions([
      'updateIsShowInfoMeeting',
      'updateIsEditInfoMeeting',
      'updateListActionWhenClickMenu',
    ]),
    showInfoMeeting(meeting) {
      this.updateIsShowInfoMeeting(true);
      this.$emit('updateSelectedMeeting', meeting);
    },

    showActionMenu(item) {
      this.$emit('resetListMeetingAll');
      this.updateListActionWhenClickMenu(item.meeting);
      item.isShowActionMenu = true;
    },

    updateSelectedMeetingEditOfMenu(item, act) {
      this.$emit('updateSelectedMeetingEdit', item, act);
    },

    removeMeetingsInfo(meeting) {
      this.$emit('removeMeeting', meeting);
    },

    confirmActionOfUser(meeting, actionValue) {
      this.$emit('confirmAction', meeting, actionValue);
    },

    approvalMeetingOfAdmin(meeting) {
      this.$emit('approvalMeeting', meeting);
    },
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/stylesheets/home/meeting.scss";
</style>
