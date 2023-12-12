<script lang="ts" setup>
  import { FormInstance } from 'ant-design-vue';
  import { reactive, ref } from 'vue';
  import dayjs from 'dayjs';
  import { Dayjs } from 'dayjs';
  import { DeleteOutlined, EditFilled } from '@ant-design/icons-vue';
  import { del } from 'vue-demi';
  import axios from 'axios';

  const columns = [
    { title: '诊断结果', dataIndex: 'jobs' },
    { title: '医生姓名', dataIndex: 'department', width: 300 },
    { title: '日期', dataIndex: 'time', width: 300 },
    { title: '操作', dataIndex: 'edit', width: 50 },
  ];

  const columnPatient = [
    {
      title: '病人信息',
      dataIndex: 'name',
    },
  ];

  type Check = {
    department?: string;
    jobs?: string;
    status?: number;
    time?: Dayjs;
    _edit?: boolean;
    _isNew?: boolean;
  };

  type Patient = {
    name?: string;
    id?: string;
  }

  const patient = reactive<Patient>(
    {
      name: '我',
      id: '12345',
    },
  );

  const checkResults = reactive<Check[]>([
    {
      jobs: 'mengtuo',
      department: 'Technical',
      status: 1,
      time: dayjs(),
    },
  ]);

  const newRecord = ref<Check>();

  function addNew(record: Check) {
    newRecord.value = record;
    copyObject(form, record);
    showModal.value = true;
    form._isNew = true;
  }

  const showModal = ref(false);

  const newCheck = (Check?: Check) => {
    if (!Check) {
      Check = { _isNew: true };
    }
    Check.department = undefined;
    Check.jobs = undefined;
    Check.status = 0;
    Check.time = dayjs();
    return Check;
  };

  const copyObject = (target: any, source?: any) => {
    if (!source) {
      return target;
    }
    Object.keys(target).forEach((key) => (target[key] = source[key]));
  };

  const form = reactive<Check>(newCheck());

  function reset() {
    return newCheck(form);
  }

  function cancel() {
    showModal.value = false;
    reset();
  }

  const formModel = ref<FormInstance>();

  const formLoading = ref(false);

  function submit() {
    formLoading.value = true;
    formModel.value
      ?.validateFields()
      .then((res: Check) => {
        res.department = res?.department;
        res.jobs = res?.jobs;
        if (form._isNew) {
          checkResults.push({ ...res });
        } else {
          copyObject(editRecord.value, res);
        }
        showModal.value = false;
        reset();
      })
      .catch((e) => {
        console.error(e);
      })
      .finally(() => {
        formLoading.value = false;
      });
  }

  async function fetchPatient() {
    try {
        const response = await axios.get('http://127.0.0.1:4523/m1/3616438-0-default/api/getPatient/');

        response.data.patientsList.forEach((item) => {
          patient.name = item.name;
          patient.id = item.id;
        });
    } catch (error) {
        console.error('Error fetching patient:', error);
    }
  }
  fetchPatient();

  async function sendCheckResults() {
    try {
        const response = await axios.post('http://127.0.0.1:4523/m1/3616438-0-default/api/sendCheckResults/');

        response.data.checkResults.forEach((item) => {
            
            item.push({  jobs: item.id, department: item.doctor, time: item.time })
        });
    } catch (error) {
        console.error('Error sending check results:', error);
    }
  }

  const editRecord = ref<Check>();

  /**
   * 编辑
   * @param record
   */
  function edit(record: Check) {
    editRecord.value = record;
    copyObject(form, record);
    showModal.value = true;
  }

  type Status = 0 | 1;

  const StatusDict = {
    0: 'offline',
    1: 'online',
  };
</script>
<template>
  <a-modal :title="form._isNew ? '新增检查结果' : '编辑检查结果'" v-model:visible="showModal" @ok="submit" @cancel="cancel">
    <a-form ref="formModel" :model="form" :labelCol="{ span: 5 }" :wrapperCol="{ span: 16 }">
      <a-form-item required label="诊断结果" name="jobs">
        <a-input v-model:value="form.jobs" />
      </a-form-item>
      <a-form-item required label="医生姓名" name="department">
        <a-input v-model:value="form.department" />
      </a-form-item>
      <a-form-item label="日期" name="time">
        <a-date-picker v-model:value="form.time" />
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="checkResults" :pagination="false">
    <template #title>
      <div class="flex justify-between pr-4">
        <h3>检查结果清单</h3>
        <a-button type="primary" @click="sendCheckResults()" :loading="formLoading">
          上传检查结果
        </a-button>
      </div>
    </template>
    <template #bodyCell="{ column, text, record }">
      <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
        <div class="flex-col flex justify-evenly ml-1">
          <span class="text-title font-bold">{{ text }}</span>
          <span class="text-xs text-subtext">{{ record.email }}</span>
        </div>
      </div>
      <template v-else-if="column.dataIndex === 'status'">
        <a-badge class="text-subtext" :color="'green'">
          <template #text>
            <span class="text-subtext">{{ StatusDict[text as Status] }}</span>
          </template>
        </a-badge>
      </template>
      <template v-else-if="column.dataIndex === 'time'">
        {{ text?.format('YYYY-MM-DD') }}
      </template>
      <template v-else-if="column.dataIndex === 'edit'">
        <a-button :disabled="showModal" type="link" @click="edit(record)">
          <template #icon>
            <EditFilled />
          </template>
          编辑
        </a-button>
        <a-button :disabled="showModal" type="link" @click="del">
          <template #icon>
            <DeleteOutlined />
          </template>
          删除
        </a-button>
      </template>
      <div v-else class="text-subtext">
        {{ text }}
      </div>
    </template>
  </a-table>
</template>
