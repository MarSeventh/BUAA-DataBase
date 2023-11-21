<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { useAccountStore } from '@/store/account';

const accountStore = useAccountStore();
const username = ref(accountStore.account?.username);
const role = ref(accountStore.role);


</script>
<template>
  <a-card title="账号信息" class="profile-info rounded-xl shadow-lg" :bordered="false">
    <div class="description">
      若要修改您的个人信息，请联系管理员。
    </div>
    <a-divider />
    <div class="text-title font-medium">个人信息</div>
    <a-descriptions class="profile-list mt-3 font-medium" :column="1">
      <a-descriptions-item label="用户名">
        {{ username }}
      </a-descriptions-item>
      <a-descriptions-item label="角色">
        {{ role }}
      </a-descriptions-item>
    </a-descriptions>
  </a-card>
</template>
<style lang="less" scoped>
.profile-info {
  :deep(.ant-card) {
    &-head {
      @apply border-none;

      &-title {
        @apply font-semibold;
      }
    }

    &-body {
      @apply pt-1;
    }
  }

  :deep(.ant-descriptions) {
    &-row:last-child>td {
      padding-bottom: 0;
    }

    &-item {
      &-content {
        @apply items-center;

        .anticon {
          @apply text-base;

          &:not(:first-child) {
            @apply ml-2;
          }
        }
      }
    }
  }
}
</style>
