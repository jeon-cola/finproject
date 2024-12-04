<template>
  <div class="signup-container">
    <div class="signup-card">
      <h2 class="card-title">회원가입</h2>
      <form @submit.prevent="handleSignup">
        <div class="input-group">
          <input
            v-model="username"
            placeholder="사용자 이름"
            class="input-field"
            required
          />
        </div>
        <div class="input-group">
          <input
            v-model="email"
            type="email"
            placeholder="이메일"
            class="input-field"
            required
          />
        </div>
        <div class="input-group">
          <input
            v-model="password"
            type="password"
            placeholder="비밀번호"
            class="input-field"
            required
          />
        </div>
        <div class="input-group">
          <input
            v-model="nickname"
            placeholder="닉네임"
            class="input-field"
            required
          />
        </div>
        <div class="input-group">
          <button type="submit" class="signup-button">회원가입</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  setup() {
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const nickname = ref('');
    const router = useRouter();

    const handleSignup = async () => {
      try {
        await axios.post('http://localhost:8000/accounts/signup/', {
          username: username.value,
          email: email.value,
          password: password.value,
          nickname: nickname.value,
        });
        alert('회원가입 성공!');
        router.push({ name: 'login' });
      } catch (error) {
        console.error('회원가입 실패:', error);
        alert('회원가입 실패: 정보를 확인해주세요.');
      }
    };

    return { username, email, password, nickname, handleSignup };
  },
};
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  background-color: #0f172a; /* 다크 블루 배경 */
  color: #f8fafc; /* 밝은 텍스트 색 */
}

.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 20px;
}

.signup-card {
  background-color: #1e293b; /* 다크 네이비 카드 배경 */
  width: 100%;
  max-width: 400px;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
}

.card-title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #93c5fd; /* 밝은 블루 */
}

.input-group {
  margin-bottom: 15px;
}

.input-field {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background-color: #334155; /* 다크 네이비 입력 필드 */
  color: #f8fafc;
  border: none;
  border-radius: 8px;
}

.signup-button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background-color: #2563eb; /* 밝은 블루 */
  color: #f8fafc;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.signup-button:hover {
  background-color: #1d4ed8; /* 더 어두운 블루 */
}
</style>
