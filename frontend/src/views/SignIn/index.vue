<template>
  <div class="sign-in">
    <el-card class="sign-in-card">
      <h1>
        vMeeting
      </h1>
      <h6>
        Trợ lý book lịch họp
      </h6>
      <h5>
        Chào mừng đã trở lại!
      </h5>
      <el-button class="btn-sign-in" @click="getAuthCode()">
        <i class="fab fa-google"></i>
        <p>
          Đăng nhập với VCCorp
        </p>
      </el-button>
    </el-card>
  </div>
</template>
<script>
import axios from 'axios';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';

export default {
  name: 'SignIn',
  data() {
    return {};
  },
  methods: {
    getAuthCode() {
      this.$gAuth.getAuthCode()
        .then((authCode) => {
          // console.log(authCode);
          this.login(authCode);
        });
    },
    login(codeUser) {
      axios({
        method: 'POST',
        url: ENDPOINT.LOGIN,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        data: {
          code: codeUser,
        },
      }).then((response) => {
        userServices.updateUserData(response.data.data);
        this.$router.push({ name: 'Home' });
      });
    },
  },
};
</script>
<style lang="scss" scope>
  @import "@/assets/stylesheets/auth/sign-in.scss";
</style>
