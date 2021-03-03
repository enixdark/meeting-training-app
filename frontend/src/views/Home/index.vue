<template>
  <div>
    <el-container class="home-container" v-if="isShowHome">
      <el-row class="rowAll">
        <el-col :span="14" :offset="5" class="meetings">
          <div class="div-search">
            <el-input class="input-shearch" placeholder="Nhập tên cuộc họp"
              v-model="textShearch">
            </el-input>
            <el-date-picker
              v-model="dateShearch"
              type="date"
              placeholder="Nhập thời gian">
            </el-date-picker>
            <el-button :class="isShearch" @click="shearchMeeting(textShearch, dateShearch)">
              <i class="el-icon-search"></i>
              Tìm kiếm
            </el-button>
          </div>
        </el-col>
        <el-col :span="18" :offset="3" class="book-room">
          <book-room
            @updateSelectedMeeting="updateSelectedMeetingEdit">
          </book-room>
        </el-col>
        <el-col class="meetings" :span="14" :offset="5"
          style="padding-left: 0px; padding-right: 0px">
          <div class="title-meeting-approval">
            <p v-if="isShowApproval">
              {{titleHome}}
            </p>
          </div>
          <div v-if="isShowMeetingHappening">
            <p class="menu-meeting">
              {{meetingHappening.title}}
            </p>
            <meeting class="meeting"
              :meeting="meetingHappening"
              @updateSelectedMeeting="updateSelectedMeeting"
              @resetListMeetingAll="resetListMeetingAll"
              @updateSelectedMeetingEdit="updateSelectedMeetingEdit"
              @removeMeeting="removeMeeting"
              @confirmAction="confirmAction"
              @approvalMeeting="approvalMeeting"
              >
            </meeting>
          </div>
          <div v-if="isShowMeetingEarly">
            <p class="menu-meeting">
              {{meetingEarly.title}}
            </p>
            <meeting class="meeting"
              :meeting="meetingEarly"
              @resetListMeetingAll="resetListMeetingAll"
              @updateSelectedMeeting="updateSelectedMeeting"
              @updateSelectedMeetingEdit="updateSelectedMeetingEdit"
              @removeMeeting="removeMeeting"
              @confirmAction="confirmAction"
              @approvalMeeting="approvalMeeting"
              >
            </meeting>
          </div>
          <div v-if="isShowDailyMeeting">
            <daily-meeting class="daily-meeting"
              :dailyMeeting="item"
              v-for="item in meetingFutures"
              :key="item.id"
              @resetListMeetingAll="resetListMeetingAll"
              @updateSelectedMeeting="updateSelectedMeeting"
              @updateSelectedMeetingEdit="updateSelectedMeetingEdit"
              @removeMeeting="removeMeeting"
              @confirmAction="confirmAction"
              @approvalMeeting="approvalMeeting">
            </daily-meeting>
          </div>
          <div class="button" v-if="isShowBtn">
            <el-button class="btnSeeMore" @click="seeMoreMeeting">
              {{btnName}}
            </el-button>
          </div>
        </el-col>
      </el-row>
    </el-container>
    <div v-if="!isShowHome">
      <check-empty-room
       :meetingFutures="meetingFutures"
      ></check-empty-room>
    </div>
    <show-infor-meeting
      :meetingInfor="selectedMeeting"
      @updateSelectedMeetingEdit="updateSelectedMeetingEdit"
      @removeMeeting="removeMeeting"
      @confirmAction="confirmAction"
      @approvalMeeting="approvalMeeting">
    </show-infor-meeting>
    <show-edit-info-meeting
      :listRooms="listRooms"
      :meetingExit="selectedMeetingEdit"
      :typeAction="action"
      :amount="amount"
      :isComponent="isComponent"
      @loadData="loadData"
      @updateSelectedMeeting="updateSelectedMeetingEdit"
      @removeMeeting="removeMeeting">
    </show-edit-info-meeting>
    <el-dialog title="Thông báo!"
      :visible.sync="dialogVisible" width="30%">
      <span>Bạn có muốn hủy lịch họp không?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteAllMeetingPeriodics">Hủy toàn bộ</el-button>
        <el-button type="danger" @click="deleteOneMeetingPeriodic">Hủy lịch này</el-button>
      </span>
    </el-dialog>
    <el-dialog title="Thông báo!"
      :visible.sync="dialogVisibleApproval" width="30%">
      <span>Bạn có muốn Phê duyệt Lịch định kì không?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="ApprovalAllMeetingPeriodics">Phê duyệt toàn bộ</el-button>
        <el-button type="danger" @click="ApprovalOneMeetingPeriodic">Phê duyệt lịch này</el-button>
      </span>
    </el-dialog>
    <show-duplicate-meetings
      @removeMeeting="removeMeeting"
      @loadData="loadData"
      :meetingApproval="meetingApprovalCurrent"
    ></show-duplicate-meetings>
    <show-export-XLS
    :listRooms="listRooms"
    ></show-export-XLS>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapActions } from 'vuex';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';
