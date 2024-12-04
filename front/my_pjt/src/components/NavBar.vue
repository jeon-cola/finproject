<template>
  <nav>
    <ul>
      <li><router-link to="/">홈</router-link></li>
      <li><router-link to="/saving">적금</router-link></li>
      <li><router-link to="/deposit">예금</router-link></li>
      <li><router-link to="/exchange_rate">환율</router-link></li>
      <li><router-link to="/posts">게시물</router-link></li> <!-- 게시물 링크 추가 -->
      <li class="nav-item" v-if="isAuthenticated">
  <RouterLink :to="{ name: 'profile' }" id="link">나의 프로필</RouterLink>
</li>
    </ul>
    <div class="auth-buttons">
      <!-- 로그인 버튼 -->
      <button v-if="!isAuthenticated" @click="openAuthModal">로그인</button>
      <!-- 사용자 정보 및 로그아웃 버튼 -->
      <div v-else>
        <span>{{ user?.username }}님</span>
        <button @click="handleLogout">로그아웃</button>
      </div>
    </div>
    <!-- 로그인 및 회원가입 모달 컴포넌트 -->
    <AuthModal v-if="isAuthModalOpen" @close="isAuthModalOpen = false" />
  </nav>
</template>

<script>
import { computed, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import AuthModal from '@/components/AuthModal.vue';

export default {
  components: { AuthModal },
  setup() {
    const userStore = useUserStore();
    
    // Pinia store 상태를 컴포넌트에서 사용
    const isAuthenticated = computed(() => userStore.isAuthenticated);
    const user = computed(() => userStore.user);

    const isAuthModalOpen = ref(false);

    // 로그인 모달 열기
    const openAuthModal = () => {
      isAuthModalOpen.value = true;
    };

    // 로그아웃 처리
    const handleLogout = async () => {
      try {
        await userStore.logout(); // 로그아웃 요청 비동기 처리
        alert('로그아웃 성공');
      } catch (error) {
        console.error('로그아웃 오류:', error);
        alert('로그아웃 실패: ' + (error.response?.data?.error || error.message));
      }
    };

    return {
      isAuthenticated,
      user,
      isAuthModalOpen,
      openAuthModal,
      handleLogout,
    };
  },
};
</script>

<style scoped>
/* 네비게이션 바 스타일 작성 */
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
ul {
  list-style: none;
  display: flex;
  gap: 1rem;
}
.auth-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
}
</style>
