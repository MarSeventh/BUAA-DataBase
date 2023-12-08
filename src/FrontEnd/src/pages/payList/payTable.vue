<script lang="ts" setup>
import { reactive, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAccountStore } from '@/store';

const router = useRouter();
const username = useAccountStore().account?.username;
const columns = [
    {
        title: '序号',
        dataIndex: 'id',
    },
    { title: '费用类型', dataIndex: 'type' },
    { title: '缴费状态', dataIndex: 'status' },
    { title: '缴费金额', dataIndex: 'price' },
];

type PayItem = {
    id?: number;
    type?: string;
    status?: number;
    price?: number;
};

const payItems = reactive<PayItem[]>([]);

async function fetchPayList() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/fetchPayList', {
            params: {
                username: username,
            },
        });
        payItems.length = 0;
        response.data.Info.forEach(item => {
            payItems.push({ id: item.id, type: item.type, status: item.status, price: item.price });
        });
    } catch (error) {
        console.error('Error fetching payItems:', error);
    }
}

fetchPayList();

type Status = 0 | 1;

const StatusDict = {
    0: '未缴费',
    1: '已缴费',
};
function getPriceSum() {
    var priceSum = 0;
    for (var i = 0; i < payItems.length; i++) {
        if (payItems[i].status == 0) {
            priceSum += payItems[i].price;
        }
    }
    return priceSum;
}
async function goin() {
    try {
        router.push({
            path: '/payPage',
            query: {
                price: getPriceSum(),
                id: -1, //-1代表该用户的所有费用
            },
        });
    } catch (error) {
        console.error('Error fetching doctors:', error);
    }
}

</script>
<template>
    <!-- 成员表格 -->
    <a-table v-bind="$attrs" :columns="columns" :dataSource="payItems" :pagination="false">
        <template #title>
            <h2 class="text-title font-bold" style="text-align: center;">费用清单</h2>
        </template>
        <template #bodyCell="{ column, text, record }">
            <div class="flex items-stretch" v-if="column.dataIndex === 'id'">
                <div class="flex-col flex justify-evenly ml-2">
                    <span class="text-title font-bold">{{ text }}</span>
                </div>
            </div>
            <template v-else-if="column.dataIndex === 'status'">
                <a-badge v-if="text === 1" class="text-subtext" :color="'green'">
                    <template #text>
                        <span class="text-subtext">{{ StatusDict[text as Status] }}</span>
                    </template>
                </a-badge>
                <a-badge v-else-if="text === 0" class="text-subtext" :color="'red'">
                    <template #text>
                        <span class="text-subtext">{{ StatusDict[text as Status] }}</span>
                    </template>
                </a-badge>
            </template>
            <div class="flex items-stretch" v-else-if="column.dataIndex === 'price'">
                <div class="flex-col flex justify-evenly ml-2">
                    <span class="text-title font-bold">￥{{ text }}</span>
                </div>
            </div>
            <div v-else class="text-subtext">
                {{ text }}
            </div>
        </template>
    </a-table>
    <div class="mt-4 flex justify-center">
        <a-button class="text-center justify-center" type="primary" @click="goin">
            立即缴费（￥{{ getPriceSum() }}）
        </a-button>
    </div>
</template>
