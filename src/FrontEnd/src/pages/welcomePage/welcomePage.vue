<script lang="ts" setup>
import { useRouter } from 'vue-router';
import medicalNavigation from './medicalNavigation.vue';
const router = useRouter();
</script>
<template>
    <div class="front-view">
        <img style="margin-top: 10px;margin-left: 10px;" src="@/assets/buaalogo.svg" width="60" height="60" />
        <div class="container">
            <div class="home">
                <div class="transform w-full">
                    <div class="tracking-wide slogan text-[2rem] xl:text-[2.75rem] font-extralight"
                        style="color: rgb(0, 0, 0);">
                        <span class="font-semibold">欢迎进入智慧医航！</span>
                    </div>
                    <div class="tracking-wide slogan text-[1.5rem] xl:text-[1.75rem] font-extralight"
                        style="color: rgb(0, 0, 0);">
                        <span class="font-semibold">Welcome to Smart BUAA Hospital!</span>
                    </div>
                </div>
            </div>
            <div class="navigation">
                <medicalNavigation />
            </div>
        </div>
    </div>
</template>
<style scoped lang="less">
.home {
    display: flex;
    width: 100%;
    height: 100%;
    margin-top: 90px;
}

.container {
    display: flex;
    /* 水平居中 */
    justify-content: center;
    text-align: center;
    /* 内容水平居中 */
}

.front-view {

    background-image: url('@/assets/buaa.jpg');
    background-size: cover;
    /* 根据容器大小调整图片尺寸 */
    background-position: center;
    /* 设置图片位置为容器中心 */
}

.navigation {
    display: flex;
    padding: 5%;
    margin-top: -100px;
}
</style>
