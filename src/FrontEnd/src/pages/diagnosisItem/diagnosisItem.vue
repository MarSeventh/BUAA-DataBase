<script lang="ts" setup>
import { useAccountStore } from '@/store';
import { computed } from 'vue';
import diagnosisInfo from './diagnosisInfo.vue';
import { useRoute } from "vue-router";

const route = useRoute()

var id = route.query.id

  const accountStore = useAccountStore();
  accountStore.init();
const accountName = computed(() => accountStore.account?.username);

const currentTime = new Date().getHours();
const greeting = computed(
    () => (currentTime < 12 ? '上午好' : currentTime < 18 ? '下午好' : '晚上好')
);
</script >

<template>
    <div class="welcome grid grid-rows-none gap-4 mt-xxs">
        <div class="bg-container p-base rounded-b-lg rounded-tr-lg pt-8 flex items-end justify-between">
            <div class="flex items-center">
                <img src="@/assets/avatar/face-1.jpg" class="w-16 h-16 rounded-full" />
                <div class="ml-base">
                    <div class="text-title font-bold text-lg">{{ greeting }}，{{ accountName }}</div>
                    <div class="text-subtext font-bold text-sm">这是您编号为{{ id }}的诊断结果</div>
                </div>
            </div>
        </div>
    </div>
    <div class="mt-15 flex justify-evenly">
        <diagnosisInfo class="flex-1 mr-lg" />
    </div>
</template>


<style scoped lang="less">
.welcome {}
</style>