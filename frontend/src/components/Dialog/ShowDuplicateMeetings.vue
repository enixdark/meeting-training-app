<template>
<div>
  <div class="dialog-background" v-if="isShowDialogDuplicateMeetings"
    @click.self="closeShowInfoMeeting">
      <el-card class="duplicate-meeting">
        <div class="div-conten">
          <i class="el-icon-date"  style="font-size: 16px;"></i>
          <p>
            {{getDayInWeek(meetingApprovalCurrent.meeting.started_time)}},
            Ngày: {{convertDate(meetingApprovalCurrent.meeting.started_time, 'DD-MM-YYYY')}}
          </p>
        </div>
        <div class="div-conten">
          <i class="fas fa-map-marker-alt"></i>
          <p>
            {{meetingApprovalCurrent.meeting.location.name}}
            <span>
              ({{meetingApprovalCurrent.meeting.location.address}})
            </span>
          </p>
        </div>
        <p class="meeting-approval-title">
          CUỘC HỌP HIỆN TẠI ĐANG PHÊ DUYỆT
        </p>
        <div >
          <el-popover placement="right" trigger="hover">
            <div slot="reference" class="conten-meeting"
              @mouseover="hoverMeeting(meetingApprovalCurrent.meeting)">
              <p class="title-meeting"> {{meetingApprovalCurrent.meeting.name}} </p>
              <p>
                Từ:
                <span>{{convertDate(meetingApprovalCurrent.meeting.started_time, 'HH:mm')}}</span>
                Đến:
                <span>{{convertDate(meetingApprovalCurrent.meeting.finished_time, 'HH:mm')}}</span>
              </p>
            </div>
            <div>
              <detail-meeting :itemSelected="meetingApprovalSelected"></detail-meeting>
            </div>
          </el-popover>
          <div class="button-admin">
            <el-button class="btn-approval" v-if="!meetingApprovalCurrent.meeting.state"
              @click="approvalMeeting(meetingApprovalCurrent.meeting)">
              Phê duyệt
            </el-button>
            <el-button class="btn-remove" @click="removeMeeting(meetingApprovalCurrent.meeting)">
              Hủy
            </el-button>
          </div>
        </div>
        <p class="duplicates-title" v-if="isShowDuplicatesTitle">
          DANH SÁCH CÁC CUỘC HỌP KHÁC CÙNG KHUNG GIỜ
        </p>
        <div v-for="item in meetingApprovalCurrent.duplicates" :key="item.index">
          <el-popover placement="right" trigger="hover">
            <div slot="reference" class="conten-meeting" @mouseover="hoverMeeting(item)">
              <p class="title-meeting"> {{item.name}} </p>
              <p>
                Từ:
                <span>{{convertDate(item.started_time, 'HH:mm')}}</span>
                Đến:
                <span>{{convertDate(item.finished_time, 'HH:mm')}}</span>
              </p>
            </div>
            <div>
              <detail-meeting :itemSelected="meetingApprovalSelected"></detail-meeting>
            </div>
          </el-popover>
          <div class="button-admin">
            <el-button class="btn-approval" v-if="!item.state"
            @click="approvalMeeting(item)">
              Phê duyệt
            </el-button>
            <el-button class="btn-remove"
            @click="removeMeeting(item)">
              Hủy
            </el-button>
          </div>
        </div>
      </el-card>
  </div>
</div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
import axios from 'axios';
import {
  getDayInWeek,
  convertDate,
} from '@/lib/common.js';
import DetailMeeting from '@/components/Meeting/DetailMeeting.vue';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';

export default {
  components: {
    DetailMeeting,
  },
  computed: {
    ...mapGetters([
      'isShowDialogDuplicateMeetings',
      'meetingApprovalCurrent',
      'isShowDuplicatesTitle',
    ]),
  },
  data() {
    return {
      meetingApprovalSelected: {
        meeting: {
          name: '',
          started_time: '',
          finished_time: '',
          description: '',
          attendees: '',
          creator: {
            name: '',
          },
        },
      },
    };
  },
  methods: {
    getDayInWeek,
    convertDate,
    ...mapActions(['updateIsShowDuplicateMeetings', 'updateMeetingApprovalCurrent']),
    closeShowInfoMeeting() {
      this.updateIsShowDuplicateMeetings(false);
    },

    // sự kiện hover
    hoverMeeting(item) {
      axios({
        method: 'GET',
        url: `${ENDPOINT.GET_MEETING}?id=${item.id}&relations[]=creator&relations[]=location&relations[]=attendees`,
        headers: {
          Authorization: `jwt ${userServices.userData().jwt}`,
          'Content-Type': 'application/json',
        },
      }).then((response) => {
        this.meetingApprovalSelected.meeting = response.data.data;
      }).catch(() => {
      });
    },

    // hủy 1 cuộc họp
    removeMeeting(item) {
      this.$emit('removeMeeting', item);
      if (item.id === this.meetingApprovalCurrent.meeting.id) {
        this.closeShowInfoMeeting();
      }
    },

    // Phê duyệt 1 cuộc họp
    approvalMeeting(item) {
      axios({
        method: 'GET',
        url: `${ENDPOINT.GET_ALL_MEETING_APPROVAL}?sort=created_at&order=desc&relations[]=attendees&relations[]=location`,
        headers: {
          Authorization: `jwt ${userServices.userData().jwt}`,
          'Content-Type': 'application/json',
        },
      }).then((res) => {
        const allMeetingApproval = res.data.data;
        const meetingFilter = allMeetingApproval.filter(p => p.meeting.id === item.id);
        if (meetingFilter[0].may_request) {
          this.$emit('approvalMeeting', meetingFilter[0].meeting);
          if (item.id === this.meetingApprovalCurrent.meeting.id) {
            this.closeShowInfoMeeting();
          } else {
            this.updateMeetingApprovalCurrent(item);
          }
        } else {
          if (item.id !== this.meetingApprovalCurrent.meeting.id) {
            this.updateMeetingApprovalCurrent(item);
          }
          this.$message({
            showClose: true,
            message: 'Có cuộc họp đã phê duyệt cùng khung giờ, Bạn phải hủy trước khi phê duyệt cuộc họp này!',
            type: 'warning',
          });
        }
      }).catch(() => {
      });
    },
  },
};
</script>
<style lang="scss" scoped>
@import '@/assets/stylesheets/dialog/duplicate-meetings.scss';
</style>
