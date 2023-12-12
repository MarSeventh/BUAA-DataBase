<script lang="ts" setup>
  import { FormInstance } from 'ant-design-vue';
  import { reactive, ref } from 'vue';
  import { DeleteOutlined, EditFilled } from '@ant-design/icons-vue';
  import axios from 'axios';
  import { useAccountStore } from '@/store';

  const accountStore = useAccountStore();
  accountStore.init();
  const username = accountStore.account?.username;

  const columns = [
    { title: '诊断结果', dataIndex: 'department' },
    { title: '操作', dataIndex: 'edit', width: 50 },
  ];

  const columnPatient = [
    { title: '病人信息', dataIndex: 'name', },
    { title: '操作', dataIndex: 'edit', width: 50 },
  ];

  type Patient = {
    name?: string;
    id?: string;
  }

  type Diagnosis = {
    department?: string;
    status?: number;
    _edit?: boolean;
    _isNew?: boolean;
  };

  const DiagnosisList = reactive<Diagnosis[]>([
    {
      department: '',
    }
  ]);

  const patient = reactive<Patient[]>([
    {
      name: '', 
      id: '',
    }
  ]);

  const showModal = ref(false);
  const showModal3 = ref(false);

  const newDiagnosis = (Diagnosis?: Diagnosis) => {
    if (!Diagnosis) {
      Diagnosis = { _isNew: true };
    }
    Diagnosis.department = undefined;
    Diagnosis.status = 0;
    return Diagnosis;
  };
  const newPatient = (Patient?: Patient) => {
    if (!Patient) {
      Patient = {};
    }
    Patient.name = undefined;
    Patient.id = undefined;
    return Patient;
  };

  const copyObject = (target: any, source?: any) => {
    if (!source) {
      return target;
    }
    Object.keys(target).forEach((key) => (target[key] = source[key]));
  };

  const form = reactive<Diagnosis>(newDiagnosis());
  const form3 = reactive<Patient>(newPatient());

  function reset() {
    return newDiagnosis(form);
  }
  function reset3() {
    return newPatient(form3);
  }

  function cancel() {
    showModal.value = false;
    reset();
  }
  function cancel3() {
    showModal3.value = false;
    reset3();
  }

  const formModel = ref<FormInstance>();

  const formLoading = ref(false);

  function submit() {
    formLoading.value = true;
    formModel.value
      ?.validateFields()
      .then((res: Diagnosis) => {
        if (form._isNew) {
          DiagnosisList.push({ ...res });
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

  function submit3() {
    formLoading.value = true;
    formModel.value
      ?.validateFields()
      .then((res: Patient) => {
        res.name = res?.name;
        res.id = res?.id;
        copyObject(editRecord3.value, res);
        showModal3.value = false;
        reset3();
      })
      .catch((e) => {
        console.error(e);
      })
      .finally(() => {
        formLoading.value = false;
      });
  }

  function delLine(){
    DiagnosisList.length = DiagnosisList.length - 1;
  }

  const DiagnosisName = reactive<string[]>([]);
  function copyArray(){
    DiagnosisList.forEach((item) => {
      DiagnosisName.push(item.department);
    })
  }
  function clearArray(){
    DiagnosisName.length = 0;
  }

  async function sendCheckResult() {
    try {
        copyArray();
        const response = await axios.post('http://127.0.0.1:8000/api/sendCheckResult/', {
          username: username,
          Pid: patient[0].id,
          Diagnosis: DiagnosisList[0].department,
        });
        clearArray();
    } catch (error) {
        console.error('Error sending Diagnosis:', error);
    }
  }

  const editRecord = ref<Diagnosis>();
  const editRecord3= ref<Patient>();

  /**
   * 编辑
   * @param record
   */
  function edit(record: Diagnosis) {
    editRecord.value = record;
    copyObject(form, record);
    showModal.value = true;
  }
  function edit3(record: Patient) {
    editRecord3.value = record;
    copyObject(form3, record);
    showModal3.value = true;
  }

  type Status = 0 | 1;

  const StatusDict = {
    0: 'offline',
    1: 'online',
  };
</script>
<template>

  <!-- 病人信息 -->
  <a-modal :title="'编辑'" v-model:visible="showModal3" @ok="submit3" @cancel="cancel3">
    <a-form ref="formModel" :model="form3" :labelCol="{ span: 5 }" :wrapperCol="{ span: 16 }">
      <a-form-item required label="姓名" name="name">
        <a-input v-model:value="form3.name" />
      </a-form-item>
      <a-form-item required label="ID" name="id">
        <a-input v-model:value="form3.id" />
      </a-form-item>
    </a-form>
  </a-modal>

  <a-table v-bind="$attrs" :columns="columnPatient" :dataSource="patient" :pagination="false">
    <template #bodyCell="{ column, text, record }">
      <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
        <div class="flex-col flex justify-evenly ml-2">
          <span class="text-title font-bold">{{ text }}</span>
          <span class="text-xs text-subtext">{{ record.id }}</span>
        </div>
      </div>
      <template v-else-if="column.dataIndex === 'edit'">
        <a-button :disabled="showModal3" type="link" @click="edit3(record)">
          <template #icon>
            <EditFilled />
          </template>
          编辑
        </a-button>
      </template>
      <div v-else class="text-subtext">
        {{ text }}
      </div>
    </template>
  </a-table>  

  <a-modal :title="form._isNew ? '新增诊断结果' : '编辑诊断结果'" v-model:visible="showModal" @ok="submit" @cancel="cancel">
    <a-form ref="formModel" :model="form" :labelCol="{ span: 5 }" :wrapperCol="{ span: 16 }">
      <a-form-item label="诊断结果" required name="department">
        <a-input v-model:value="form.department" />
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="DiagnosisList" :pagination="false">
    <template #title>
      <div class="flex justify-between pr-4">
        <a-button type="primary" @click="sendCheckResult" :loading="formLoading">
          上传诊断结果
        </a-button>
      </div>
    </template>
    <template #bodyCell="{ column, text, record }">
      <template v-if="column.dataIndex === 'edit'">
        <a-button :disabled="showModal" type="link" @click="edit(record)">
          <template #icon>
            <EditFilled />
          </template>
          编辑
        </a-button>
      </template>
      <div v-else class="text-subtext">
        {{ text }}
      </div>
    </template>
  </a-table>
</template>