import BookRoom from '@/components/Home/BookRoom.vue';
import Meeting from '@/components/Home/Meeting.vue';
import DailyMeeting from '@/components/Home/DailyMeeting.vue';
import ShowInforMeeting from '@/components/Dialog/ShowInforMeeting.vue';
import ShowEditInfoMeeting from '@/components/Dialog/ShowEditInfoMeeting.vue';
import ShowDuplicateMeetings from '@/components/Dialog/ShowDuplicateMeetings.vue';
import ShowExportXLS from '@/components/Dialog/ShowExportXLSFile.vue';
import CheckEmptyRoom from '@/components/Home/CheckEmptyRoom.vue';
import { convertDate } from '@/lib/common.js';
import {
  groupMeetingByDates,
  getListMeetingInToday,
  resetAllMeetings,
  getDataSearch,
} from '@/lib/listMeetings.js';


export default {
  name: 'Home',
  components: {
    BookRoom,
    Meeting,
    DailyMeeting,
    ShowInforMeeting,
    ShowEditInfoMeeting,
    ShowDuplicateMeetings,
    CheckEmptyRoom,
    ShowExportXLS,
  },
  computed: {
    ...mapGetters([
      'listRooms',
      'meetingHappening',
      'isShowMeetingHappening',
      'meetingEarly',
      'isShowMeetingEarly',
      'isShowDailyMeeting',
      'meetingFutures',
      'isShowBtn',
      'isShearch',
      'btnName',
      'isShowHome',
      'isComponent',
      'isShowApproval',
      'titleHome',
      'meetingApprovalCurrent',
    ]),
  },
  data() {
    return {
      selectedMeeting: null,
      selectedMeetingEdit: null,
      selectedMeetingApproval: null,
      action: 'Add',
      amountStart: 2,
      amount: 2,
      limit: 2,
      confirm: null,
      dialogVisible: false,
      dialogVisibleApproval: false,
      meeting: null,
      textShearch: '',
      dateShearch: null,
    };
  },
  created() {
    this.updateIsComponent(1);
    this.loadData();
  },
  methods: {
    convertDate,
    ...mapActions([
      'updateListRooms',
      'updateListEmptyRooms',
      'loadDataMeetings',
      'updateIsShowInfoMeeting',
      'updateIsEditInfoMeeting',
      'updateIsComponent',
      'updateMeetingAwaitingApproval',
      'updateMeetingApprovalCurrent',
      'shearchMeetings',
      'updateIsShearch',
    ]),

    loadData() {
      this.loadDataMeetings(getDataSearch(false, this.amount, '', 's'));
      this.updateListEmptyRooms();
      this.updateListRooms();
    },

    // Sự kiện xem thêm
    seeMoreMeeting() {
      if (this.isComponent === 3) {
        axios({
          method: 'GET',
          url: `${ENDPOINT.GET_ALL_MEETING_APPROVAL}?sort=created_at&order=desc&relations[]=attendees&relations[]=location`,
          headers: {
            Authorization: `jwt ${userServices.userData().jwt}`,
            'Content-Type': 'application/json',
          },
        }).then((response) => {
          const allMeetingFutures = response.data.data;
          const allMeetingFuturesNew = getListMeetingInToday(allMeetingFutures);
          const allMeetingFuturesByDate = groupMeetingByDates(allMeetingFuturesNew);
          const countAll = allMeetingFuturesByDate.length;
          if (this.btnName === 'Xem thêm') {
            if (this.amount >= countAll) {
              this.amount = countAll;
            } else {
              this.amount += this.limit;
            }
            this.loadDataMeetings(
              getDataSearch(this.isShearch, this.amount, this.textShearch, this.dateShearch),
            );
          } else if (countAll - this.limit > 0) {
            if (this.amount - countAll <= 0) {
              this.amount = 2;
            } else {
              this.amount -= this.limit;
            }
            this.loadDataMeetings(
              getDataSearch(this.isShearch, this.amount, this.textShearch, this.dateShearch),
            );
          } else {
            this.loadDataMeetings(
              getDataSearch(this.isShearch, this.amountStart, this.textShearch, this.dateShearch),
            );
          }
        }).catch(() => {
        });
      } else {
        axios({
          method: 'GET',
          url: `${ENDPOINT.GET_ALL_MEETING}?relations%5B%5D=creator&relations%5B%5D=location&relations%5B%5D=attendees`,
          headers: {
            Authorization: `jwt ${userServices.userData().jwt}`,
            'Content-Type': 'application/json',
          },
        }).then((response) => {
          const allMeetingFutures = response.data.data.futures;
          const allMeetingFuturesNew = getListMeetingInToday(allMeetingFutures);
          const allMeetingFuturesByDate = groupMeetingByDates(allMeetingFuturesNew);
          const countAll = allMeetingFuturesByDate.length;
          if (this.btnName === 'Xem thêm') {
            if (this.amount >= countAll) {
              this.amount = countAll;
            } else {
              this.amount += this.limit;
            }
            this.loadDataMeetings(
              getDataSearch(this.isShearch, this.amount, this.textShearch, this.dateShearch),
            );
          } else if (countAll - this.limit > 0) {
            if (this.amount - countAll <= 0) {
              this.amount = 2;
            } else {
              this.amount -= this.limit;
            }
            this.loadDataMeetings(
              getDataSearch(this.isShearch, this.amount, this.textShearch, this.dateShearch),
            );
          } else {
            this.loadDataMeetings(
              getDataSearch(this.isShearch, this.amountStart, this.textShearch, this.dateShearch),
            );
          }
        }).catch(() => {
        });
      }
    },

    // Sự kiện xóa cuộc họp
    removeMeeting(item) {
      this.meeting = item;
      if (!item.is_periodic) {
        this.deleteOneMeetingPeriodic();
      } else {
        this.dialogVisible = true;
      }
    },

    // Huy toan bo lich dinh ky
    deleteAllMeetingPeriodics() {
      this.dialogVisible = false;
      let urlSelected = null;
      let data = null;
      const roleUser = userServices.userData().user.roles;
      if (roleUser.length > 0 && roleUser[0].role_type === 'admin') {
        urlSelected = `${ENDPOINT.DELETE_MEETING_BY_ADMIN}?periodic=true`;
        data = [{
          id: this.meeting.id,
        }];
      } else {
        urlSelected = `${ENDPOINT.DELETE_MEETING_PERIODIC}`;
        data = {
          id: this.meeting.id,
        };
      }
      this.deleteMeeting(urlSelected, data);
    },

    // Huy 1 cuoc hop dinh ki
    deleteOneMeetingPeriodic() {
      this.dialogVisible = false;
      let urlSelected = null;
      const roleUser = userServices.userData().user.roles;
      if (roleUser.length > 0 && roleUser[0].role_type === 'admin') {
        urlSelected = `${ENDPOINT.DELETE_MEETING_BY_ADMIN}`;
      } else {
        urlSelected = `${ENDPOINT.DELETE_MEETING_BY_COORDIRATOR}`;
      }
      const data = [{
        id: this.meeting.id,
      }];
      this.deleteMeeting(urlSelected, data);
    },

    // Xoa 1 cuoc hop bat ki
    deleteMeeting(urlSelected, dataMeeting) {
      this.$confirm('Bạn có chắc chắn muốn hủy không?', 'Thông báo', {
        confirmButtonText: 'Hủy',
        cancelButtonText: 'Đóng',
        type: 'warning',
      }).then(() => {
        axios({
          method: 'DELETE',
          url: urlSelected,
          headers: {
            Authorization: `jwt ${userServices.userData().jwt}`,
            'Content-Type': 'application/json',
          },
          data: dataMeeting,
        }).then(() => {
          this.$message({
            showClose: true,
            message: 'Hủy cuộc họp thành công!',
            type: 'success',
          });
          this.loadData();
          if (this.meetingApprovalCurrent !== null) {
            this.updateMeetingApprovalCurrent(this.meetingApprovalCurrent.meeting);
          }
        }).catch(() => {
          this.$message({
            showClose: true,
            message: 'Không thể xóa cuộc họp này',
            type: 'warning',
          });
        });
      });
    },

    // Xác nhận có tham gia hay k?
    confirmAction(meeting, confirmValue) {
      axios({
        method: 'POST',
        url: `${ENDPOINT.POST_CONFIRM}?meeting_id=${meeting.id}`,
        headers: {
          Authorization: `jwt ${userServices.userData().jwt}`,
          'Content-Type': 'application/json',
        },
        data: {
          confirm_status: confirmValue,
        },
      }).then(() => {
        this.$message({
          showClose: true,
          message: 'Xác nhận thành công!',
          type: 'success',
        });
        this.loadData();
      }).catch(() => {
        this.$message({
          showClose: true,
          message: 'Xác nhận không thành công!',
          type: 'warning',
        });
      });
    },

    // Phê duyệt toàn bộ cuộc họp định kì
    ApprovalAllMeetingPeriodics() {
      let urlSelected = null;
      let dataSelected = null;
      urlSelected = `${ENDPOINT.PATCH_APPROVAL_MEETING}?periodic=true`;
      dataSelected = [{
        id: this.meeting.id,
      }];
      this.approvalMeetingBy(urlSelected, dataSelected);
    },

    // Phê duyệt 1 cuộc họp trong cuộc họp định kì
    ApprovalOneMeetingPeriodic() {
      let urlSelected = null;
      let dataSelected = null;
      urlSelected = `${ENDPOINT.PATCH_APPROVAL_MEETING}`;
      dataSelected = [{
        id: this.meeting.id,
      }];
      this.approvalMeetingBy(urlSelected, dataSelected);
    },

    // Sự kiện phê duyệt cuộc họp
    approvalMeeting(item) {
      let urlSelected = null;
      let dataSelected = null;
      if (item.is_periodic) {
        this.dialogVisibleApproval = true;
        this.meeting = item;
      } else {
        urlSelected = `${ENDPOINT.PATCH_APPROVAL_MEETING}`;
        dataSelected = [{
          id: item.id,
        }];
        this.approvalMeetingBy(urlSelected, dataSelected);
      }
    },

    // phê duyệt 1 cuộc họp bất kì
    approvalMeetingBy(urlSelected, dataSelected) {
      axios({
        method: 'PATCH',
        url: urlSelected,
        headers: {
          Authorization: `jwt ${userServices.userData().jwt}`,
          'Content-Type': 'application/json',
        },
        data: dataSelected,
      }).then(() => {
        this.$message({
          showClose: true,
          message: 'Phê duyệt thành công!',
          type: 'success',
        });
        this.dialogVisibleApproval = false;
        this.loadData();
      }).catch(() => {
        this.$message({
          showClose: true,
          message: 'Phê duyệt không thành công!',
          type: 'warning',
        });
      });
    },

    // Tim kiem cuoc hop
    shearchMeeting(textShearch, dateShearch) {
      if ((textShearch.length <= 0 || textShearch === '' || textShearch === undefined)
      && dateShearch === null) {
        this.$message({
          showClose: true,
          message: 'Bạn chưa nhập thông tin tìm kiếm',
          type: 'warning',
        });
      } else {
        this.updateIsShearch(true);
        this.loadDataMeetings(getDataSearch(true, this.amount, textShearch, dateShearch));
      }
    },

    updateSelectedMeeting(item) {
      this.selectedMeeting = item;
    },

    updateSelectedMeetingEdit(item, act) {
      this.selectedMeetingEdit = item;
      this.action = act;
    },

    resetListMeetingAll() {
      resetAllMeetings(
        this.meetingHappening.meetings,
        this.meetingEarly.meetings,
        this.meetingFutures,
      );
    },
  },
};
</script>
<style lang="scss" scoped>
@import '@/assets/stylesheets/home/index.scss';
</style>
