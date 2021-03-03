<template>
  <div>
    <div class="peoples" id="peoples-id" v-if="isShowInfoAttendees">
      <div class="people" v-for="attendee in form.attendees" :key="attendee.index">
        <div class="info-people" >
          <el-avatar :size="20" class="avatar">
            <img v-bind:src="attendee.user.avatar_url" />
          </el-avatar>
          <p>
            {{attendee.user.name}} &lt; {{attendee.user.email}} &gt;
          </p>
        </div>
        <i class="el-icon-error" @click="removeUser(attendee)"></i>
      </div>
    </div>
    <div class="attendee-email">
      <el-select
        class="attendee-email"
        v-model="form.id"
        @change="changeInputEmail(form.id)"
        @keydown.enter.native.exact.prevent
        @keyup.enter.native.exact="submitForm"
        :remote="true"
        :remote-method="remoteMethod"
        filterable
        placeholder="thêm người tham gia (enter email mới)">
        <el-option
          style="font-size: 12px;"
          v-for="item in form.mailUsers"
          :key="item.id"
          :label="item.email"
          :value="item.id"
        ></el-option>
      </el-select>
    </div>
    <p v-if="isEmailFormat">
      *  Email mới phải có domain dạng ...@gmail.com hoặc ...@vccorp.vn
    </p>
  </div>
</template>
<script>
import axios from 'axios';
import ENDPOINT from '@/config/endpoint.js';
import userServices from '@/lib/userServices.js';

export default {
  props: ['meeting', 'type'],
  data() {
    return {
      listAllEmailUsers: [],
      isShowInfoAttendees: true,
      isEmailFormat: false,
      newMail: '',
      form: {
        id: '',
        attendees: [],
        mailUsers: [],
      },
    };
  },
  mounted() {
    this.loadData();
  },

  methods: {
    submitForm() {
      const ismailFormatOne = (/^([a-zA-Z0-9])+@(gmail.com)/).test(this.newMail);
      const mailFormatTwo = (/^([a-zA-Z0-9])+@(vccorp.vn)/).test(this.newMail);
      if (ismailFormatOne || mailFormatTwo) {
        let selectedAttendee = [];
        this.isEmailFormat = false;
        if (this.form.attendees !== 0) {
          selectedAttendee = this.form.attendees.filter(p => p.user.email === this.newMail);
        }
        if (selectedAttendee.length === 0) {
          const userNew = {
            name: 'newUser',
            email: this.newMail,
            avatar_url: '',
          };
          this.form.id = null;
          this.form.attendees.push({ user: userNew, is_accepted: false, may_join: false });
          this.isShowInfoAttendees = true;
          this.$emit('inputAttendees', this.form.attendees);
        } else {
          this.$message({
            showClose: true,
            message: 'Mail đã có sẵn',
            type: 'warning',
          });
        }
      } else {
        this.$message({
          showClose: true,
          message: 'Mail không hợp lệ',
          type: 'warning',
        });
        this.isEmailFormat = true;
      }
    },

    loadData() {
      if (this.meeting === null || this.type === 'bookNow') {
        this.form.attendees = [];
      } else {
        this.form.attendees = this.meeting.attendees.slice(0);
      }
      if (this.form.attendees.length === 0) {
        this.isShowInfoAttendees = false;
      } else {
        this.isShowInfoAttendees = true;
      }
    },

    changeInputEmail(id) {
      const user = this.form.mailUsers.find(p => p.id === id);
      if (this.type === 'Update') {
        const selectedUser = this.meeting.attendees.find(p => p.user_id === id);
        if (selectedUser) {
          this.form.attendees.push(selectedUser);
        } else {
          this.form.attendees.push({ user, is_accepted: false, may_join: false });
        }
      } else {
        this.form.attendees.push({ user });
      }
      this.form.mailUsers = this.form.mailUsers.filter(p => p.id !== user.id);
      this.form.id = '';
      this.isShowInfoAttendees = true;
      this.$emit('inputAttendees', this.form.attendees);
    },

    remoteMethod(query) {
      axios({
        method: 'GET',
        url: `${ENDPOINT.GET_USERS}?q=${query}&limit=10`,
        headers: {
          Authorization: `jwt ${userServices.userData().jwt}`,
          'Content-Type': 'application/json',
        },
      }).then((rep) => {
        this.isEmailFormat = false;
        const emailCordirator = userServices.userData().user.email;
        this.listAllEmailUsers = rep.data.data.filter(p => p.email !== emailCordirator);
        this.form.mailUsers = this.listAllEmailUsers;
        for (let i = 0; i < this.form.attendees.length; i += 1) {
          const selectedEmail = this.form.attendees[i].user;
          this.form.mailUsers = this.form.mailUsers.filter(p => p.email !== selectedEmail.email);
        }
      }).catch(() => {
      });
      this.newMail = query;
    },

    removeUser(item) {
      if (item.user.email === userServices.userData().user.email) {
        this.$message({
          showClose: true,
          message: 'Bạn không thể rút khỏi cuộc họp',
          type: 'warning',
        });
      } else {
        this.form.attendees = this.form.attendees.filter(p => p.user.email !== item.user.email);
      }
      this.$emit('inputAttendees', this.form.attendees);
    },
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/stylesheets/edit-meeting/attendees.scss";
</style>
