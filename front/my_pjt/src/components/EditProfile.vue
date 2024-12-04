<template>
  <div class="profile-container">
    <div class="card">
      <div class="card-header">
        <h1>프로필 수정</h1>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleUpdateProfile">
          <div class="form-group">
            <label for="username">이름</label>
            <input id="username" v-model="username" placeholder="사용자 이름" required />
          </div>
          <div class="form-group">
            <label for="email">이메일</label>
            <input id="email" v-model="email" type="email" placeholder="이메일" required />
          </div>
          <div class="form-group">
            <label for="password">비밀번호</label>
            <input id="password" v-model="password" type="password" placeholder="비밀번호" />
          </div>
          <div class="form-group">
            <label for="nickname">닉네임</label>
            <input id="nickname" v-model="nickname" placeholder="닉네임" />
          </div>
          <div class="form-group">
            <label for="age">나이</label>
            <input id="age" v-model="age" type="number" placeholder="나이" />
          </div>
          <div class="form-group">
            <label for="asset">현재 가진 재산</label>
            <input id="asset" v-model="asset" type="number" placeholder="현재 가진 재산" />
          </div>
          <div class="form-group">
            <label for="salary">연봉</label>
            <input id="salary" v-model="salary" type="number" placeholder="연봉" />
          </div>
          <button type="submit" class="submit-button">프로필 수정</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

// Pinia 스토어 사용
const userStore = useUserStore();

// 입력 필드 초기화
const username = ref(userStore.user?.username || '');
const email = ref(userStore.user?.email || '');
const password = ref('');
const nickname = ref(userStore.user?.nickname || '');
const age = ref(userStore.user?.age || '');
const asset = ref(userStore.user?.asset || 0); // 정수로 초기화
const salary = ref(userStore.user?.salary || 0);
const router = useRouter();

// 프로필 수정 처리 함수
const handleUpdateProfile = async () => {
  try {
    const payload = {
      username: username.value,
      email: email.value,
      password: password.value,
      nickname: nickname.value,
      age: age.value,
      asset: parseInt(asset.value, 10), // 정수로 변환
      salary: parseInt(salary.value, 10),
    };
    await userStore.updateProfile(payload);
    alert('프로필 수정 성공');
    router.push({ name: 'profile' });
  } catch (error) {
    console.error('프로필 수정 실패:', error);
    alert('필수 정보를 입력하지 않았습니다.');
  }
};
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #0f172a;
  color: #f8fafc;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  padding: 20px;
}

.card {
  background-color: #1e293b;
  padding: 30px;
  width: 400px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
}

.card-header h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  color: #93c5fd;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

label {
  font-size: 14px;
  color: #f8fafc;
}

input {
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #334155;
  color: #f8fafc;
}

input::placeholder {
  color: #cbd5e1;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background-color: #2563eb;
  color: #f8fafc;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #1d4ed8;
}
</style>
