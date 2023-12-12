<script lang="ts" setup>
  import { FormInstance } from 'ant-design-vue';
  import { reactive, ref } from 'vue';
  import { DeleteFilled, DeleteOutlined, EditFilled, EditOutlined } from '@ant-design/icons-vue';
  import axios from 'axios';
  import { useAccountStore } from '@/store';

  const accountStore = useAccountStore();
  accountStore.init();
  const username = accountStore.account?.username;

  const columns = [
    { title: '药名', dataIndex: 'name', width: 300 },
    { title: 'ID', dataIndex: 'id', width: 300 },
    { title: '用量', dataIndex: 'amount' },
    { title: '操作', dataIndex: 'edit', width: 100 },
  ];

  const columns2 = [
    { title: '药名', dataIndex: 'name', width: 300 },
    { title: 'ID', dataIndex: 'id' },
    { title: '操作', dataIndex: 'edit', width: 100 },
  ];

  const columnPatient = [
    { title: '病人信息', dataIndex: 'name' },
    { title: '操作', dataIndex: 'edit', width: 50 },
  ];
  
  type Medicine = {
    amount?: number;
    name?: string;
    id?: string;
    status?: number;
    _edit?: boolean;
    _isNew?: boolean;
  };

  type Patient = {
    name?: string;
    id?: string;
  }

  const patient = reactive<Patient[]>([
    {
      name: '',
      id: '',
    }
  ]);

  const medicineGroup = reactive<Medicine[]>([]);

  const searchList = reactive<Medicine[]>([]);

  const showModal = ref(false);
  const showModal2 = ref(false);
  const showModal3 = ref(false);

  const newMedicine = (Medicine?: Medicine) => {
    if (!Medicine) {
      Medicine = { _isNew: true };
    }
    Medicine.amount = undefined;
    Medicine.name = undefined;
    Medicine.status = 0;
    return Medicine;
  };
  const newPatient = (Patient?: Patient) => {
    if (!Patient) {
      Patient = {};
    }
    Patient.name = undefined;
    Patient.id = undefined;
    return Patient;
  };

  const copyObject = (target: Medicine, source?: Medicine) => {
    if (!source) {
      return target;
    }
    target.name = source.name;
    target.amount = source.amount;
    target._isNew = false;
  };
  const copyObject3 = (target: Patient, source?: Patient) => {
    if (!source) {
      return target;
    }
    target.name = source.name;
    target.id = source.id;
  };

  const form = reactive<Medicine>(newMedicine());
  const form2 = reactive<Medicine>(newMedicine());
  const form3 = reactive<Patient>(newPatient());

  function reset() {
    return newMedicine(form);
  }
  function reset2() {
    return newMedicine(form2);
  }
  function reset3() {
    return newPatient(form3);
  }

  function cancel() {
    showModal.value = false;
    reset();
  }
  function cancel2() {
    showModal2.value = false;
    reset2();
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
      .then((res: Medicine) => {
        res.amount = res?.amount;
        res.name = res?.name;
        if (form._isNew) {
          medicineGroup.push({ ...res });
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

  function add2List() {
    formLoading.value = true;
    formModel.value
      ?.validateFields()
      .then((res: Medicine) => {
        copyObject(editRecord.value, form2);
        medicineGroup.push(editRecord.value);
        showModal2.value = false;
        reset2();
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
        copyObject3(editRecord3.value, res);
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

  const medicineName = reactive<string[]>([]);
  const medicineID = reactive<string[]>([]);
  const medicineAmount = reactive<number[]>([]);
  function copyArray(){
    medicineGroup.forEach((item) => {
      medicineName.push(item.name);
      medicineID.push(item.id);
      medicineAmount.push(item.amount);
    })
    console.log(medicineGroup);
  }
  function clearArray(){
    medicineName.length = 0;
    medicineID.length = 0;
    medicineAmount.length = 0;
  }
  
  async function sendMedicineGroup() {
    try {
        copyArray();
        const response = await axios.post('http://127.0.0.1:8000/api/sendMedicineList/', {
          username: username,
          Pid: patient[0].id,
          MedicineList: medicineName,
          IDList: medicineID,
          AmountList: medicineAmount,
        });
        clearArray();
    } catch (error) {
        console.error('Error sending medicineList:', error);
    }
  }

  async function searchMedicineList(query) {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/searchMedicineList/',{
          params:{
            name: query,
          }
        });
        searchList.length = 0; // 清空数组

        // 将获取到的数据放入数组中
        response.data.medicineList.forEach((item) => {
            searchList.push({ name: item.name, id: item.id, amount: 0});
        });
    } catch (error) {
        console.error('Error searching medicine list:', error);
    }
  }

  function delLine(record: Medicine){
    medicineGroup.forEach((item, index) => {
      if (item.amount == record.amount) {
        medicineGroup.splice(index, 1);
        return;
      }
    })
  }

  const editRecord = ref<Medicine>();
  const editRecord3 = ref<Patient>();

  /** 
   * 编辑
   * @param record
   */
  function edit(record: Medicine) {
    editRecord.value = record;
    copyObject(form, record);
    showModal.value = true;
  }
  function edit2(record: Medicine) {
    editRecord.value = record;
    copyObject(form2, record);
    showModal2.value = true;
  }
  function edit3(record: Patient) {
    editRecord3.value = record;
    copyObject3(form3, record);
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

  <a-modal :title="form._isNew ? '新增药品' : '编辑药品'" v-model:visible="showModal" @ok="submit" @cancel="cancel">
    <a-form ref="formModel" :model="form" :labelCol="{ span: 5 }" :wrapperCol="{ span: 16 }">
      <a-form-item required label="药名" name="name">
        <a-input v-model:value="form.name" />
      </a-form-item>
      <a-form-item required label="用量" name="amount">
        <a-input v-model:value="form.amount" />
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="medicineGroup" :pagination="false">
    <template #title>
      <div class="flex justify-between pr-4">
        <h3>开药清单</h3>
        <a-button type="primary" @click="sendMedicineGroup" :loading="formLoading">
          上传药品清单
        </a-button>
      </div>
    </template>
    <template #bodyCell="{ column, text, record }">
      <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
        <div class="flex-col flex justify-evenly ml-1">
          <span class="text-title font-bold">{{ text }}</span>
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
        <a-button :disabled="showModal" type="link" @click="delLine(record)">
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

  <a-divider></a-divider>

  <!-- search -->

  <a-modal :title="form2._isNew ? '新增' : '添加到药品清单'" v-model:visible="showModal2" @ok="add2List" @cancel="cancel2">
    <a-form ref="formModel" :model="form2" :labelCol="{ span: 5 }" :wrapperCol="{ span: 16 }">
      <a-form-item label="输入用量" required name="amount">
        <a-input v-model:value="form2.amount" />
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns2" :dataSource="searchList" :pagination="false">
    <template #title="{}">
      <div class="flex justify-between pr-4">
        <h3>查找并添加药品</h3>
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
      </div>
    </template>
    <template #bodyCell="{ column, text, record }">
      <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
        <div class="flex-col flex justify-evenly ml-1 ">
          <span class="text-title font-bold">{{ text }}</span>
        </div>
      </div>
      <template v-else-if="column.dataIndex === 'edit'">
        <a-button :disabled="showModal2" type="link" @click="edit2(record)">
          <template #icon>
            <EditFilled />
          </template>
          添加
        </a-button>
      </template>
      <div v-else class="text-subtext">
        {{ text }}
      </div>
    </template>
  </a-table>
</template>
