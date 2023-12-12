<script lang="ts" setup>
  import { getBase64 } from '@/utils/file';
  import { FormInstance } from 'ant-design-vue';
  import { reactive, ref } from 'vue';
  import dayjs from 'dayjs';
  import { Dayjs } from 'dayjs';
  import { EditFilled } from '@ant-design/icons-vue';

  const columns = [
    {
      title: '姓名',
      dataIndex: 'name',
      width: 200
    },
    { title: 'ID', dataIndex: 'email', width: 250 },
    { title: '岗位', dataIndex: 'department' },
    { title: '密码', dataIndex: 'jobs' },
    { title: '操作', dataIndex: 'edit', width: 200 },
  ];

  type Author = {
    name?: string;
    email?: string;
    avatar?: string;
    department?: string;
    jobs?: string;
    position?: string[];
    role?: string;
    status?: number;
    time?: Dayjs;
    _edit?: boolean;
    _isNew?: boolean;
  };

  const authors = reactive<Author[]>([
    {
      name: 'Li Zhi',
      email: '1126263215@qq.com',
      avatar: '/src/assets/avatar/face-1.jpg',
      jobs: 'developer',
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

  const newAuthor = (author?: Author) => {
    if (!author) {
      author = { _isNew: true };
    }
    author.name = undefined;
    author.email = undefined;
    author.avatar = undefined;
    author.position = [];
    author.department = undefined;
    author.jobs = undefined;
    author.status = 0;
    author.time = dayjs();
    return author;
  };

  const copyObject = (target: any, source?: any) => {
    if (!source) {
      return target;
    }
    Object.keys(target).forEach((key) => (target[key] = source[key]));
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

  async function extractImg(file: Blob, author: Author) {
    await getBase64(file).then((res) => {
      author.avatar = res;
    });
  }

  function submit() {
    formLoading.value = true;
    formModel.value
      ?.validateFields()
      .then((res: Author) => {
        res.department = res?.position?.[0];
        res.jobs = res?.position?.[1];
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

  const editRecord = ref<Author>();

  /**
   * 编辑
   * @param record
   */
  function edit(record: Author) {
    editRecord.value = record;
    copyObject(form, record);
    form.position = [form.department!, form.jobs!];
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
      <a-form-item label="照片" required name="avatar">
        <a-upload :show-upload-list="false" :beforeUpload="(file: File) => extractImg(file, form)">
          <img class="h-8 p-0.5 rounded border border-dashed border-border" v-if="form.avatar" :src="form.avatar" />
          <a-button v-else type="dashed">
            <template #icon>
              <UploadOutlined />
            </template>
            上传
          </a-button>
        </a-upload>
      </a-form-item>
      <a-form-item label="姓名" required name="name">
        <a-input v-model:value="form.name" />
      </a-form-item>
      <a-form-item required label="ID" name="email">
        <a-input v-model:value="form.email" />
      </a-form-item>
      <a-form-item required label="岗位" name="department">
        <a-input v-model:value="form.department" />
      </a-form-item>
      <a-form-item required label="密码" name="jobs">
        <a-input v-model:value="form.department" />
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="authors" :pagination="false">
    <template #title>
      <div class="flex justify-between pr-4">
        <h3>医生列表</h3>
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
        <img class="w-12 rounded" :src="record.avatar" />
        <div class="flex-col flex justify-evenly ml-2">
          <span class="text-title font-bold">{{ text }}</span>
        </div>
      </div>
      <div class="" v-else-if="column.dataIndex === 'position'">
        <div class="text-title font-bold">
          {{ record.jobs }}
        </div>
        <div class="text-subtext">
          {{ record.department }}
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
      </template>
      <div v-else class="text-subtext">
        {{ text }}
      </div>
    </template>
  </a-table>
</template>