<template>
    <div class="signin flex items-center justify-center">
        <signin-box class="shadow-lg" @success="onsigninSuccess" />
    </div>
</template>
<script lang="ts" setup>
import signinBox from './SigninBox.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
function onsigninSuccess() {
    router.push('/login');
}
</script>
<style scoped lang="less">
.signin {
    min-height: max(100vh, 720px);
    margin-top: -78px;
}
</style>
  