<template>
    <ThemeProvider :color="{ middle: { 'bg-base': '#fff' }, primary: { DEFAULT: '#1896ff' } }">
        <div class="signin-box rounded-sm">
            <a-form :model="form" :wrapperCol="{ span: 24 }" @finish="signin"
                class="signin-form w-[400px] p-lg xl:w-[440px] xl:p-xl h-fit text-text">
                <a-divider>注册（非社区用户）</a-divider>
                <a-form-item :required="true" name="idcard">
                    <a-input v-model:value="form.idcard" autocomplete="new-idcard" placeholder="请输入身份证号"
                        class="signin-input h-[40px]" type="idcard" />
                </a-form-item>
                <a-form-item :required="true" name="username">
                    <a-input v-model:value="form.username" autocomplete="new-username" placeholder="请输入用户名"
                        class="signin-input h-[40px]" />
                </a-form-item>
                <a-form-item :required="true" name="password">
                    <a-input v-model:value="form.password" autocomplete="new-password" placeholder="请输入登录密码"
                        class="signin-input h-[40px]" type="password" />
                </a-form-item>
                <a-button htmlType="submit" class="h-[40px] w-full" type="primary" :loading="loading"> 注册 </a-button>
                <a-button style="margin-top: 10px;" class="h-[40px] w-full" type="primary" @click="login" :loading="loading"> 已有账号？登录 </a-button>
                <a-divider></a-divider>
                <div class="terms">
                    注册即代表您同意我们的
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

export interface signinFormProps {
    username: string;
    password: string;
    idcard: string;
}
const loading = ref(false);
const router = useRouter();

const form = reactive({
    username: undefined,
    password: undefined,
    idcard: undefined,
});

const emit = defineEmits<{
    (e: 'success', fields: signinFormProps): void;
    (e: 'failure', reason: string, fields: signinFormProps): void;
}>();

  const accountStore = useAccountStore();
  accountStore.init();
function signin(params: signinFormProps) {
    loading.value = true;
    accountStore
        .signin(params.username, params.password, params.idcard)
        .then((res) => {
            emit('success', params);
        })
        .catch((e) => {
            emit('failure', e.message, params);
        })
        .finally(() => (loading.value = false));
}

function login() {
    router.push('/login');
}
</script>
  