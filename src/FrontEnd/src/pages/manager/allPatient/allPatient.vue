<script lang="ts" setup>
  import { reactive, ref } from 'vue';
  import axios from 'axios';

  const columns = [
    {
      title: '姓名',
      dataIndex: 'name',
      width: 200
    },
    { title: 'ID', dataIndex: 'id', width: 200 },
    { title: '是否为社区成员', dataIndex: 'jobs' },
    { title: '总流水（元）', dataIndex : 'sum'},
  ];

  type Author = {
    name?: string;
    id?: number;
    jobs?: string;
    sum?: number;
    _edit?: boolean;
    _isNew?: boolean;
  };

  const authors = reactive<Author[]>([
  ]);

  async function getAllPatients() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/getAllPatients/');
        response.data.patientList.forEach((item) => {
            authors.push({ name: item.name, id: item.id, jobs: item.iscommem , sum: item.sum});
        });
    } catch (error) {
        console.error('Error getting all patients:', error);
    }
  }
  getAllPatients()

  /**
   * 编辑
   * @param record
   */

</script>
<template>
  <!-- 成员表格 -->
  <a-table v-bind="$attrs" :columns="columns" :dataSource="authors" :pagination="false">
    <template #title>
      <div class="flex justify-between pr-4">
        <h3>所有患者</h3>
      </div>
    </template>
    <template #bodyCell="{ column, text, record }">
      <div class="flex items-stretch" v-if="column.dataIndex === 'name'">
        <div class="flex-col flex justify-evenly ml-1">
          <span class="text-title font-bold">{{ text }}</span>
        </div>
      </div>
      <div v-else class="text-subtext">
        {{ text }}
      </div>
    </template>
  </a-table>
</template>