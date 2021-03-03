<template>
  <div class="name" :style="{background:data.colorPair}">
    <div class="carId">
      <p>
        {{data.name}}
      </p>
      <span>
        ({{data.address}})
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestLeft',
  props: {
    data: Object,
  },
};
</script>

<style lang="scss" scope>
@import '@/assets/stylesheets/check-empty-room/test-left.scss';
</style>
