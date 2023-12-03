<template>
    <div class="container">
        <h2 style="color: white;margin: 30px">智能导医台</h2>
        <a-textarea style="width: 50vh;opacity: 0.85;" v-model="question" type="textarea" :rows="4"
            placeholder="输入您感觉不舒服的地方"></a-textarea>
        <a-card style="margin-top: 15px;opacity: 0.85;" title="就诊建议" class="mt-4 profile-info rounded-xl shadow-lg"
            :bordered="false">
            <div class="description font-bold">
                {{ typedAnswer }}
            </div>
            <a-divider style="margin-bottom: auto;margin-top: 54%;" />
            <div class="text-title font-medium">AI生成，仅供参考！</div>
        </a-card>
        <a-button class="mt-3" type="primary" @click="askQuestion">询问</a-button>
    </div>
</template>
  
<script lang="ts" setup>
import axios from 'axios';
import { ref } from 'vue';

var question = ''
var answer = ''
var typedAnswer = ref('');

async function askQuestion() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/getSuggestion', {
            question: question,
        });

        answer = response.data.answer;

        await typeWriterEffect(answer);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function typeWriterEffect(answer) {
    const delay = 50; // 打字速度，单位为毫秒
    for (let i = 0; i < answer.length; i++) {
        typedAnswer.value += answer.charAt(i);
        await sleep(delay);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

</script>

<style scoped lang="less">
.container {
    display: flex;
    flex-direction: column;
    /* 垂直排列 */
    align-items: center;
    /* 水平居中 */
    text-align: center;
    /* 内容水平居中 */
    justify-content: center;
}

.profile-info {
    width: 50vh;
    height: 40vh;
    overflow-y: auto;

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

  