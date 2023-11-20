<script lang="ts" setup>
import { LogoutOutlined } from '@ant-design/icons-vue';
import { ThemeProvider, alert } from 'stepin';

</script>
<template>
  <ThemeProvider :color="{ middle: { 'bg-base': '#003f8c' }, primary: { DEFAULT: '#1896ff' } }" :autoAdapt="false">
    <div class="front-view flex flex-col">
      <div class="text-text flex-1">
        <div class="front-header flex items-baseline py-md px-xl">
          <router-link to="/home" class="text-xxl text-text hover:text-text">
            <img src="@/assets/buaalogo.svg" width="48" height="48" />
            BUAA HOSPITAL
          </router-link>
        </div>
        <div class="front-content px-xl">
          <router-view />
        </div>
      </div>
    </div>
  </ThemeProvider>
</template>
<style lang="less" scoped>
.front-view {
  background-image: url('@/assets/background.jpg');
  /* 设置背景图片的路径 */
  background-size: cover;
  /* 调整背景图片的大小，以填充整个容器 */
  background-position: center;
  /* 将背景图片居中显示 */
  background-repeat: no-repeat;

  /* 防止背景图片重复显示 */
  .front-header {
    .front-nav-item {
      &.with-list .front-nav-item-content {
        &:after {
          content: '';
          @apply ~"h-[8px]"~"w-[8px]" transition-transform ml-2 inline-block border-text border-l-0 border-t-0 border-r-2 border-b-2 border-solid~"rotate-[-135deg]" translate-y-1/4;
        }

        &:hover {
          &:after {
            @apply ~"rotate-[45deg]" translate-y-0;
          }
        }
      }
    }
  }

  .front-content {
    min-height: calc(100vh - 78px);
  }
}</style>
