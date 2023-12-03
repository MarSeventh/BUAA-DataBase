<script lang="ts" setup>
import axios from 'axios';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';

const router = useRouter();

const route = useRoute();

const assayItemId = route.query.id;

const columns = [
    {
        title: '编号',
        dataIndex: 'id',
    },
    {
        title: '化验项目',
        dataIndex: 'name',
    },
    {
        title: '化验结果',
        dataIndex: 'result',
    },
    {
        title: '最小参考值',
        dataIndex: 'min',
    },
    {
        title: '最大参考值',
        dataIndex: 'max',
    },
    {
        title: '化验时间',
        dataIndex: 'time',
    },
];

type AssayItem = {
    id?: number;
    name?: string;
    result?: number;
    min?: number;
    max?: number;
    time?: string;
};

const assayItems = reactive<AssayItem[]>([]);



const showModal = ref(false);

async function fetchAssayItemList() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/getLaboratorySheet', {
            id: assayItemId,
        });
        assayItems.length = 0; // 清空assayItems数组

        // 将获取到的部门数据放入assayItems数组中
        response.data.assayItemList.forEach((item) => {
            assayItems.push({ id: item.itemid, name: item.checkName, result: item.result, min: item.minresult, max: item.maxresult, time: item.outputtime });
        });
    } catch (error) {
        console.error('Error fetching assayItems:', error);
    }

}
fetchAssayItemList();



</script>

<template>
    <!-- 成员表格 -->
    <a-table v-bind="$attrs" :columns="columns" :dataSource="assayItems" :pagination="false">
        <template #title>
            <h2 class="text-title font-bold" style="text-align: center;">化验详情</h2>
        </template>
        <template #bodyCell="{ column, text, record }">
            <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
                <div class="flex-col flex justify-evenly ml-2">
                    <span class="text-title font-bold">{{ text }}</span>
                </div>
            </div>
            <template v-else-if="column.dataIndex === 'result'">
                <div class="flex items-center justify-between">
                    <span>{{ text }}</span>
                    <div>
                        <a-badge v-if="text >= record.min && text <= record.max" class="ml-1 text-subtext" :color="'green'">
                            <template #text>
                                <span class="text-subtext">正常</span>
                            </template>
                        </a-badge>
                        <a-badge v-else class="ml-1 text-subtext" :color="'red'">
                            <template #text>
                                <span class="text-subtext">异常</span>
                            </template>
                        </a-badge>
                    </div>
                </div>
            </template>
            <div v-else class="text-subtext">
                {{ text }}
            </div>
        </template>
    </a-table>
</template>
