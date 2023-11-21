<script lang="ts" setup>
  import { useRouter } from 'vue-router';

  const router = useRouter();
  function signIn() {
    router.push('/login');
  }
</script>
<template>
  <div class="home text-center flex flex-col justify-center">
    <div class="transform w-full">
      <div class="tracking-wide slogan text-[3.5rem] xl:text-[5.25rem] font-extralight" style="color: rgb(255, 255, 255);">
        <span class="font-semibold">智慧医航</span>
      </div>
      <p class="text-subtext text-[1.5rem] xl:text-[1.75rem] font-extralight tracking-wide" style="color: rgb(255, 255, 255);">
        北航校医院智慧管理系统
      </p>
      <button
        @click="signIn"
        class="bg-primary-300 hover:bg-primary-400 cursor-pointer mt-lg shadow border-0 outline-none text-xl px-[64px] py-lg rounded-sm"
      >
        登录
      </button>
    </div>
  </div>
</template>
<style scoped lang="less">
  .home {
    min-height: max(100vh, 600px);
    margin-top: -78px;
  }
</style>
