<script lang="ts" setup>
import axios from 'axios';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import { useAccountStore } from '@/store';

const accountStore = useAccountStore();
const router = useRouter();

const route = useRoute();
const departmentName = route.query.name;

const columns = [
    {
        title: '医生姓名',
        dataIndex: 'name',
    },
    {
        title: '诊室编号',
        dataIndex: 'roomid',
    },
    {
        title: '排队人数',
        dataIndex: 'quenelen',
    },
    { title: '确认挂号', dataIndex: 'select', width: 200 },
];

type Doctor = {
    name?: string;
    roomid?: string;
    quenelen?: string;
    _edit?: boolean;
    _isNew?: boolean;
};

const doctors = reactive<Doctor[]>([]);



const showModal = ref(false);

async function fetchDoctorList() {
    try {
        const response = await axios.post('http://127.0.0.1:4523/m1/3616438-0-default/api/doctorList', {
            department: departmentName,
        });
        doctors.length = 0; // 清空doctors数组

        // 将获取到的部门数据放入doctors数组中
        response.data.doctorList.forEach((item) => {
            doctors.push({ name: item.name, roomid: item.roomid, quenelen: item.quenelen });
        });
    } catch (error) {
        console.error('Error fetching doctors:', error);
    }

}
fetchDoctorList();

const price = accountStore.role === 'communityPatient' ? 1 : 10;

/*async function addPay() {
    try {
        const response = await axios.post('http://127.0.0.1:4523/m1/3616438-0-default/api/addPay', {
            name: '挂号费',
            number: price,
        });

        return response.data.id;
    } catch (error) {
        console.error('Error fetching doctors:', error);
    }
}*/

async function confirmDoctor(name: String) {
    try {
        const response = await axios.post('http://127.0.0.1:4523/m1/3616438-0-default//api/confirmDoctor', {
            name: name,
        });
        return response.data.id;
    } catch (error) {
        console.error('Error fetching doctors:', error);
    }
}
async function goin(record: Doctor) {
    try {
        const id = await confirmDoctor(record.name);
        router.push({
            path: '/payPage',
            query: {
                price: price,
                id: id,
            },
        });
    } catch (error) {
        console.error('Error fetching doctors:', error);
    }
}

</script>

<template>
    <!-- 成员表格 -->
    <a-table v-bind="$attrs" :columns="columns" :dataSource="doctors" :pagination="false">
        <template #title>
            <h2 class="text-title font-bold" style="text-align: center;">{{ departmentName }}医生列表</h2>
        </template>
        <template #bodyCell="{ column, text, record }">
            <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
                <div class="flex-col flex justify-evenly ml-2">
                    <span class="text-title font-bold">{{ text }}</span>
                </div>
            </div>
            <template v-else-if="column.dataIndex === 'quenelen'">
                <div class="flex-col flex justify-evenly ml-2">
                    <span>{{ text }}人</span>
                </div>
                <a-progress v-if="record.quenelen >= 50" :strokeWidth="4" :percent="record.quenelen * 2" status="exception" />
                <a-progress v-else :strokeWidth="4" :percent="record.quenelen * 2" status="normal" />
            </template>
            <template v-else-if="column.dataIndex === 'roomid'">
                <div class="flex-col flex justify-evenly ml-2">
                    <span>{{ text }}</span>
                </div>
            </template>
            <template v-else-if="column.dataIndex === 'select'">
                <a-button :disabled="showModal" type="primary" @click="goin(record)">
                    确认预约
                </a-button>
            </template>
            <div v-else class="text-subtext">
                {{ text }}
            </div>
        </template>
    </a-table>
</template>
