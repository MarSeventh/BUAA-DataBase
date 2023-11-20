<script lang="ts" setup>
import DepartmentTable from './departmentTable.vue';
import { useAccountStore } from '@/store';
import { computed } from 'vue';

const accountStore = useAccountStore();
const accountName = computed(() => accountStore.account?.username);

const currentTime = new Date().getHours();
const greeting = computed(
    () => (currentTime < 12 ? '上午好' : currentTime < 18 ? '下午好' : '晚上好')
);
</script >

<template>
    <div class="personal">
        <div class="banner w-full rounded-xl p-base items-baseline">
            <a-breadcrumb class="navi">
                <a-breadcrumb-item class="text-text-inverse">Home</a-breadcrumb-item>
                <a-breadcrumb-item>挂号预约</a-breadcrumb-item>
            </a-breadcrumb>
            <div class="mt-0.5 text-text-inverse text-xl font-semibold">DepartmentSelect</div>
            <div
                class="profile flex items-center justify-between p-base bg-container rounded-2xl absolute -bottom-16 left-6 shadow-lg">
                <div class="info flex items-center">
                    <img class="w-20 rounded-lg" src="@/assets/avatar/face-1.jpg" />
                    <div class="flex flex-col justify-around ml-4">
                        <span class="text-title text-xl font-bold">{{ greeting }}，{{ accountName }} ，欢迎回来！</span>
                        <span class="text-subtext font-semibold">请选择挂号科室</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="table w-full mt-24 flex justify-evenly">
            <DepartmentTable />
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
