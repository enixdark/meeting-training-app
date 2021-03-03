<template>
  <el-container>
    <el-row :gutter="20">
      <el-col class="text-center py-5" :span="12" :offset="6">
        <img src="@/assets/images/errors/500.svg" alt="404">
        <router-link :to="{ path: '/' }">Quay lại trang chủ</router-link>
      </el-col>
    </el-row>
  </el-container>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>
