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
        title: '化验名称',
        dataIndex: 'name',
    },
    {
        title: '化验时间',
        dataIndex: 'time',
    },
    { title: '详情', dataIndex: 'select', width: 200 },
];

type Assay = {
    id?: number;
    name?: string;
    time?: string;
};

const assays = reactive<Assay[]>([]);



const showModal = ref(false);

async function fetchAssayList() {
    try {
        const response = await axios.get('http://127.0.0.1:4523/m1/3616438-0-default/api/getLaboratorySheetids');
        assays.length = 0; // 清空assays数组

        // 将获取到的部门数据放入assays数组中
        response.data.assayList.forEach((item) => {
            assays.push({ id: item.id, name: item.checkName, time: item.time });
        });
    } catch (error) {
        console.error('Error fetching assays:', error);
    }

}
fetchAssayList();


async function goin(record: Assay) {
    try {
        router.push({
            path: '/assayItem',
            query: {
                id: record.id,
            },
        });
    } catch (error) {
        console.error('Error fetching assays:', error);
    }
}

</script>

<template>
    <!-- 成员表格 -->
    <a-table v-bind="$attrs" :columns="columns" :dataSource="assays" :pagination="false">
        <template #title>
            <h2 class="text-title font-bold" style="text-align: center;">化验结果清单</h2>
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
