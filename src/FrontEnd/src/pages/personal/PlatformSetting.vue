<script lang="ts" setup>
import { useAccountStore } from '@/store/account';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';

const router = useRouter();
const { logout } = useAccountStore();
const accountStore = useAccountStore();
const role = accountStore.role;
const username = accountStore.account?.username;

function checkInput(input: string) {
  if (input === '我是' + username + '，我确定要注销账号') {
    return true;
  } else {
    return false;
  }
};

var input = ref<string>('');

function handleLogout() {
  logout().then(() => router.push('/login'));
}

const open = ref<boolean>(false);

const showModal = () => {
  open.value = true;
};
async function deleteAccount() {
  try {
    const response = await axios.post('http://127.0.0.1:4523/m1/3616438-0-default/api/deleteAccount');
    if (response.status == 200) {
      logout().then(() => router.push('/login'));
    } else {
      console.log(response.data);
    }
  } catch (error) {
    console.log(error);
  }
}
const handleOk = (e: MouseEvent) => {
  console.log(e);
  if (checkInput(input.value)) {
    deleteAccount();
    open.value = false;
  } else {
    const fail = document.getElementById('fail');
    fail?.classList.remove('hidden');
  }
};

</script>
<template>
  <a-modal v-model:visible="open" title="注销账号" @ok="handleOk">
    <p>注销账号后，您的账号将无法再次登录，可能造成数据丢失。</p>
    <p>请确认您已经清楚了解该操作的后果。</p>
    <p style="color: red;">若您仍要注销，请输入“我是{{ username }}，我确定要注销账号”</p>
    <a-input v-model:value="input" />
    <div id="fail" class="hidden" style="color: red;margin-bottom: 3px;">输入错误，请重新输入！</div>
  </a-modal>
  <a-card :bordered="false" title="账号设置" class="shadow-lg platform-setting rounded-xl">
    <a-divider />
    <div>
      <span style="font-weight: bold; font-size: 1.2em;">退出登录： </span>
      <a-button type="primary" @click="handleLogout">确认</a-button>
    </div>
    <a-divider />
    <div>
      <span style="font-weight: bold; font-size: 1.2em;color: red;">注销账号： </span>
      <a-button type="primary" class="hover:bg-red-400" @click="showModal">确认</a-button>
    </div>
  </a-card>
</template>
<style lang="less" scoped>
.platform-setting {
  :deep(.ant-card-head) {
    @apply border-none;

    .ant-card-head-title {
      @apply font-semibold;
    }
  }

  :deep(.ant-card-body) {
    @apply pt-2;
  }

  .group {
    &:not(:first-child) {
      @apply mt-6;
    }

    &-list {
      &-item {
        &:not(:first-child) {
          @apply mt-6;
        }
      }
    }
  }
}
</style>
