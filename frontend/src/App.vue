<template>
  <div id="app">
    <page-header v-if="isShowHeader"></page-header>
    <router-view/>
  </div>
</template>

<script>
import PageHeader from '@/components/Layout/Header';

export default {
  name: 'App',
  components: {
    PageHeader,
  },
  data() {
    return {
      isShowHeader: true,
    };
  },
  watch: {
    $route: 'checkShowHeader',
  },
  beforeMount() {
    this.checkShowHeader();
  },
  methods: {
    checkShowHeader() {
      const notShowHeaderPages = ['Login', 'PageNotFound', 'ServerError'];
      if (notShowHeaderPages.includes(this.$route.name)) {
        this.isShowHeader = false;
      } else {
        this.isShowHeader = true;
      }
    },
  },
};
</script>

<style lang="scss">
@import '@/assets/stylesheets/main.scss';
</style>
