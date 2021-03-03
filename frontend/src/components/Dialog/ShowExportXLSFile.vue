<template>
  <div>
    <div class="dialog-background" v-if="isShowExprotXLS" @click.self="closeShowExprotXLS">
      <el-card class="export-xls-file">
        <p class="export-title" style="font-weight: bold;">TỔNG HỢP CÁC CUỘC HỌP RA FILE XLS</p>
        <p class="export-title">Theo phòng họp - thời gian</p>
        <div class="roomtime-selected">
          <i class="fas fa-map-marker-alt"></i>
          <p>Địa điểm</p>
          <el-select class="room-select"
          multiple
          collapse-tags
          @change="changeRoom"
          v-model="form.locationId" placeholder>
            <el-option
              class="room-option"
              v-for="item in listRooms"
              :label="item.name"
              :key="item.id"
              :value="item.id"
            ></el-option>
          </el-select>
        </div>
        <div class="chooseAllRoom">
          <el-checkbox v-model="checked" @change="chooseAllRoom"></el-checkbox>
          <p>Chọn tất cả</p>
        </div>
        <div class="roomtime-selected">
          <i class="fas fa-clock"></i>
          <p>Thời gian</p>
          <el-date-picker style="margin-right: 10px;"
            v-model="startDate"
            type="date"
            placeholder="Từ ngày:">
          </el-date-picker>
          <el-date-picker
            v-model="stopDate"
            type="date"
            placeholder="Đến ngày:">
          </el-date-picker>
        </div>
        <div class="btn-export">
          <el-button @click="exportMeetings">Tổng hợp</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
import axios from 'axios';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';
import { convertDate } from '@/lib/common.js';

export default {
  props: ['listRooms'],
  computed: {
    ...mapGetters(['isShowExprotXLS']),
  },
  data() {
    return {
      form: {
        locationId: '',
      },
      checked: false,
      startDate: '',
      stopDate: '',
    };
  },
  watch: {
    isShowExprotXLS: 'loadData',
  },
  methods: {
    convertDate,
    ...mapActions(['updateIsShowExprotXLS']),
    closeShowExprotXLS() {
      this.updateIsShowExprotXLS(false);
    },
    checkValidateData() {
      if ((this.form.locationId === null || this.form.locationId === '') && !this.checked) {
        this.$message({
          message: 'Bạn chưa chọn phòng họp!',
          type: 'warning',
        });
        return false;
      }
      if (this.startDate === null || this.startDate === '') {
        this.$message({
          message: 'Bạn chưa chọn thời gian bắt đầu!',
          type: 'warning',
        });
        return false;
      }
      if (this.stopDate === null || this.stopDate === '') {
        this.$message({
          message: 'Bạn chưa chọn thời gian kết thúc!',
          type: 'warning',
        });
        return false;
      }
      if (this.stopDate < this.startDate) {
        this.$message({
          message: 'Ngày kết thúc phải lớn hơn ngày bắt đầu!',
          type: 'warning',
        });
        return false;
      }
      return true;
    },
    loadData() {
      this.form.locationId = '';
      this.checked = false;
      this.startDate = '';
      this.stopDate = '';
    },
    changeRoom() {
      this.checked = false;
    },
    chooseAllRoom() {
      this.form.locationId = '';
    },
    exportMeetings() {
      const dataSelected = [];
      if (this.checked) {
        this.listRooms.forEach((p) => {
          dataSelected.push({ id: p.id });
        });
      } else {
        this.form.locationId.forEach((p) => {
          dataSelected.push({ id: p });
        });
      }
      if (this.checkValidateData()) {
        axios({
          method: 'POST',
          url: `${ENDPOINT.EXPORT_XLS_FILE}?ge=${convertDate(this.startDate, 'YYYY-MM-DD')}&le=${convertDate(this.stopDate, 'YYYY-MM-DD')}`,
          headers: {
            Authorization: `jwt ${userServices.userData().jwt}`,
            'Content-Type': 'application/json',
          },
          data: dataSelected,
        }).then(() => {
          this.$message({
            message: 'Tổng hợp thành công, hãy vào mail để kiểm tra!',
            type: 'success',
          });
          this.closeShowExprotXLS();
        }).catch(() => {
          this.$message({
            message: 'Tổng hợp không thành công, đã có lỗi!',
            type: 'success',
          });
        });
      }
    },
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/stylesheets/dialog/export-xls.scss";
</style>
