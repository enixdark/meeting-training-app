<template>
  <el-container>
    <el-row :gutter="0" class="header-main">
      <el-col :span="2" class="header-name">
        <el-link :underline="false" @click="loadData(1)">
          vMeeting
        </el-link>
      </el-col>
      <el-col :span="22" class="header-menu">
        <el-menu mode="horizontal">
          <el-menu-item index="1" class="header-menu__item" @click="openCheckEmptyRoom">
            Check phòng
          </el-menu-item>
          <el-menu-item index="2" class="header-menu__item" @click="openCoordinatorEdit">
            Book lịch
          </el-menu-item>
          <el-menu-item index="3" class="header-menu__item" @click="loadData(2)">
            Lịch của tôi
          </el-menu-item>
          <el-menu-item index="4" class="header-menu__item" @click="loadData(3)">
            Phê duyệt
          </el-menu-item>
          <el-menu-item index="4" class="header-menu__item"
            @click="showExportXLS" v-if="isShowExport">
            Tổng hợp
          </el-menu-item>
          <el-menu-item index="4" class="header-menu__logout" @click="signOut">
            <el-avatar :size="24" >
              <img  v-bind:src="srcImage" alt="">
            </el-avatar>
            <span>
              Đăng Xuất
            </span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
  </el-container>
</template>
<script>
import { mapActions } from 'vuex';
import userServices from '@/lib/userServices.js';
import { getDataSearch } from '@/lib/listMeetings.js';


export default {
  name: 'Header',
  components: {
  },
  data() {
    return {
      srcImage: userServices.userData().user.avatar_url,
      isShowExport: true,
    };
  },
  mounted() {
    this.display();
  },
  methods: {
    ...mapActions([
      'updateIsShowHome',
      'updateIsEditInfoMeeting',
      'loadDataMeetings',
      'updateListEmptyRooms',
      'updateIsComponent',
      'updateMeetingAwaitingApproval',
      'updateIsShearch',
      'updateIsShowExprotXLS',
    ]),

    openCoordinatorEdit() {
      this.updateIsEditInfoMeeting(true);
    },

    signOut() {
      userServices.signOut();
      this.$router.push({ name: 'Login' });
    },

    loadData(item) {
      this.updateIsShearch(false);
      this.updateIsShowHome(true);
      this.updateIsComponent(item);
      this.loadDataMeetings(getDataSearch(false, 2, '', ''));
      this.updateListEmptyRooms();
    },
    openCheckEmptyRoom() {
      this.updateIsShowHome(false);
    },
    showExportXLS() {
      this.updateIsShowExprotXLS(true);
    },
    display() {
      const isroleUser = userServices.userData().user.roles;
      if (isroleUser.length === 0) {
        this.isShowExport = false;
      } else if (isroleUser[0].role_type === 'admin') {
        this.isShowExport = true;
      } else {
        this.isShowExport = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/assets/stylesheets/layout/header.scss'
</style>
