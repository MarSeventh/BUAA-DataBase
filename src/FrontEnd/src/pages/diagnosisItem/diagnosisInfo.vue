<script lang="ts" setup>
import { reactive, ref } from 'vue';
import axios from 'axios';
import { useRoute } from "vue-router";

const route = useRoute()

var id = route.query.id
var doctor = ref('')
var statement = ref('')
var time = ref('')


async function fetchDiagnosisInfo() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/getDiagnosis',{
            id: id
        });
        doctor.value = response.data.doctor
        statement.value = response.data.statement
        time.value = response.data.time
    } catch (error) {
        console.error('Error fetching diagnosiss:', error);
    }

}

fetchDiagnosisInfo();
</script>


<template>
  <a-card title="诊断结果" class="profile-info rounded-xl shadow-lg" :bordered="false">
    <div class="description">
      {{ statement }}
    </div>
    <a-divider />
    <div class="text-title font-medium">诊断信息</div>
    <a-descriptions class="profile-list mt-3 font-medium" :column="1">
      <a-descriptions-item label="诊断结果编号">
        {{ id }}
      </a-descriptions-item>
      <a-descriptions-item label="医生姓名">
        {{ doctor }}
      </a-descriptions-item>
      <a-descriptions-item label="诊断时间">
        {{ time }}
      </a-descriptions-item>
    </a-descriptions>
  </a-card>
</template>


<style lang="less" scoped>
.profile-info {
  :deep(.ant-card) {
    &-head {
      @apply border-none;

      &-title {
        @apply font-semibold;
      }
    }

    &-body {
      @apply pt-1;
    }
  }

  :deep(.ant-descriptions) {
    &-row:last-child>td {
      padding-bottom: 0;
    }

    &-item {
      &-content {
        @apply items-center;

        .anticon {
          @apply text-base;

          &:not(:first-child) {
            @apply ml-2;
          }
        }
      }
    }
  }
}
</style>
