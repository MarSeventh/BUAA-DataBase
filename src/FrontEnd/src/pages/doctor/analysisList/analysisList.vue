<script lang="ts" setup>
import { FormInstance, message } from 'ant-design-vue';
import { reactive, ref } from 'vue';
import { DeleteOutlined, EditFilled } from '@ant-design/icons-vue';
import axios from 'axios';
import { useAccountStore } from '@/store';

const accountStore = useAccountStore();
accountStore.init();
const username = accountStore.account?.username;

const columns = [
  { title: '检查项目', dataIndex: 'department' },
  { title: '操作', dataIndex: 'edit', width: 50 },
];

const columnPatient = [
  { title: '病人信息', dataIndex: 'name', },
  { title: '操作', dataIndex: 'edit', width: 50 },
];

type AnalysisName = {
  label?: string,
  value?: string,
};

type Patient = {
  name?: string;
  id?: string;
}

const analysisProject = reactive<AnalysisName[]>([])

type Analysis = {
  department?: string;
  status?: number;
  _edit?: boolean;
  _isNew?: boolean;
};

const analysisList = reactive<Analysis[]>([]);

const patient = reactive<Patient[]>([
  {
    name: '',
    id: '',
  }
]);

function addNew() {
  showModal.value = true;
  form._isNew = true;
}

const showModal = ref(false);
const showModal3 = ref(false);

const newAnalysis = (Analysis?: Analysis) => {
  if (!Analysis) {
    Analysis = { _isNew: true };
  }
  Analysis.department = undefined;
  Analysis.status = 0;
  return Analysis;
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

const form = reactive<Analysis>(newAnalysis());
const form3 = reactive<Patient>(newPatient());

function reset() {
  return newAnalysis(form);
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
    .then((res: Analysis) => {
      if (form._isNew) {
        analysisList.push({ ...res });
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

function delLine() {
  analysisList.length = analysisList.length - 1;
}

const analysisName = reactive<string[]>([]);
function copyArray() {
  analysisList.forEach((item) => {
    analysisName.push(item.department);
  })
}
function clearArray() {
  analysisName.length = 0;
}

async function fetchAnalysisName() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/getAnalysisName/');
    analysisProject.length = 0;
    response.data.info.forEach((item) => {
      analysisProject.push({ label: item.checkName, value: item.checkName })
    });
  } catch (error) {
    console.error('Error fetching analysis name:', error);
  }
}
fetchAnalysisName();

const uploadSuccess = ref(false);
function closeUploadSuccess() {
  uploadSuccess.value = false;
}
async function sendAnalysisList() {
  formLoading.value = true;
  try {
    copyArray();
    const response = await axios.post('http://127.0.0.1:8000/api/sendAnalysisList/', {
      username: username,
      Pid: patient[0].id,
      AnalysisList: analysisName,
    });
    async (response) => {
      console.log(response.status);
      if (response.status === 200) {
        uploadSuccess.value = true;
      }
    }
    message.success('上传成功');
    clearArray();
  } catch (error) {
    message.error('上传失败');
    console.error('Error sending analysis:', error);
  } finally {
    formLoading.value = false;
  }
}

const editRecord = ref<Analysis>();
const editRecord3 = ref<Patient>();

/**
 * 编辑
 * @param record
 */
function edit(record: Analysis) {
  editRecord.value = record;
  copyObject(form, record);
  showModal.value = true;
}
function edit3(record: Patient) {
  editRecord3.value = record;
  copyObject(form3, record);
  showModal3.value = true;
}

function onChange(value: any) {
  form.department = value[0];
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

  <a-modal :title="form._isNew ? '新增检查项目' : '编辑检查项目'" v-model:visible="showModal" @ok="submit" @cancel="cancel">
    <a-form ref="formModel" :model="form" :labelCol="{ span: 5 }" :wrapperCol="{ span: 16 }">
      <a-form-item required label="检查项目" name="department">
        <a-cascader :options="analysisProject" @change="onChange" />
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="analysisList" :pagination="false">
    <template #title>
      <div class="flex justify-between pr-4">
        <a-button type="primary" @click="sendAnalysisList" :loading="formLoading">
          上传检查项目
        </a-button>
        <a-button type="primary" @click="addNew" :loading="formLoading">
          <template #icon>
            <PlusOutlined />
          </template>
          新增检查项目
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
        <a-button :disabled="showModal" type="link" @click="delLine">
          <template #icon>
            <DeleteOutlined />
          </template>
          删除
        </a-button>
      </template>
      <div v-else class="text">
        {{ text }}
      </div>
    </template>
  </a-table>

  <a-modal :title="'上传成功'" v-model:visible="uploadSuccess" @cancel="closeUploadSuccess">
  </a-modal>
</template>
