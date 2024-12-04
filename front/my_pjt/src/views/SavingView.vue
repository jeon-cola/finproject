<template>
  <div class='go'>
    <h1>Saving Page</h1>
    <div v-if="filteredData2.length > 0">
      <!-- 필터 부분 -->
      <div class="filter-container">
        <select v-model="selectedKorCoNm">
          <option value="" disabled selected>은행 선택</option>
          <option value="none">상관 없음</option>
          <option v-for="(value, index) in uniqueKorCoNm" :key="index">{{ value }}</option>
        </select>
        <select v-model="selectedIntrRate" :disabled="!uniqueIntrRate.length">
          <option value="" disabled selected>저축 금리 선택</option>
          <option value="none">상관 없음</option>
          <option v-for="(value, index) in uniqueIntrRate" :key="index">{{ value }} </option>
        </select>
        <select v-model="selectedIntrRate2" :disabled="!uniqueIntrRate2.length">
          <option value="" disabled selected>최고 우대 금리</option>
          <option value="none">상관 없음</option>
          <option v-for="(value, index) in uniqueIntrRate2" :key="index">{{ value }}</option>
        </select>
        <select v-model="selectedIntrRateTypeNm" :disabled="!uniqueIntrRateTypeNm.length">
          <option value="" disabled selected>금리 유형</option>
          <option value="none">상관 없음</option>
          <option v-for="(value, index) in uniqueIntrRateTypeNm" :key="index">{{ value }}</option>
        </select>
        <select v-model="selectedRsrvTypeNm" :disabled="!uniqueRsrvTypeNm.length">
          <option value="" disabled selected>적금 유형</option>
          <option value="none">상관 없음</option>
          <option v-for="(value, index) in uniqueRsrvTypeNm" :key="index">{{ value }}</option>
        </select>
        <select v-model="selectedSaveTrm" :disabled="!uniqueSaveTrm.length">
          <option value="" disabled selected>저축 기간</option>
          <option value="none">상관 없음</option>
          <option v-for="(value, index) in uniqueSaveTrm" :key="index">{{ value }} </option>
        </select>
      </div>

      <hr>
      
      <!-- 카드 레이아웃으로 표시 -->
      <div class="cards-container">
        <div class="card" v-for="(result, index) in filteredData2" :key="index">
          <div class="card-header">
            <h3>{{ result.fin_prdt_nm }}</h3>
          </div>
          <div class="card-body">
            <p><strong>은행명:</strong> {{ result.kor_co_nm }}</p>
            <p><strong>금리:</strong> {{ result.intr_rate }}%</p>
            <p><strong>우대 금리:</strong> {{ result.intr_rate2 }}%</p>
            <p><strong>금리 유형:</strong> {{ result.intr_rate_type_nm }}</p>
            <p><strong>적금 유형:</strong> {{ result.rsrv_type_nm }}</p>
            <p><strong>저축 기간:</strong> {{ result.save_trm }}개월</p>
          </div>
          <div class="card-footer">
            <button @click="goToDetail2(result)">자세히 보기</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <p>데이터를 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';
const router = useRouter()

const store = useCounterStore();
onMounted(async () => {
  store.send_saving(); // Saving 데이터를 가져오는 메서드 호출
});

// 선택된 필터 변수들
const selectedKorCoNm = ref(""); // 회사명
const selectedIntrRate = ref(""); // 금리
const selectedIntrRate2 = ref(""); // 추가 금리
const selectedIntrRateTypeNm = ref(""); // 금리 유형
const selectedRsrvTypeNm = ref(""); // 적금 유형
const selectedSaveTrm = ref(""); // 저축 기간

// 필터 옵션 중복 제거
// 필터 옵션 중복 제거 및 의존성 반영
const uniqueKorCoNm = computed(() => {
  return [...new Set(store.filterData2.map(item => item.kor_co_nm))].sort();
});

const uniqueIntrRate = computed(() => {
  return [
    ...new Set(
      store.filterData2
        .filter(item =>
          !selectedKorCoNm.value ||
          selectedKorCoNm.value === 'none' ||
          item.kor_co_nm === selectedKorCoNm.value
        )
        .map(item => item.intr_rate)
    )
  ].sort((a, b) => a - b);
});

const uniqueIntrRate2 = computed(() => {
  return [
    ...new Set(
      store.filterData2
        .filter(item =>
          (!selectedKorCoNm.value || selectedKorCoNm.value === 'none' || item.kor_co_nm === selectedKorCoNm.value) &&
          (!selectedIntrRate.value || selectedIntrRate.value === 'none' || item.intr_rate === Number(selectedIntrRate.value))
        )
        .map(item => item.intr_rate2)
    )
  ].sort((a, b) => a - b);
});

