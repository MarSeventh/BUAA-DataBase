<script lang="ts" setup>
import { ref } from 'vue';
import PlatformSetting from './PlatformSetting.vue';
import ProfileInfo from './ProfileInfo.vue';
import { useAccountStore } from '@/store';

const accountStore = useAccountStore();
accountStore.init();


const name = ref(accountStore.account?.username);
const role = ref(accountStore.role);
</script>


<template>
  <div class="personal">
    <div class="banner w-full rounded-xl p-base items-baseline">
      <a-breadcrumb class="navi">
        <a-breadcrumb-item class="text-text-inverse">Home</a-breadcrumb-item>
        <a-breadcrumb-item>Personal</a-breadcrumb-item>
      </a-breadcrumb>
      <div class="mt-0.5 text-text-inverse text-xl font-semibold">个人中心</div>
      <div
        class="profile flex items-center justify-between p-base bg-container rounded-2xl absolute -bottom-16 left-6 shadow-lg">
        <div class="info flex items-center">
          <img class="w-20 rounded-lg" src="@/assets/avatar/face-1.jpg" />
          <div class="flex flex-col justify-around ml-4">
            <span class="text-title text-xl font-bold">{{ name }}</span>
            <span class="text-subtext font-semibold">{{ role }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-24 flex justify-evenly">
      <PlatformSetting class="flex-1" />
      <ProfileInfo class="flex-1 ml-lg" />
    </div>
  </div>
</template>


<style lang="less" scoped>
.personal {
  .banner {
    height: 240px;
    background-image: url('@/assets/personal-bg.png');
    background-position: 50% 10%;
    background-size: cover;
    position: relative;

    .profile {
      width: calc(~'100% - 48px');
    }

    :deep(.navi) {

      .ant-breadcrumb-link,
      .ant-breadcrumb-separator {
        color: rgba(255, 255, 255, 0.65);
      }

      &>span:last-child .ant-breadcrumb-link {
        @apply text-text-inverse;
      }
    }
  }
}
</style>
