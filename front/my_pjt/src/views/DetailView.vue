<template>
  <div class="go">
    <h1 class="title">Detail Page</h1>
    <div v-if="store.result" class="card">
      <div class="card-body">
        <p><strong>은행명:</strong> {{ store.result.kor_co_nm }}</p>
        <p><strong>상품명:</strong> {{ store.result.fin_prdt_nm }}</p>
        <p><strong>가입 방법:</strong> {{ store.result.join_way }}</p>
        <p><strong>만급 후 이자율:</strong> {{ store.result.mtrt_int }}</p>
        <p><strong>특별 조건:</strong> {{ store.result.spcl_cnd }}</p>
        <p><strong>기타 정보:</strong> {{ store.result.etc_note }}</p>
        <p><strong>저축 금리:</strong> {{ store.result.intr_rate }}<strong>%</strong></p>
        <p><strong>최고 우대 금리:</strong> {{ store.result.intr_rate2 }}<strong>%</strong></p>
        <p><strong>금리 유형:</strong> {{ store.result.intr_rate_type_nm }}</p>
        <p><strong>저축 기간:</strong> {{ store.result.save_trm }}<strong>개월</strong></p>
        <button @click="saveDeposit" class="save-button">저장하기</button>
        <button @click="goToDeposit" class="close-button">X</button>
      </div>
    </div>

    <div v-else>
      <p>데이터를 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';

const store = useCounterStore();
const router = useRouter();

const saveDeposit = function() {
  store.saveDeposit();
};

const goToDeposit = function() {
  router.push({ name: 'deposit' }); // depositView 로 이동
};
</script>

<style scoped>
.go {
  padding-top: 50px;
  background-color: #000000; /* 배경 색상 검은색 */
  color: white; /* 글자 색상 홍색 */
  min-height: 100vh; /* 화면 전체 높이 */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.card {
  background-color: #ffffff; /* 카드 배경 하우에색 */
  color: #000000; /* 카드 글자 검은색 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 카드 그림자 효과 */
  width: 80%;
  max-width: 600px;
  position: relative;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #0056b3;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: gray;
  color: white;
  border: none;

  width: 25px;
  height: 25px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  background-color: blue;
}
</style>