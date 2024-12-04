<template>
  <div class="exchange-container">
    <div class="card">
      <div class="card-header">
        <h1>환율 계산기</h1>
      </div>
      <div class="card-body">
        <!-- 왼쪽 통화 입력 -->
        <div class="left-container">
          <label for="currency-select">통화 선택</label>
          <select id="currency-select" v-model="selectCurrent" class="select-dropdown">
            <option v-for="result in store.exchangeRateList" :key="result.cur_unit" :value="result">
              {{ result.cur_nm }}
            </option>
          </select>
          <label for="amount-input">금액 입력</label>
          <input type="text" id="amount-input" v-model="text" :placeholder="selectCurrent?.cur_unit || '통화 선택'" />
        </div>

        <!-- 오른쪽 환율 계산 결과 -->
        <div class="right-container">
          <label for="krw-output">환산 결과 (KRW)</label>
          <input type="text" id="krw-output" v-model="text2" placeholder="원" />

          <hr class="divider" />

          <div v-if="selectCurrent" class="exchange-info">
            <p><strong>{{ selectCurrent.cur_nm }} ({{ selectCurrent.cur_unit }})</strong></p>
            <p>환율 기준: <strong>{{ selectCurrent.deal_bas_r }} 원</strong></p>
            <p>환산 금액: <strong>{{ exchangeCost.toLocaleString() }} 원</strong></p>
            <p>환산 통화: <strong>{{ exchangeCost2.toLocaleString() }} {{ selectCurrent.cur_unit }}</strong></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { onMounted, ref, computed } from 'vue';

const store = useCounterStore();

onMounted(() => {
  store.getExchangeRate();
});

const text = ref(null);
const selectCurrent = ref(null);
const text2 = ref(null);

const exchangeCost = computed(() => {
  if (selectCurrent.value && text.value) {
    let dealBaseR = selectCurrent.value.deal_bas_r;
    if (dealBaseR.includes(',')) {
      dealBaseR = Number(dealBaseR.replace(/,/g, ''));
    } else {
      dealBaseR = Number(dealBaseR);
    }

    const amount = Number(text.value);
    return dealBaseR * amount;
  }
  return 0;
});

const exchangeCost2 = computed(() => {
  if (selectCurrent.value && text2.value) {
    let dealBaseR2 = selectCurrent.value.deal_bas_r;
    if (dealBaseR2.includes(',')) {
      dealBaseR2 = Number(dealBaseR2.replace(/,/g, ''));
    } else {
      dealBaseR2 = Number(dealBaseR2);
    }

    const amount2 = Number(text2.value);
    return amount2 / dealBaseR2;
  }
  return 0;
});
</script>

<style scoped>
/* 전체 컨테이너 */
.exchange-container {
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
  width: 500px;
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

/* 왼쪽 컨테이너 */
.left-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.left-container label {
  font-weight: bold;
  margin-bottom: 5px;
}

.select-dropdown {
  background-color: #334155; /* 다크 네이비 드롭다운 */
  color: #f8fafc;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
}

#amount-input {
  background-color: #475569; /* 어두운 입력 필드 */
  color: #f8fafc;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
}

/* 오른쪽 컨테이너 */
.right-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

#krw-output {
  background-color: #475569; /* 어두운 입력 필드 */
  color: #f8fafc;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
}

/* 환율 정보 */
.exchange-info p {
  margin: 5px 0;
  font-size: 14px;
}

/* 구분선 */
.divider {
  border: 0;
  height: 1px;
  background: linear-gradient(to right, transparent, #64748b, transparent);
}
</style>
