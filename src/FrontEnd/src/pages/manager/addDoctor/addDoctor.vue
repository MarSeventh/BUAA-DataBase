<script lang="ts" setup>
  import { getBase64 } from '@/utils/file';
  import { FormInstance , message} from 'ant-design-vue';
  import { reactive, ref } from 'vue';
  import { EditFilled, EditOutlined } from '@ant-design/icons-vue';
  import axios from 'axios';

  const columns = [
    {
      title: '姓名',
      dataIndex: 'name',
      width: 200
    },
    { title: '岗位', dataIndex: 'department', width: 300},
    { title: '密码', dataIndex: 'jobs' },
    { title: '操作', dataIndex: 'edit', width: 50 },
    { title: '', dataIndex: 'send', width: 50 },
  ];

  type Author = {
    name?: string;
    department?: string;
    jobs?: string;
    _edit?: boolean;
    _isNew?: boolean;
  };

  const authors = reactive<Author[]>([
  ]);

  function addNew() {
    showModal.value = true;
    form._isNew = true;
  }

  const showModal = ref(false);

  const newAuthor = (author?: Author) => {
    if (!author) {
      author = { _isNew: true };
    }
    author.name = undefined;
    author.department = undefined;
    author.jobs = undefined;
    return author;
  };

  const copyObject = (target: any, source?: any) => {
    if (!source) {
      return target;
    }
    target.name = source.name;
    target.department = source.department;
    target.jobs = source.jobs;
    target._isNew = false;
  };

  const form = reactive<Author>(newAuthor());

  function reset() {
    return newAuthor(form);
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
      .then((res: Author) => {
        if (form._isNew) {
          authors.push({ ...res });
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

  async function addDoctor() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/addDoctor/', {
          username: authors[0].name,
          password: authors[0].jobs,
          tittle: authors[0].department,
        });
        message.success('上传成功')
    } catch (error) {
    message.error('上传失败')
    console.error('Error sending Diagnosis:', error);
  }
  }

  const editRecord = ref<Author>();

  /**
   * 编辑
   * @param record
   */
  function edit(record: Author) {
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
  <a-modal :title="form._isNew ? '新增' : '编辑'" v-model:visible="showModal" @ok="submit" @cancel="cancel">
    <a-form ref="formModel" :model="form" :labelCol="{ span: 5 }" :wrapperCol="{ span: 16 }">
      <a-form-item label="姓名" required name="name">
        <a-input v-model:value="form.name" />
      </a-form-item>
      <a-form-item required label="岗位" name="department">
        <a-input v-model:value="form.department" />
      </a-form-item>
      <a-form-item required label="密码" name="jobs">
        <a-input v-model:value="form.jobs" />
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="authors" :pagination="false">
    <template #title>
      <div class="flex justify-between pr-4">
        <h3>添加医生</h3>
        <a-button type="primary" @click="addNew" :loading="formLoading">
          <template #icon>
            <PlusOutlined />
          </template>
          新增
        </a-button>
      </div>
    </template>
    <template #bodyCell="{ column, text, record }">
      <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
        <div class="flex-col flex justify-evenly ml-1">
          <span class="text-title font-bold">{{ text }}</span>
        </div>
      </div>
      <template v-else-if="column.dataIndex === 'edit'">
        <a-button :disabled="showModal" type="link" @click="edit(record)">
          <template #icon>
            <EditFilled />
          </template>
          编辑
        </a-button>
      </template>
      <template v-else-if="column.dataIndex === 'send'">
        <a-button :disabled="showModal" type="link" @click="addDoctor">
          <template #icon>
            <EditOutlined />
          </template>
          上传
        </a-button>
      </template>
      <div v-else class="text-subtext">
        {{ text }}
      </div>
    </template>
  </a-table>
</template>