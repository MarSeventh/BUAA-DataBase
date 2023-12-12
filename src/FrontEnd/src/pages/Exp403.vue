<script lang="ts" setup>
  import { useRoute } from 'vue-router';
  import { useAccountStore } from '@/store';

  const accountStore = useAccountStore();
  
  const mypermission = accountStore.permissions;
  defineProps({
    permission: String,
    path: String,
  });
  console.log(useRoute());
</script>
<template>
  <div>
    <div>403 Forbidden (no permission)</div>
    <div>path: {{ path }}</div>
    <div>
      need permission: <a-tag color="blue">{{ permission }}</a-tag>
      your permission: <a-tag color="blue">{{ mypermission }}</a-tag>
    </div>
  </div>
</template>
