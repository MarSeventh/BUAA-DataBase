<script lang="ts" setup>
import axios from 'axios';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';


const router = useRouter();

const columns = [
    {
        title: '科室名',
        dataIndex: 'name',
    },
    { title: '挂号', dataIndex: 'goin', width: 200 },
];

type Department = {
    name?: string;
    _edit?: boolean;
    _isNew?: boolean;
};

const departments = reactive<Department[]>([]);



const showModal = ref(false);

async function fetchDepartmentList() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/departmentList'); 
        departments.length = 0; // 清空departments数组

        // 将获取到的部门数据放入departments数组中
        response.data.name.forEach((nameitem) => {
          departments.push({ name: nameitem });
        });
      } catch (error) {
        console.error('Error fetching departments:', error);
      }

}
fetchDepartmentList();

function goin(record: Department) {
    router.push({
        path: '/doctorSelect',
        query: {
            name: record.name,
        },
    });
}

</script>

<template>

    <!-- 成员表格 -->
    <a-table v-bind="$attrs" :columns="columns" :dataSource="departments" :pagination="false">
        <template #title>
            <h2 class="text-title font-bold" style="text-align: center;">科室列表</h2>
        </template>
        <template #bodyCell="{ column, text, record }">
            <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
                <div class="flex-col flex justify-evenly ml-2">
                    <span class="text-title font-bold">{{ text }}</span>
                </div>
            </div>
            <template v-else-if="column.dataIndex === 'goin'">
                <a-button :disabled="showModal" type="primary" @click="goin(record)">
                    挂号
                </a-button>
            </template>
            <div v-else class="text-subtext">
                {{ text }}
            </div>
        </template>
    </a-table>
</template>