const uniqueIntrRateTypeNm = computed(() => {
  return [
    ...new Set(
      store.filterData2
        .filter(item =>
          (!selectedKorCoNm.value || selectedKorCoNm.value === 'none' || item.kor_co_nm === selectedKorCoNm.value) &&
          (!selectedIntrRate.value || selectedIntrRate.value === 'none' || item.intr_rate === Number(selectedIntrRate.value)) &&
          (!selectedIntrRate2.value || selectedIntrRate2.value === 'none' || item.intr_rate2 === Number(selectedIntrRate2.value))
        )
        .map(item => item.intr_rate_type_nm)
    )
  ].sort();
});

const uniqueRsrvTypeNm = computed(() => {
  return [
    ...new Set(
      store.filterData2
        .filter(item =>
          (!selectedKorCoNm.value || selectedKorCoNm.value === 'none' || item.kor_co_nm === selectedKorCoNm.value) &&
          (!selectedIntrRate.value || selectedIntrRate.value === 'none' || item.intr_rate === Number(selectedIntrRate.value)) &&
          (!selectedIntrRate2.value || selectedIntrRate2.value === 'none' || item.intr_rate2 === Number(selectedIntrRate2.value)) &&
          (!selectedIntrRateTypeNm.value || selectedIntrRateTypeNm.value === 'none' || item.intr_rate_type_nm === selectedIntrRateTypeNm.value)
        )
        .map(item => item.rsrv_type_nm)
    )
  ].sort();
});

const uniqueSaveTrm = computed(() => {
  return [
    ...new Set(
      store.filterData2
        .filter(item =>
          (!selectedKorCoNm.value || selectedKorCoNm.value === 'none' || item.kor_co_nm === selectedKorCoNm.value) &&
          (!selectedIntrRate.value || selectedIntrRate.value === 'none' || item.intr_rate === Number(selectedIntrRate.value)) &&
          (!selectedIntrRate2.value || selectedIntrRate2.value === 'none' || item.intr_rate2 === Number(selectedIntrRate2.value)) &&
          (!selectedIntrRateTypeNm.value || selectedIntrRateTypeNm.value === 'none' || item.intr_rate_type_nm === selectedIntrRateTypeNm.value) &&
          (!selectedRsrvTypeNm.value || selectedRsrvTypeNm.value === 'none' || item.rsrv_type_nm === selectedRsrvTypeNm.value)
        )
        .map(item => item.save_trm)
    )
  ].sort((a, b) => a - b);
});

// 필터된 데이터
const filteredData2 = computed(() => {
  return store.filterData2.filter(item => {
    return (
      (selectedKorCoNm.value === 'none' || !selectedKorCoNm.value || item.kor_co_nm === selectedKorCoNm.value) &&
      (selectedIntrRate.value === 'none' || !selectedIntrRate.value || item.intr_rate === Number(selectedIntrRate.value)) &&
      (selectedIntrRate2.value === 'none' || !selectedIntrRate2.value || item.intr_rate2 === Number(selectedIntrRate2.value)) &&
      (selectedIntrRateTypeNm.value === 'none' || !selectedIntrRateTypeNm.value || item.intr_rate_type_nm === selectedIntrRateTypeNm.value) &&
      (selectedRsrvTypeNm.value === 'none' || !selectedRsrvTypeNm.value || item.rsrv_type_nm === selectedRsrvTypeNm.value) &&
      (selectedSaveTrm.value === 'none' || !selectedSaveTrm.value || item.save_trm === selectedSaveTrm.value)
    );
  }).sort();
});


const goToDetail2 = async (result) => {
  await store.goToDetail2(result); 
  router.push({ name: 'detailsaving' }); 
};
</script>

<style scoped>
.go {
  padding-top: 50px;
  background-color: #000000;
  color: #FFFFFF;
  padding: 0 20px;
  padding-top: 50px;
}

/* 제목 스타일 */
h1 {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 34px;
  line-height: 44px;
  text-align: center;
  margin-bottom: 20px;
  color: #FFFFFF;
}

/* 필터 컨테이너 스타일 */
.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;

}

select {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 16px;
  padding: 10px;
  margin: 5px;
  border: 1px solid #333;
  background-color: #2d2d2d;
  color: #fff;
  border-radius: 5px;
  width: 200px;
}

select:disabled {
  background-color: #555;
}

/* 카드 컨테이너 */
.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.card {
  background-color: #2d2d2d;
  border: 1px solid #767676;
  border-radius: 10px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  margin: 10px;
  overflow: hidden;
  color: #fff;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: scale(1.05);
}

.card-header {
  background-color: #333;
  padding: 15px;
  text-align: center;
}

.card-body {
  padding: 15px;
}

.card-footer {
  background-color: #333;
  padding: 10px;
  text-align: center;
}

button {
  background-color: #0078D6;
  color: #fff;
  font-weight: 700;
  font-size: 16px;
  padding: 10px 30px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  text-align: center;
}

button:hover {
  background-color: #0056a0;
}
</style>
