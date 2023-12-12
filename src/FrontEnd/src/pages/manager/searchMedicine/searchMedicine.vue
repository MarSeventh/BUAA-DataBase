<script lang="ts" setup>
  import { FormInstance } from 'ant-design-vue';
  import { reactive, ref } from 'vue';
  import dayjs from 'dayjs';
  import { Dayjs } from 'dayjs';
  import { EditFilled } from '@ant-design/icons-vue';
  import axios from 'axios';

  const columns = [
    {
      title: '药品名',
      dataIndex: 'name',
      width: 350
    },
    { title: '药品ID', dataIndex: 'id', width: 350 },
    { title: '库存量', dataIndex: 'amount' },
    { title: '操作', dataIndex: 'edit', width: 200 },
  ];

  type Medicine = {
    name?: string;
    id?: string;
    amount?: number;
    status?: number;
    time?: Dayjs;
    _edit?: boolean;
    _isNew?: boolean;
  };

  const medicineList = reactive<Medicine[]>([
    {
      name: '感冒药',
      id: '1',
      amount: 100,
      status: 1,
      time: dayjs(),
    },
  ]);

  function addNew() {
    showModal.value = true;
    form._isNew = true;
  }

  const showModal = ref(false);

  const newMedicine = (author?: Medicine) => {
    if (!author) {
      author = { _isNew: true };
    }
    author.name = undefined;
    author.id = undefined;
    author.amount = undefined;
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

  const form = reactive<Medicine>(newMedicine());

  function reset() {
    return newMedicine(form);
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
      .then((res: Medicine) => {
        res.amount = res?.amount;
        if (form._isNew) {
          medicineList.push({ ...res });
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

  function display(record: Medicine){
    showModal.value = true;
  }

  async function searchMedicineList(record: string) {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/getMedicineList/',{
          params:{
            id: record
          }
        });
        medicineList.length = 0; // 清空数组

        // 将获取到的部门数据放入数组中
        response.data.medicineList.forEach((item) => {
            medicineList.push({ name: item.name, id: item.id, amount: item.amount });
        });
    } catch (error) {
        console.error('Error fetching medicineList:', error);
    }
  }

  const editRecord = ref<Medicine>();

  /**
   * 编辑
   * @param record
   */
  function edit(record: Medicine) {
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
      <a-form-item label="药品名" required name="name">
        <a-input v-model:value="form.name" />
      </a-form-item>
      <a-form-item required label="药品ID" name="email">
        <a-input v-model:value="form.id" />
      </a-form-item>
      <a-form-item required label="库存" name="department">
        <a-input v-model:value="form.amount" />
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="medicineList" :pagination="false">
    <template #title="{record}">
      <div class="flex justify-between pr-4">
        <h3>药品列表</h3>
        <div class="global-search-wrapper" style="width: 300px">
          <a-auto-complete
            class="global-search"
            style="width: 100%"
            option-label-prop="title"
          >
            <a-input-search placeholder="输入要查找的药品id" enterButton>
              <a-button :disabled="showModal" type="link" @click="searchMedicineList(record);">
                <PlusOutlined />
              </a-button>
            </a-input-search>
          </a-auto-complete>
        </div>
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
        <div class="flex-col flex justify-evenly ml-1 ">
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
      <div v-else class="text-subtext">
        {{ text }}
      </div>
    </template>
  </a-table>
</template>