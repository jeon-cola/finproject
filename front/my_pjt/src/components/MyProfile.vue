<template>
  <div class="profile-container">
    <div class="card">
      <div class="card-header">
        <h1>나의 프로필</h1>
      </div>
      <div class="card-body">
        <div v-if="user">
          <div class="info-group">
            <p><strong>사용자 이름:</strong> {{ user.username }}</p>
          </div>
          <div class="info-group">
            <p><strong>이메일:</strong> {{ user.email }}</p>
          </div>
          <div class="info-group">
            <p><strong>나이:</strong> {{ user.age }}</p>
          </div>
          <div class="info-group">
            <p><strong>닉네임:</strong> {{ user.nickname }}</p>
          </div>
          <div class="info-group">
            <p><strong>현재 보유중인 금액:</strong> {{ formattedAsset }} 원</p>
          </div>
          <div class="info-group">
            <p><strong>연봉:</strong> {{ formattedSalary }} 원</p>
          </div>

          <button @click="goToMy" class="info-button">저장한 상품 정보</button>
          <button @click="goToEditProfile" class="edit-button">정보 수정</button>
          <button @click="confirmDeleteAccount" class="delete-button">회원탈퇴</button>
        </div>
        <div v-else>
          <p>사용자 정보를 불러오는 중입니다...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const userStore = useUserStore();
    const user = computed(() => userStore.user);
    const router = useRouter();

    const goToMy = () => router.push({ name: 'myproduct' });

    const formatNumber = (value) =>
      value ? value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') : 0;

    const formattedAsset = computed(() => formatNumber(user.value?.asset));
    const formattedSalary = computed(() => formatNumber(user.value?.salary));

    const goToEditProfile = () => router.push({ name: 'editProfile' });

    const confirmDeleteAccount = async () => {
      if (confirm('정말로 회원탈퇴를 하시겠습니까?')) {
        try {
          await axios.delete('http://localhost:8000/accounts/delete-account/', {
            headers: { Authorization: `Token ${userStore.token}` },
          });
          alert('계정이 삭제되었습니다.');
          userStore.logout();
          router.push('/signup');
        } catch (error) {
          alert('회원탈퇴 중 문제가 발생했습니다.');
        }
      }
    };

    return {
      user,
      formattedAsset,
      formattedSalary,
      goToMy,
      goToEditProfile,
      confirmDeleteAccount,
    };
  },
};
</script>

<style scoped>
/* 전체 컨테이너 */
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #0f172a; /* 딥 네이비 배경 */
  color: #f8fafc; /* 밝은 텍스트 */
  font-family: 'Helvetica Neue', Arial, sans-serif;
  padding: 20px;
}

/* 카드 스타일 */
.card {
  background-color: #1e293b; /* 다크 네이비 카드 배경 */
  padding: 30px;
  width: 400px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6); /* 고급스러운 그림자 */
  color: #e2e8f0; /* 텍스트 색상 */
}

/* 카드 헤더 */
.card-header h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #f8fafc;
  text-align: center;
}

/* 카드 바디 */
.card-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 정보 그룹 */
.info-group {
  margin-bottom: 15px;
  font-size: 1rem;
  line-height: 1.5;
}

/* 버튼 스타일 */
.info-button,
.edit-button,
.delete-button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.info-button {
  background-color: #2563eb; /* 밝은 블루 */
  color: #f8fafc;
}

.info-button:hover {
  background-color: #1d4ed8; /* 더 어두운 블루 */
  
}

.edit-button {
  background-color: #10b981; /* 밝은 그린 */
  color: #f8fafc;
  margin-top: 15px;
}

.edit-button:hover {
  background-color: #059669; /* 더 어두운 그린 */
  
}

.delete-button {
  background-color: #dc2626; /* 레드 */
  color: #f8fafc;
  margin-top: 15px;
}

.delete-button:hover {
  background-color: #b91c1c; /* 더 어두운 레드 */
}

p {
  margin: 0;
}
</style>
