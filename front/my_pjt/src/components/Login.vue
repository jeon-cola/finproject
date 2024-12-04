<template>
  <div class="login-container">
    <div class="login-card">
      <h2 v-if="!isAuthenticated" class="card-title">로그인</h2>
      <form v-if="!isAuthenticated" @submit.prevent="handleLogin">
        <div class="input-group">
          <input
            v-model="username"
            placeholder="사용자 이름"
            required
            class="input-field"
          />
        </div>
        <div class="input-group">
          <input
            v-model="password"
            type="password"
            placeholder="비밀번호"
            required
            class="input-field"
          />
        </div>
        <div class="input-group">
          <button type="submit" class="login-button">로그인</button>
        </div>
      </form>

      <div v-if="!isAuthenticated" class="signup-section">
        <h5>아이디가 없으십니까?</h5>
        <RouterLink :to="{ name: 'signup' }" class="signup-link">
          회원가입
        </RouterLink>
      </div>

      <!-- 로그아웃 버튼 -->
      <div v-if="isAuthenticated" class="logout-section">
        <h2 class="card-title">프로필</h2>
        <p class="welcome-message">{{ userProfile.username }}님 환영합니다!</p>
        <button @click="handleLogout" class="logout-button">로그아웃</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    const username = ref('');
    const password = ref('');

    const isAuthenticated = computed(() => userStore.isAuthenticated);
    const userProfile = computed(() => userStore.user);

    const handleLogin = async () => {
      try {
        await userStore.login(username.value, password.value);
        alert('로그인 성공');
        router.push({ name: 'home' });
      } catch (error) {
        alert('로그인 실패: 존재하지 않는 회원입니다.');
      }
    };

    const handleLogout = async () => {
      try {
        await userStore.logout();
        alert('로그아웃 성공');
        router.push('');
      } catch (error) {
        alert('로그아웃 실패');
      }
    };

    return {
      username,
      password,
      handleLogin,
      handleLogout,
      isAuthenticated,
      userProfile,
    };
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
  color: #f8fafc; /* 밝은 텍스트 */
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 20px;
}

.login-card {
  background-color: #1e293b; /* 다크 네이비 카드 배경 */
  width: 100%;
  max-width: 400px;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
}

.card-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #93c5fd; /* 밝은 블루 */
  text-align: center;
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

.login-button {
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

.login-button:hover {
  background-color: #1d4ed8; /* 더 어두운 블루 */
}

.signup-section {
  text-align: center;
  margin-top: 20px;
}

.signup-link {
  color: #93c5fd;
  text-decoration: none;
}

.signup-link:hover {
  text-decoration: underline;
}

.logout-section {
  text-align: center;
}

.welcome-message {
  margin: 15px 0;
  font-size: 16px;
}

.logout-button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background-color: #dc2626; /* 레드 */
  color: #f8fafc;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #b91c1c; /* 더 어두운 레드 */
}
</style>
