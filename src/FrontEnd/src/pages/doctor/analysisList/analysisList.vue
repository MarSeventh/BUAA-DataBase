<script lang="ts" setup>
  import { getBase64 } from '@/utils/file';
  import { FormInstance } from 'ant-design-vue';
  import { reactive, ref } from 'vue';
  import dayjs from 'dayjs';
  import { Dayjs } from 'dayjs';
  import { DeleteOutlined, EditFilled } from '@ant-design/icons-vue';
  import axios from 'axios';

  const accountStore = useAccountStore();
  accountStore.init();
  const username = accountStore.account?.username;

  const columns = [
    { title: '检查项目', dataIndex: 'department' },
    { title: '日期', dataIndex: 'time' },
    { title: '操作', dataIndex: 'edit', width: 50 },
  ];

  const columnPatient = [
    {
      title: '病人信息',
      dataIndex: 'name',
    },
  ];

  type AnalysisName = {
    label?: string,
    value?: string,
  };

  const analysisProject = reactive<AnalysisName[]>([
    {
      label: '血常规',
      value: '血常规',
    },
    {
      label: '尿常规',
      value: '尿常规',
    },
  ])

  type Analysis = {
    department?: string;
    status?: number;
    time?: Dayjs;
    _edit?: boolean;
    _isNew?: boolean;
  };

  const analysisList = reactive<Analysis[]>([
    {
      department: 'Technical',
      status: 1,
      time: dayjs(),
    },
  ]);

  function addNew() {
    showModal.value = true;
    form._isNew = true;
  }

  const showModal = ref(false);

  const newAnalysis = (Analysis?: Analysis) => {
    if (!Analysis) {
      Analysis = { _isNew: true };
    }
    Analysis.department = undefined;
    Analysis.status = 0;
    Analysis.time = dayjs();
    return Analysis;
  };

  const copyObject = (target: any, source?: any) => {
    if (!source) {
      return target;
    }
    Object.keys(target).forEach((key) => (target[key] = source[key]));
  };

  const form = reactive<Analysis>(newAnalysis());

  function reset() {
    return newAnalysis(form);
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
      .then((res: Analysis) => {
        res.department = res?.department;
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

  function delLine(){
    analysisList.length = analysisList.length - 1;
  }

  async function fetchAnalysisName() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/getAnalysisName/', {
          username
          //TODO: username貌似不需要？
        });
        analysisProject.length = 0;

        response.data.AnalysisName.forEach((item) => {
          analysisProject.push({ label: item, value: item })
        });
    } catch (error) {
        console.error('Error fetching analysis name:', error);
    }
  }
  fetchAnalysisName();

  async function sendAnalysisList() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/sendAnalysisList/', {
          analysisList: analysisList
          //TODO: 需要加上病人信息和医生信息
        });
    } catch (error) {
        console.error('Error sending analysis:', error);
    }
  }

  const editRecord = ref<Analysis>();

  /**
   * 编辑
   * @param record
   */
  function edit(record: Analysis) {
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
  <a-modal :title="form._isNew ? '新增药品' : '编辑药品'" v-model:visible="showModal" @ok="submit" @cancel="cancel">
    <a-form ref="formModel" :model="form" :labelCol="{ span: 5 }" :wrapperCol="{ span: 16 }">
      <a-form-item required label="检查项目" name="department">
        <a-cascader
          v-model:value="form.department"
          :options="analysisProject"
        />
      </a-form-item>
      <a-form-item label="日期" name="time">
        <a-date-picker v-model:value="form.time" />
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="analysisList" :pagination="false">
    <template #title>
      <div class="flex justify-between pr-4">
        <a-button type="primary" @click="sendAnalysisList" :loading="formLoading">
          上传药品清单
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
      <div class="flex items-stretch" v-if="column.dataIndex === 'time'">
        {{ text?.format('YYYY-MM-DD') }}
      </div>
      <template v-else-if="column.dataIndex === 'edit'">
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
      <div v-else class="text-subtext">
        {{ text }}
      </div>
    </template>
  </a-table>
</template>
