<script lang="ts" setup>
  import { getBase64 } from '@/utils/file';
  import { FormInstance } from 'ant-design-vue';
  import { reactive, ref } from 'vue';

  const accountStore = useAccountStore();
  accountStore.init();
  const username = accountStore.account?.username;

  const columns = [
    { title: '时段/天', dataIndex: 'jobs', width: 150},
    { title: '星期一', dataIndex: 'day1', width: 200 },
    { title: '星期二', dataIndex: 'day2', width: 200 },
    { title: '星期三', dataIndex: 'day3', width: 200 },
    { title: '星期四', dataIndex: 'day4', width: 200 },
    { title: '星期五', dataIndex: 'day5', width: 200 },
    { title: '星期六', dataIndex: 'day6', width: 200 },
    { title: '星期日', dataIndex: 'day7', width: 200 },
  ];
 
  const columnPatient = [
    {
      title: '病人信息',
      dataIndex: 'name',
    },
  ];

  type Author = {
    jobs?: string;
    day1?: string;
    day2?: string;
    day3?: string;
    day4?: string;
    day5?: string;
    day6?: string;
    day7?: string;
    status?: number;
    _edit?: boolean;
    _isNew?: boolean;
  };


  const authors = reactive<Author[]>([
    {
      jobs: '上午',
    },
    {
      jobs: '下午',
    },
  ]);

  const showModal = ref(false);

  const newAuthor = (author?: Author) => {
    if (!author) {
      author = { _isNew: true };
    }
    author.jobs = undefined;
    author.day1 = undefined;
    author.day2 = undefined;
    author.day3 = undefined;
    author.day4 = undefined;
    author.day5 = undefined;
    author.day6 = undefined;
    author.day7 = undefined;
    author.status = 0;
    return author;
  };

  const copyObject = (target: any, source?: any) => {
    if (!source) {
      return target;
    }
    Object.keys(target).forEach((key) => (target[key] = source[key]));
  };

  const form = reactive<Author>(newAuthor());

  async function fetchAnalysisName() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/getAnalysisName/', {
          username
          //TODO: 看hyx的貌似是username : username?
        });
        authors[0].day1 = response.data[0];
        authors[0].day2 = response.data[1];
        authors[0].day3 = response.data[2];
        authors[0].day4 = response.data[3];
        authors[0].day5 = response.data[4];
        authors[0].day6 = response.data[5];
        authors[0].day7 = response.data[6];
        authors[1].day1 = response.data[7];
        authors[1].day2 = response.data[8];
        authors[1].day3 = response.data[9];
        authors[1].day4 = response.data[10];
        authors[1].day5 = response.data[11];
        authors[1].day6 = response.data[12];
        authors[1].day7 = response.data[13];
    } catch (error) {
        console.error('Error fetching analysis name:', error);
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
  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="authors" :pagination="false">
    <template #title>
      <div class="flex justify-between pr-4">
      </div>
    </template>
    <template #bodyCell="{ column, text, record }">
      <div class="" v-if="column.dataIndex === 'position'">
        <div class="text-title font-bold">
          {{ record.jobs }}
        </div>
        <div class="text-subtext">
          {{ record.department }}
        </div>
      </div>
    </template>
  </a-table>
</template>
