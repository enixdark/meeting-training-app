<template>
  <el-card class="participation" :class="status">
    <div class="card-body">
      <div>
        <i class="el-icon-view"
        v-if="isShowAcitonUserView">
        <span style="color: #6979f8"
          @click="showDialogInforMeeting(itemSelected)">
          Xem thông tin
        </span>
      </i>
      </div>
      <div v-if="itemSelected.meeting.state">
        <i class="el-icon-edit"
        v-if="isShowAcitonCordiratorUpdate">
        <span style="color: #6979f8"
          @click="showDialogEditMeeting(itemSelected)">
          Sửa thông tin
        </span>
      </i>
      </div>
      <div v-if="itemSelected.meeting.state">
        <i class="el-icon-s-custom"
          v-if="isShowAcitonCordiratorChange"
          @click="showBtnChangeCordirator">
          <span style="color: #FF647C">
            Đổi điều phối viên
          </span>
        </i>
      </div>
      <div v-if="!itemSelected.meeting.state">
        <i class="el-icon-s-custom"
          v-if="isShowAcitonAdminApprove"
          @click="approvalMeeting(itemSelected)">
            <span style="color: #FF647C">
              Phê duyệt
            </span>
          </i>
      </div>
      <div v-if="itemSelected.meeting.state">
        <i class="el-icon-d-arrow-left"
          v-if="isShowAcitonAttendeeConfirmed">
          <span style="color: #6979f8"
            @click="confirmAction(itemSelected, 'affirmative')">
            Tham gia
          </span>
        </i>
      </div>
      <div v-if="itemSelected.meeting.state">
        <i class="el-icon-d-arrow-right"
          v-if="isShowAcitonAttendeeNotConfirm">
          <span style="color: #FF647C"
            @click="confirmAction(itemSelected, 'negative')">
            Không Tham Gia
          </span>
        </i>
      </div>
      <i class="el-icon-delete"
        v-if="isShowAcitonCordiratorRemove">
        <span style="color: #FF647C"
          @click="removeMeetingsInfo(itemSelected)">
          Hủy
        </span>
      </i>
      <div v-if="isShowbtnChange">
        <el-select class="select-codirator-new"
          v-model="id" filterable placeholder="Chọn điều phối viên">
          <el-option style="font-size: 12px"
            v-for="item in listAttendees"
            :key="item.user_id"
            :label="item.user.email"
            :value="item.user_id">
          </el-option>
        </el-select>
      </div>
      <div class="btn-change-cordirator"
        v-if="isShowbtnChange">
        <el-button
          @click="changeCordirator(itemSelected)">
          Thay đổi
        </el-button>
      </div>
    </div>
  </el-card>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
import axios from 'axios';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';
import { getDataSearch } from '@/lib/listMeetings.js';

export default {
  props: ['itemSelected'],
  computed: {
    ...mapGetters([
      'isShowAcitonCordiratorUpdate',
      'isShowAcitonCordiratorChange',
      'isShowAcitonCordiratorRemove',
      'isShowAcitonUserView',
      'isShowAcitonAttendeeNotConfirm',
      'isShowAcitonAttendeeConfirmed',
      'isShowAcitonAdminApprove',
      'isShowAcitonAdminRemoveApprove',
    ]),
  },
  data() {
    return {
      isShowbtnChange: false,
      listAttendees: this.itemSelected.meeting.attendees.filter(
        p => p.user_id !== userServices.userData().user.id,
      ),
      status: 'small',
      id: '',
    };
  },
  methods: {
    ...mapActions([
      'updateIsEditInfoMeeting',
      'updateIsShowInfoMeeting',
      'updateListRooms',
      'updateListEmptyRooms',
      'loadDataMeetings',
      'updateListActionChangeCoordirator',
      'updateIsShowDuplicateMeetings',
      'updateMeetingApprovalCurrent',
    ]),
    showDialogEditMeeting(item) {
      this.updateIsEditInfoMeeting(true);
      this.$emit('updateSelectedMeetingEdit', item.meeting, 'Update');
      item.isShowActionMenu = false;
    },

    showDialogInforMeeting(item) {
      this.updateIsShowInfoMeeting(true);
      this.$emit('showInfoMeeting', item);
      item.isShowActionMenu = false;
    },

    close(item) {
      item.isShowActionMenu = false;
    },

    removeMeetingsInfo(item) {
      this.$emit('removeMeeting', item.meeting);
      item.isShowActionMenu = false;
    },

    confirmAction(item, actionValue) {
      this.$emit('confirmAction', item.meeting, actionValue);
      item.isShowActionMenu = false;
    },

    showBtnChangeCordirator() {
      this.status = 'big';
      this.updateListActionChangeCoordirator();
      this.isShowbtnChange = true;
    },

    changeCordirator(item) {
      if (this.id === '') {
        this.$message({
          showClose: true,
          message: 'Bạn chưa chọn điều phối viên mới',
          type: 'warning',
        });
      } else {
        this.$confirm('Bạn có chắc chắn muốn đổi điều phối viên?', 'Thông báo', {
          confirmButtonText: 'Lưu',
          cancelButtonText: 'Đóng',
          type: 'warning',
        }).then(() => {
          axios({
            method: 'PATCH',
            url: `${ENDPOINT.PATCH_CHANGE_CORDIRATOR}?meeting_id=${item.meeting.id}`,
            headers: {
              Authorization: `jwt ${userServices.userData().jwt}`,
              'Content-Type': 'application/json',
            },
            data: {
              coordinator_id: this.id,
            },
          }).then(() => {
            this.$message({
              showClose: true,
              message: 'Đổi điều phối viên thành công!',
              type: 'success',
            });
            this.loadData();
            item.isShowActionMenu = false;
          }).catch(() => {
            this.$message({
              showClose: true,
              message: 'Không thể đổi điều phối viên!',
              type: 'error',
            });
          });
        })
          .catch(() => {
          });
      }
    },

    approvalMeeting(item) {
      if (item.may_request) {
        this.$emit('approvalMeeting', item.meeting);
      } else {
        this.updateMeetingApprovalCurrent(item.meeting);
        this.updateIsShowDuplicateMeetings(true);
      }
      item.isShowActionMenu = false;
    },

    loadData() {
      this.loadDataMeetings(getDataSearch(false, 2, '', ''));
      this.updateListEmptyRooms();
      this.updateListRooms();
    },
  },
};
</script>
<style lang="scss">
@import  "@/assets/stylesheets/meeting/action.scss";
</style>
