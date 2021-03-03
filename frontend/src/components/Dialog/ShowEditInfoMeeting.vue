<template>
  <div v-if="isEditInfoMeeting">
    <div class="dialog-background" @click.self="closeCoordinatorEdit">
      <el-card class="corrdination-edit" style="overflow: auto">
        <div class="edit">
          <el-form :model="form">
            <el-form-item label="Nội dung" class="title">
              <el-input v-model="form.title" class="title-input"></el-input>
            </el-form-item>
            <div class="room-time-people">
              <i class="el-icon-date" style="font-size: 12px"></i>
              <p>Book Lịch</p>
              <el-select
                class="select"
                v-model="form.meetingTypeId"
                placeholder
                @change="changeTypeMeetings"
                :disabled="disabledTypeMeeting"
              >
                <el-option
                  class="room-option"
                  v-for="item in listTypeMeetings"
                  :label="item.name"
                  :key="item.id"
                  :value="item.id"
                ></el-option>
              </el-select>
            </div>
            <div class="room-time-people">
              <i class="fas fa-map-marker-alt"></i>
              <p>Địa điểm</p>
              <el-select class="select" v-model="form.locationId" placeholder @change="changeRooms">
                <el-option
                  class="room-option"
                  v-for="item in listRooms"
                  :label="item.name"
                  :key="item.id"
                  :value="item.id"
                ></el-option>
              </el-select>
            </div>
            <div class="room-time-people">
              <i class="fas fa-clock" style="font-size: 13px"></i>
              <p>Thời gian</p>
              <el-avatar style="background: #979797"></el-avatar>
              <p class="status-time">Hết hạn</p>
              <el-avatar style="background: #FF647C"></el-avatar>
              <p class="status-time">Đang bận</p>
              <el-avatar style="background: #6979f8"></el-avatar>
              <p class="status-time">Đang đặt</p>
              <el-avatar class="empty-time" style="background: white"></el-avatar>
              <p class="status-time">Còn trống</p>
            </div>
            <list-times
              class="list-times"
              :meeting="meetingExit"
              :typeAction="typeAction"
              :locationId="form.locationId"
              :startTimeInEdit="startTime"
              :stopTimeInEdit="stopTime"
              :date="date"
              :endDate="endDate"
              :numberPeriodic="numberPeriodic"
              :periodicId="periodicId"
              :meetingType="form.meetingTypeId"
              @selectedDateMeeting="inputDate"
              @selectedTimeMeeting="inputTimes"
              @inputTimePeriodics="inputTimePeriodics"
              @showMessage="showMessage"
            ></list-times>
            <div class="room-time-people">
              <i class="fas fa-pen" style="font-size: 12px"></i>
              <p>Mô tả</p>
            </div>
            <el-input class="contents-input" type="textarea" v-model="form.description"></el-input>
            <div class="room-time-people">
              <i class="fas fa-walking"></i>
              <p style="width: 20%;">Người tham gia({{form.listAttendees.length}})</p>
            </div>
            <attendees
              :meeting="meetingExit"
              :type="typeAction"
              @inputAttendees="inputAttendees">
            </attendees>
            <div class="btn">
              <div class="btn-remove">
                <a @click="removeMeetingsInfo(meetingExit)">Hủy cuộc họp này</a>
              </div>
              <div class="confirm">
                <a @click="closeCoordinatorEdit">Bỏ qua</a>
                <el-button class="btn-save" @click="saveMeeting()">Lưu</el-button>
              </div>
            </div>
          </el-form>
        </div>
      </el-card>
    </div>
    <el-dialog title="Thông báo!"
    :visible.sync="dialogVisible" width="30%">
      <span>Bạn có muốn sửa toàn bộ lịch họp này không?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="updateAllMeetingPeriodics">Sửa toàn bộ</el-button>
        <el-button type="primary" @click="updateOneMeetingPeriodic">Sửa lịch này</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import axios from 'axios';
import { mapGetters, mapActions } from 'vuex';
import { isObject } from 'util';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';
import {
  convertDate,
  fomatDateTime,
  chunkInefficient,
  getCurrentDate,
} from '@/lib/common.js';
import {
  getListMeetingPeriodics,
  formatDataMeeting,
} from '@/lib/listMeetings.js';
import ListTimes from '../EditMeeting/ListTimes.vue';
import Attendees from '../EditMeeting/Attendees.vue';

