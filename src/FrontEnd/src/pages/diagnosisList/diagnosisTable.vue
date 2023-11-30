<script lang="ts" setup>
import axios from 'axios';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();


const columns = [
    {
        title: '编号',
        dataIndex: 'id',
    },
    {
        title: '医生姓名',
        dataIndex: 'name',
    },
    {
        title: '诊断时间',
        dataIndex: 'time',
    },
    { title: '详情', dataIndex: 'select', width: 200 },
];

type Diagnosis = {
    id?: number;
    name?: string;
    time?: string;
};

const diagnosiss = reactive<Diagnosis[]>([]);



const showModal = ref(false);

async function fetchDiagnosisList() {
    try {
        const response = await axios.get('http://127.0.0.1:4523/m1/3616438-0-default/api/getDiagnosisList');
        diagnosiss.length = 0; // 清空diagnosiss数组

        // 将获取到的部门数据放入diagnosiss数组中
        response.data.diagnosisList.forEach((item) => {
            diagnosiss.push({ id: item.id, name: item.doctor, time: item.time });
        });
    } catch (error) {
        console.error('Error fetching diagnosiss:', error);
    }

}
fetchDiagnosisList();


async function goin(record: Diagnosis) {
    try {
        router.push({
            path: '/diagnosisItem',
            query: {
                id: record.id,
            },
        });
    } catch (error) {
        console.error('Error fetching diagnosiss:', error);
    }
}

</script>

<template>
    <!-- 成员表格 -->
    <a-table v-bind="$attrs" :columns="columns" :dataSource="diagnosiss" :pagination="false">
        <template #title>
            <h2 class="text-title font-bold" style="text-align: center;">诊断结果清单</h2>
        </template>
        <template #bodyCell="{ column, text, record }">
            <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
                <div class="flex-col flex justify-evenly ml-2">
                    <span class="text-title font-bold">{{ text }}</span>
                </div>
            </div>
            <template v-else-if="column.dataIndex === 'select'">
                <a-button :disabled="showModal" type="primary" @click="goin(record)">
                    查看详情
                </a-button>
            </template>
            <div v-else class="text-subtext">
                {{ text }}
            </div>
        </template>
    </a-table>
</template>
