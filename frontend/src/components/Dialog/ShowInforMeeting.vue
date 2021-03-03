<template>
  <div v-if="isShowInfoMeeting">
    <div class="dialog-background" @click.self="closeShowInfoMeeting">
      <el-card class="inforMeeting" :class="setSize" style="overflow: auto">
        <div class="div-InforMeeting">
          <div class="title-InforMeeting">
            <i class="el-icon-arrow-left"></i>
            <p>
              {{meetingInfor.meeting.name}}
            </p>
          </div>
          <p class="text-infomation">
            Thông tin
          </p>
          <div>
            <i class="fas fa-map-marker-alt" style="font-size: 16px"></i>
            <p>
              {{meetingInfor.meeting.location.name}}
            </p>
          </div>
          <div>
            <i class="fas fa-clock"></i>
            <p>
              Từ {{convertDate(meetingInfor.meeting.started_time, 'HH:mm')}}
              đến {{convertDate(meetingInfor.meeting.finished_time, 'HH:mm')}},
              {{getDayInWeek(meetingInfor.meeting.started_time)}}
              ngày {{convertDate(meetingInfor.meeting.started_time, 'DD-MM-YYYY')}}
            </p>
          </div>
          <div class="contentsMeeting">
            <i class="fas fa-pen"></i>
            <div class="contents">
              <p>
                {{meetingInfor.meeting.description}}
              </p>
            </div>
          </div>
          <div class="div-peoples">
            <i class="fas fa-walking" style="font-size: 15px"></i>
            <div class="peoples">
              <div class="user" v-for="attendee in listAttenDees" :key="attendee.index">
                <el-avatar :size="18" class="avatar">
                  <img v-bind:src="attendee.user.avatar_url"/>
                </el-avatar>
                <p style="width: 31%;">
                  {{attendee.user.name}}
                </p>
                <p style="width: 35%;">
                  {{attendee.user.email}}
                </p>
                <div class="confirm" :class="'confirm-'+ attendee.is_accepted">
                  <p v-if="!attendee.is_accepted">
                    Chưa xác nhận
                  </p>
                  <p v-if="attendee.is_accepted">
                    Tham gia
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="seeMore" @click="seeMore">
            <a v-if="isShowBtnSeeMore">
              {{btnName}}
            </a>
          </div>
          <div class="btn-confirm-coordinator">
            <a class="remove-meeting"
            v-if="isShowAcitonCordiratorRemove"
            @click="removeMeetingsInfo(meetingInfor.meeting)">
              Hủy cuộc họp này
            </a>
            <div v-if="meetingInfor.meeting.state">
              <a class="not-adhere-meeting" v-if="isShowAcitonAttendeeNotConfirm"
                @click="confirmActionAttendee(meetingInfor.meeting, 'negative')">
                Không tham gia
              </a>
            </div>
            <div v-if="meetingInfor.meeting.state">
              <a class="adhere-meeting" v-if="isShowAcitonAttendeeConfirmed"
                @click="confirmActionAttendee(meetingInfor.meeting, 'affirmative')">
                Tham gia
              </a>
            </div>
            <div class="div-btn">
              <a class="not-adhere-meeting" v-if="isShowOfUser"
                @click="closeShowInfoMeeting">
                Bỏ qua
              </a>
              <div v-if="meetingInfor.meeting.state">
                <el-button class="btn-update" v-if="isShowAcitonCordiratorUpdate"
                  @click="showEditInfoMeeting">
                    Sửa
                </el-button>
              </div>
              <el-button class="btn-update" v-if="isShowAcitonAdminApprove"
                @click="approvalMeeting(meetingInfor)">
                Phê duyệt
              </el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex';
import {
  getDayInWeek,
  convertDate,
} from '@/lib/common.js';

export default {
  name: 'InfoMeeting',
  props: ['meetingInfor'],
  computed: {
    ...mapGetters([
      'isShowInfoMeeting',
      'isShowAcitonAttendeeNotConfirm',
      'isShowAcitonAttendeeConfirmed',
      'isShowAcitonCordiratorRemove',
      'isShowAcitonCordiratorUpdate',
      'isShowAcitonAdminApprove',
    ]),
  },
  data() {
    return {
      listAttenDees: [],
      isShowBtnSeeMore: true,
      btnName: 'Xem thêm',
      amount: 5,
      setSize: '',
    };
  },
  watch: {
    isShowInfoMeeting: 'loadData',
  },
  methods: {
    convertDate,
    getDayInWeek,
    ...mapActions([
      'updateIsShowInfoMeeting',
      'updateIsEditInfoMeeting',
      'updateListActionWhenClickMenu',
      'updateIsShowDuplicateMeetings',
      'updateMeetingApprovalCurrent',
    ]),

    loadData() {
      const amountAttendees = this.meetingInfor.meeting.attendees.length;
      if (amountAttendees <= 5) {
        if (amountAttendees === 5) {
          this.setSize = 'size-small-5';
        }
        if (amountAttendees === 4) {
          this.setSize = 'size-small-4';
        }
        if (amountAttendees === 3) {
          this.setSize = 'size-small-3';
        }
        if (amountAttendees === 2) {
          this.setSize = 'size-small-2';
        }
        if (amountAttendees === 1) {
          this.setSize = 'size-small-1';
        }
      } else {
        this.setSize = 'size-big';
      }
      this.checkIsCoodirator(this.meetingInfor.meeting);
      this.loadEmailAttendees(this.amount);
      this.updateListActionWhenClickMenu(this.meetingInfor.meeting);
    },

    loadEmailAttendees(amount) {
      const count = this.meetingInfor.meeting.attendees.length;
      if (amount < count) {
        this.isShowBtnSeeMore = true;
        this.btnName = 'Xem thêm';
        this.listAttenDees = this.meetingInfor.meeting.attendees.slice(0, amount);
      } else {
        this.isShowBtnSeeMore = false;
        this.listAttenDees = this.meetingInfor.meeting.attendees;
      }
    },

    seeMore() {
      if (this.btnName === 'Xem thêm') {
        this.listAttenDees = this.meetingInfor.meeting.attendees;
        this.btnName = 'Ẩn bớt';
      } else {
        this.listAttenDees = this.meetingInfor.meeting.attendees.slice(0, this.amount);
        this.btnName = 'Xem thêm';
      }
    },

    showEditInfoMeeting() {
      this.updateIsEditInfoMeeting(true);
      this.updateIsShowInfoMeeting(false);
      this.$emit('updateSelectedMeetingEdit', this.meetingInfor.meeting, 'Update');
    },

    checkIsCoodirator() {
      this.isShowOfUser = true;
    },

    removeMeetingsInfo(meeting) {
      this.$emit('removeMeeting', meeting);
      this.updateIsShowInfoMeeting(false);
    },

    confirmActionAttendee(meeting, actionValue) {
      this.$emit('confirmAction', meeting, actionValue);
      this.closeShowInfoMeeting();
    },

    closeShowInfoMeeting() {
      this.updateIsShowInfoMeeting(false);
    },

    approvalMeeting(item) {
      this.closeShowInfoMeeting();
      if (item.may_request) {
        this.$emit('approvalMeeting', item.meeting);
      } else {
        this.updateMeetingApprovalCurrent(item.meeting);
        this.updateIsShowDuplicateMeetings(true);
      }
      item.isShowActionMenu = false;
    },
  },
};
</script>
<style lang="scss" scope>
@import '@/assets/stylesheets/dialog/infor-meeting.scss';
</style>