export default {
  name: 'EditInforMeeting',
  components: {
    ListTimes,
    Attendees,
  },
  props: ['meetingExit', 'listRooms', 'typeAction', 'amount'],
  computed: {
    ...mapGetters(['isEditInfoMeeting']),
  },
  watch: {
    isEditInfoMeeting: 'loadData',
  },
  data() {
    return {
      showDialogTime: false,
      startTime: '',
      stopTime: '',
      date: '',
      endDate: getCurrentDate(),
      numberPeriodic: 1,
      periodicId: 1,
      form: {
        title: '',
        locationId: '',
        meetingTypeId: false,
        description: '',
        listAttendees: [],
      },
      dataEdittoMeeting: [],
      listTypeMeetings: [
        { name: 'Theo ngày', id: false },
        { name: 'Định kì', id: true },
      ],
      dialogVisible: false,
    };
  },
  methods: {
    convertDate,
    fomatDateTime,
    chunkInefficient,
    getCurrentDate,
    ...mapActions([
      'updateIsEditInfoMeeting',
      'updateDialogVisible',
      'updateListDates',
      'updateListTimes',
      'updateListRooms',
      'updateListEmptyRooms',
      'updateMeetingInCurrentDay',
      'updateMeetingFutures',
      'updateIsShowPeriodTimes',
      'updateDataMeetings',
    ]),

    // Load dữ liệu ban đầu
    loadData() {
      this.updateIsShowPeriodTimes(false);
      // Khi book lịch mới
      if (this.meetingExit === null) {
        this.form.title = '';
        this.form.meetingTypeId = false;
        this.disabledTypeMeeting = false;
        this.form.locationId = this.listRooms.slice(0, 1)[0].id;
        this.startTime = '';
        this.stopTime = '';
        this.date = convertDate(new Date(), 'YYYY-MM-DD');
        this.form.description = '';
        this.form.listAttendees = [];
        return;
      }
      // Khi sửa lịch
      if (this.meetingExit !== null && this.typeAction === 'Update') {
        this.form.locationId = this.meetingExit.location_id;
        this.form.title = this.meetingExit.name;
        this.form.meetingTypeId = this.meetingExit.is_periodic;
        this.disabledTypeMeeting = true;
        this.startTime = convertDate(this.meetingExit.started_time, 'HH:mm');
        this.stopTime = convertDate(this.meetingExit.finished_time, 'HH:mm');
        this.date = convertDate(this.meetingExit.started_time, 'YYYY-MM-DD');
        this.form.description = this.meetingExit.description;
        this.form.listAttendees = this.meetingExit.attendees;
        return;
      }

      // Khi book lịch nhanh
      if (this.meetingExit !== null && this.typeAction === 'bookNow') {
        this.form.locationId = this.meetingExit.location.id;
        this.form.title = '';
        this.form.meetingTypeId = false;
        this.disabledTypeMeeting = false;
        this.startTime = this.meetingExit.started_time;
        this.stopTime = this.meetingExit.finished_time;
        this.date = convertDate(new Date(), 'YYYY-MM-DD');
        this.form.description = '';
        this.form.listAttendees = [];
      }
    },

    // Thay đổi loại cuộc họp
    changeTypeMeetings(typeMeeting) {
      if (typeMeeting === true) {
        this.updateIsShowPeriodTimes(true);
      } else {
        this.updateIsShowPeriodTimes(false);
      }
    },

    // Thay đổi phòng họp
    changeRooms(locationIdChange) {
      if (this.meetingExit !== null && this.typeAction === 'Update') {
        if (
          locationIdChange === this.meetingExit.location_id
          && this.date === convertDate(this.meetingExit.started_time, 'YYYY-MM-DD')
        ) {
          this.startTime = convertDate(this.meetingExit.started_time, 'HH:mm');
          this.stopTime = convertDate(this.meetingExit.finished_time, 'HH:mm');
        } else {
          this.startTime = '';
          this.stopTime = '';
        }
      } else {
        this.startTime = '';
        this.stopTime = '';
      }
      this.updateListDates(this.date);
      this.updateListTimes({
        date: this.date,
        locationId: locationIdChange,
        meeting: this.meetingExit,
      });
    },

    // Lưu cuộc họp (Thêm, sửa)
    saveMeeting() {
      if (this.checkInputData()) {
        if (this.typeAction === 'Add' || this.typeAction === 'bookNow') {
          this.postMeeting();
        } else if (this.typeAction === 'Update') {
          const data = new isObject();
          this.getDataToEditOneMeeting(data);
          if (this.form.meetingTypeId === true) {
            this.dialogVisible = true;
          } else {
            this.updateOneMeetingPeriodic();
          }
        }
      }
    },

    // Sửa toàn bộ
    updateAllMeetingPeriodics() {
      const data = new isObject();
      this.getDataToEditOneMeeting(data);
      const role = userServices.userData().user.roles;
      if (role.length > 0 && role[0].role_type === 'admin') {
        this.putMeeting(ENDPOINT.PATCH_MEETING_PERIODIC_BY_ADMIN, [data]);
      } else {
        this.putMeeting(ENDPOINT.PATCH_MEETING_PERIODIC, [data]);
      }
      this.dialogVisible = false;
    },

    // Sửa lịch họp hiện tại
    updateOneMeetingPeriodic() {
      const data = new isObject();
      this.getDataToEditOneMeeting(data);
      const role = userServices.userData().user.roles;
      if (role.length > 0 && role[0].role_type === 'admin') {
        this.putMeeting(ENDPOINT.PATCH_MEETING_BY_ADMIN, [data]);
      } else {
        this.putMeeting(ENDPOINT.PATCH_MEETING, [data]);
      }
      this.dialogVisible = false;
    },

    // Thêm mới lịch họp
    postMeeting() {
      const listMailAttendees = [];
      const role = userServices.userData().user.roles;
      let successMessage = null;
      for (let i = 0; i < this.form.listAttendees.length; i += 1) {
        listMailAttendees.push({
          email: this.form.listAttendees[i].user.email,
        });
      }
      let urlSelected = null;
      if (role.length > 0 && role[0].role_type === 'admin') {
        if (this.form.meetingTypeId !== true) {
          urlSelected = ENDPOINT.POST_MEETING_BY_ADMIN;
        } else {
          urlSelected = `${ENDPOINT.POST_MEETING_BY_ADMIN}?periodic=true`;
        }
        successMessage = 'Book lịch thành công!';
      } else {
        if (this.form.meetingTypeId !== true) {
          urlSelected = ENDPOINT.POST_MEETING;
        } else {
          urlSelected = `${ENDPOINT.POST_MEETING}?periodic=true`;
        }
        successMessage = 'Book lịch thành công!, Đã gửi yêu cầu cho Admin Phê duyệt';
      }

      let dataSelected = null;
      if (this.form.meetingTypeId === true) {
        dataSelected = getListMeetingPeriodics(
          this.getDataMeetingSelected(listMailAttendees),
        );
      } else {
        dataSelected = [
          formatDataMeeting(1, this.getDataMeetingSelected(listMailAttendees)),
        ];
      }
      axios({
        method: 'POST',
        url: urlSelected,
        headers: {
          Authorization: `jwt ${userServices.userData().jwt}`,
          'Content-Type': 'application/json',
        },
        data: dataSelected,
      })
        .then(() => {
          this.closeCoordinatorEdit();
          this.showMessage(successMessage, 'success');
          this.$emit('loadData');
        })
        .catch(() => {
          this.showMessage('Book lịch không thành công!', 'error');
        });
    },

    // Sửa lịch họp
    putMeeting(urlSelected, dataSelected) {
      axios({
        method: 'PATCH',
        url: urlSelected,
        headers: {
          Authorization: `jwt ${userServices.userData().jwt}`,
          'Content-Type': 'application/json',
        },
        data: dataSelected,
      })
        .then(() => {
          this.closeCoordinatorEdit();
          this.showMessage('Sửa lịch họp thành công', 'success');
          this.$emit('loadData');
        })
        .catch((err) => {
          console.log(err.response);
          this.showMessage('Sửa lịch họp không thành công', 'error');
        });
    },

    // format dữ liệu đầu vào để chuyển thành data chuẩn trong API
    getDataMeetingSelected(listMail) {
      const dataMeeting = {
        typeMeeting: this.form.meetingTypeId,
        startDate: this.date,
        stopDate: this.endDate,
        periodicId: this.periodicId,
        numberPeriodic: this.numberPeriodic,
        title: this.form.title,
        description: this.form.description,
        state: true,
        locationId: this.form.locationId,
        startTime: this.startTime,
        stopTime: this.stopTime,
        listMailAttendees: listMail,
      };
      return dataMeeting;
    },

    // Kiểm tra xem những gì thay đổi
    // Chỉ lấy ra những phần thông tin meeting bị thay đổi để UPDATE
    getDataToEditOneMeeting(data) {
      const newLocationId = this.form.locationId;
      const newStartTime = fomatDateTime(this.date, this.startTime);
      const newStopTime = fomatDateTime(this.date, this.stopTime);
      const newName = this.form.title;
      const newDescription = this.form.description;
      const emailCordirator = userServices.userData().user.email;
      const newAttendees = this.form.listAttendees.filter(
        p => p.user.email !== emailCordirator,
      );
      data.id = this.meetingExit.id;
      if (newLocationId !== this.meetingExit.location_id) {
        data.location_id = newLocationId;
        this.updateAttendeesEdit(data);
      }
      if (newName !== this.meetingExit.name) {
        data.name = newName;
      }
      if (newDescription !== this.meetingExit.description) {
        data.description = newDescription;
      }
      if (
        newStartTime !== this.meetingExit.started_time
        || newStopTime !== this.meetingExit.finished_time
      ) {
        data.started_time = newStartTime;
        data.finished_time = newStopTime;
        this.updateAttendeesEdit(data);
      }
      const isChangeAttendees = this.checkAttendeesChange();
      if (
        !isChangeAttendees
        && newLocationId === this.meetingExit.location_id
        && newStartTime === this.meetingExit.started_time
        && newStopTime === this.meetingExit.finished_time
      ) {
        const listMailAttendees = [];
        for (let i = 0; i < newAttendees.length; i += 1) {
          listMailAttendees.push({
            email: newAttendees[i].user.email,
            is_accepted: newAttendees[i].is_accepted,
            may_join: newAttendees[i].may_join,
          });
        }
        data.attendees = listMailAttendees;
      }
    },

    // Kiểm tra xem danh sách Người tham gia có thay đổi không
    checkAttendeesChange() {
      let haveChange = true;
      const oldAttendees = this.meetingExit.attendees;
      const newAttendees = this.form.listAttendees;
      if (newAttendees.length !== oldAttendees.length) {
        haveChange = false;
        return haveChange;
      }
      for (let i = 0; i < oldAttendees.length; i += 1) {
        const newAttendee = oldAttendees.filter(
          p => p.user.email === newAttendees[i].user.email,
        );
        if (newAttendee.length === 0) {
          haveChange = false;
        } else {
          haveChange = true;
        }
      }
      return haveChange;
    },

    // Đưa hết thông tin của Người tham gia về chưa xác nhận Khi thay đổi thời gian
    updateAttendeesEdit(data) {
      const emailCordirator = userServices.userData().user.email;
      const listAttendees = this.form.listAttendees.filter(
        p => p.user.email !== emailCordirator,
      );
      const listMailAttendees = [];
      for (let i = 0; i < listAttendees.length; i += 1) {
        listAttendees[i].is_accepted = false;
        listAttendees[i].may_join = false;
        listMailAttendees.push({
          email: listAttendees[i].user.email,
          is_accepted: listAttendees[i].is_accepted,
          may_join: listAttendees[i].may_join,
        });
      }
      data.attendees = listMailAttendees;
    },

    // Thay đổi ngày họp
    inputDate(date) {
      this.date = date;
    },

    // Thay đổi thời gian họp
    inputTimes(date, start, stop) {
      this.startTime = start;
      this.stopTime = stop;
      this.date = date;
    },

    // Thay đổi thời gian định kì
    inputTimePeriodics(endDate, numberPeriodic, periodicId) {
      this.endDate = endDate;
      this.numberPeriodic = numberPeriodic;
      this.periodicId = periodicId;
    },

    // Thay đổi danh sách Người tham gia
    inputAttendees(listAttendees) {
      this.form.listAttendees = listAttendees;
    },

    // Validate thông tin lịch họp đầu vào
    checkInputData() {
      if (
        this.form.title === ''
        || this.form.description === ''
        || this.startTime === ''
        || this.stopTime === ''
      ) {
        this.showMessage('Bạn nhập thiếu các thông tin bắt buộc!', 'warning');
        return false;
      }
      if (this.form.meetingTypeId === true) {
        if (
          this.endDate === null
          || this.periodicId === null
          || this.numberPeriodic === null
        ) {
          this.showMessage(
            'Bạn nhập thiếu các thông tin bắt buộc cho Lịch họp định kỳ!',
            'warning',
          );
          return false;
        }
      }
      return true;
    },

    // mở dialog
    openDialogVisible() {
      this.updateDialogVisible(true);
    },

    // Đóng giao diện sửa thông tin
    closeCoordinatorEdit() {
      this.updateIsEditInfoMeeting(false);
      this.$emit('getAllMeetings');
      this.$emit('updateSelectedMeeting', null, 'Add');
    },

    // Hủy cuộc họp
    removeMeetingsInfo(meeting) {
      this.$emit('removeMeeting', meeting);
      this.closeCoordinatorEdit();
    },

    showMessage(messageSelected, typeMessage) {
      this.$message({
        showClose: true,
        message: messageSelected,
        type: typeMessage,
      });
    },
  },
};
</script>

<style lang="scss" scope>
@import "@/assets/stylesheets/dialog/edit-info-meeting.scss";
</style>
