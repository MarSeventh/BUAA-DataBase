<template>
    <div class="home text-center flex flex-col justify-center">
        <div class="transform w-full">
            <div class="mt-20 tracking-wide slogan text-[2rem] xl:text-[5.25rem] font-extralight"
                style="color: rgb(0, 0, 0);">
                <span class="font-semibold">付款金额：{{ price }} 元</span>
            </div>
            <div class="flex justify-center">
                <a-card title="微信支付" class="mb-4 mt-4 mr-4 rounded-lg shadow-lg" :bordered="false">
                    <img src="@/assets/wechatpay.png" style="width:300px ;height:300px ;" alt="wechatpay">
                </a-card>
                <a-card title="支付宝支付" class="mb-4 mt-4 ml-4 rounded-lg shadow-lg" :bordered="false">
                    <img src="@/assets/alipay.jpg" style="width:300px ;height:300px ;" alt="wechatpay">
                </a-card>
            </div>
            <button @click="successPay"
                class="mr-2 bg-primary-300 hover:bg-primary-300 cursor-pointer mt-lg shadow border-0 outline-none text-lg px-[64px] py-lg rounded-sm">
                我已付款
            </button>
            <button @click="failPay"
                class="ml-2 bg-red-300 hover:bg-red-300 cursor-pointer mt-lg shadow border-0 outline-none text-lg px-[64px] py-lg rounded-sm">
                稍后付款
            </button>
        </div>
    </div>
</template>
  
<script lang="ts" setup>
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
import { useAccountStore } from '@/store';

  const accountStore = useAccountStore();
  accountStore.init();
const userName = accountStore.account.username;

const router = useRouter();
const route = useRoute();
const id = route.query.id;
const price = route.query.price;

async function successPay() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/finishPay/', {
            id: id,
            userName: userName,
        });
        if (response.status === 200) {
            router.go(-1);
        }
    } catch (error) {
        console.log(error);
    }
}

function failPay() {
    router.go(-1);
}

</script>

<style scoped lang="less">
.home {
    min-height: max(100vh, 600px);
    margin-top: -78px;
}
</style>
  