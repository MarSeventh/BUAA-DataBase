<template>
  <ThemeProvider :color="{ middle: { 'bg-base': '#fff' }, primary: { DEFAULT: '#1896ff' } }">
    <div class="login-box rounded-sm">
      <a-form :model="form" :wrapperCol="{ span: 24 }" @finish="login"
        class="login-form w-[400px] p-lg xl:w-[440px] xl:p-xl h-fit text-text">
        <a-divider>登录</a-divider>
        <a-form-item :required="true" name="username">
          <a-input v-model:value="form.username" autocomplete="new-username" placeholder="请输入用户名或邮箱: admin"
            class="login-input h-[40px]" />
        </a-form-item>
        <a-form-item :required="true" name="password">
          <a-input v-model:value="form.password" autocomplete="new-password" placeholder="请输入登录密码: 888888"
            class="login-input h-[40px]" type="password" />
        </a-form-item>
        <div id="fail" class="hidden" style="color: red;margin-bottom: 3px;">用户名或密码错误</div>
        <a-button htmlType="submit" class="h-[40px] w-full" type="primary" :loading="loading"> 登录 </a-button>
        <a-button style="margin-top: 10px;" class="h-[40px] w-full" type="primary" @click="Signin" :loading="loading"> 没有账号？注册 </a-button>
        <a-divider></a-divider>
        <div class="terms">
          登录即代表您同意我们的
          <span class="font-bold">用户条款 </span>、<span class="font-bold"> 数据使用协议 </span>、以及
          <span class="font-bold">Cookie使用协议</span>。
        </div>
      </a-form>
    </div>
  </ThemeProvider>
</template>
<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { useAccountStore } from '@/store';
import { ThemeProvider } from 'stepin';
import { useRouter } from 'vue-router';

export interface LoginFormProps {
  username: string;
  password: string;
}
const loading = ref(false);

const form = reactive({
  username: undefined,
  password: undefined,
});

const emit = defineEmits<{
  (e: 'success', fields: LoginFormProps): void;
  (e: 'failure', reason: string, fields: LoginFormProps): void;
}>();

const accountStore = useAccountStore();
function login(params: LoginFormProps) {
  loading.value = true;
  accountStore
    .login(params.username, params.password)
    .then((res) => {
      emit('success', params);
    })
    .catch((e) => {
      document.getElementById("fail").classList.remove("hidden");
      emit('failure', e.message, params);
    })
    .finally(() => (loading.value = false));
}

const router = useRouter();

function Signin() {
  router.push('/signin');
}
</script>
