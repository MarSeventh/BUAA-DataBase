<script lang="ts" setup>
  import { FormInstance } from 'ant-design-vue';
  import { reactive, ref } from 'vue';
  import { DeleteFilled, EditFilled, EditOutlined } from '@ant-design/icons-vue';
  import axios from 'axios';

  const columns = [
    {
      title: '药品名',
      dataIndex: 'name',
      width: 200
    },
    { title: '药品ID', dataIndex: 'id', width: 100 },
    { title: '价格', dataIndex: 'price', width: 100 },
    { title: '库存量', dataIndex: 'amount', width: 100 },
    { title: '作用描述', dataIndex: 'description' },
    { title: '操作', dataIndex: 'edit', width: 100 },
  ];

  type Medicine = {
    name?: string;
    id?: string;
    amount?: number;
    price?: number;
    description?: string;
    status?: number;
    _edit?: boolean;
    _isNew?: boolean;
  };

  const medicineList = reactive<Medicine[]>([
    {
      name: '感冒药',
      id: '1',
      price: 100,
      amount: 100,
      description: '治疗感冒',
      status: 1,
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
    author.id = '未生成';
    author.amount = undefined;
    author.price = undefined;
    author.description = undefined;
    author.status = 0;
    return author;
  };

  const copyObject = (target: any, source?: any) => {
    if (!source) {
      return target;
    }
    target.name = source.name;
    target.amount = source.amount;
    target.price = source.price;
    target.description = source.description;
    target._isNew = false;
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

  function delLine(record: Medicine){
    medicineList.forEach((item, index) => {
      if (item.amount == record.amount) {
        medicineList.splice(index, 1);
        return;
      }
    })
  }

  async function searchMedicineList(record: string) {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/getMedicineList/',{
          params:{
            name: record,
          }
        });
        medicineList.length = 0; // 清空数组

        // 将获取到的数据放入数组中
        response.data.medicineList.forEach((item) => {
            medicineList.push({ name: item.name, id: item.id, amount: item.amount });
        });
    } catch (error) {
        console.error('Error fetching medicineList:', error);
    }
  }
  
  async function addMedicine(record: Medicine) {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/addMedicine/', {
          Medicine: record.name,
          Amount: record.amount,
          Price: record.price,
          Description: record.description,
        });
    } catch (error) {
        console.error('Error adding medicine:', error);
    }
  }

  async function deleteMedicine(record: Medicine) {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/deleteMedicine/', {
          params:{
            id: record.id,
          }
        });
        delLine(record);
    } catch (error) {
        console.error('Error deleting medicine:', error);
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
      <a-form-item required label="价格" name="price">
        <a-input v-model:value="form.price" />
      </a-form-item>
      <a-form-item required label="库存" name="amount">
        <a-input v-model:value="form.amount" />
      </a-form-item>
      <a-form-item required label="作用描述" name="description">
        <a-input v-model:value="form.description" />
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
          <a-input-search placeholder="输入要查找的药品id" @search="searchMedicineList" enterButton>  
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
            <EditOutlined />
          </template>
          编辑
        </a-button>
        <a-button :disabled="showModal" type="link" @click="addMedicine(record)">
          <template #icon>
            <EditOutlined />
          </template>
          上传
        </a-button>
        <a-button :disabled="showModal" type="link" @click="deleteMedicine(record)">
          <template #icon>
            <DeleteFilled />
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