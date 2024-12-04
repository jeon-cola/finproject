<template>
  <div class="profile-container">
    <h1 class="main-title">나의 상품 정보</h1>

    <div class="chart-container">
      <h2>저축 금리 및 우대금리 비교</h2>
      <canvas id="interestRateChart"></canvas>
    </div>

    <div class="products-container">
      <div class="card">
        <h2>적금 상품</h2>
        <div v-if="savingData.length > 0">
          <div v-for="save in savingData" :key="save.id" class="saving-item">
            <p><strong>은행:</strong> {{ save.kor_co_nm }}</p>
            <p><strong>이름:</strong> {{ save.fin_prdt_nm }}</p>
            <p><strong>저축 금리:</strong> {{ save.intr_rate }}%</p>
            <p><strong>최고 우대금리:</strong> {{ save.intr_rate2 }}%</p>
            <button class="delete-button" @click="deleteSaving(save)">삭제</button>
            <hr />
          </div>
        </div>
        <div v-else>
          <p>저장된 적금 상품이 없습니다.</p>
        </div>
      </div>

      <div class="card">
        <h2>예금 상품</h2>
        <div v-if="depositData.length > 0">
          <div v-for="save in depositData" :key="save.id" class="deposit-item">
            <p><strong>은행:</strong> {{ save.kor_co_nm }}</p>
            <p><strong>이름:</strong> {{ save.fin_prdt_nm }}</p>
            <p><strong>금리:</strong> {{ save.intr_rate }}%</p>
            <p><strong>우대금리:</strong> {{ save.intr_rate2 }}%</p>
            <button class="delete-button" @click="deleteDeposit(save)">삭제</button>
            <hr />
          </div>
        </div>
        <div v-else>
          <p>저장된 예금 상품이 없습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import Chart from 'chart.js/auto';

export default {
  setup() {
    const userStore = useUserStore();
    const user = computed(() => userStore.user);
    const router = useRouter();
    const store = useCounterStore();
    const savingData = ref([]);
    const depositData = ref([]);
    const chartInstance = ref(null);

    const deleteDeposit = (deposit) => {
      store.deleteDeposit(deposit);
      depositData.value = depositData.value.filter((item) => item.id !== deposit.id);
      renderChart();
    };

    const deleteSaving = (saving) => {
      store.deleteSaving(saving);
      savingData.value = savingData.value.filter((item) => item.id !== saving.id);
      renderChart();
    };

    const renderChart = () => {
      const ctx = document.getElementById('interestRateChart').getContext('2d');
      // 기존 그래프 제거
      if (chartInstance.value) {
        chartInstance.value.destroy();
      }

      // 적금과 예금 데이터를 결합
      const labels = [
        ...savingData.value.map((item) => `${item.fin_prdt_nm} (적금)`),
        ...depositData.value.map((item) => `${item.fin_prdt_nm} (예금)`),
      ];
      const baseRates = [
        ...savingData.value.map((item) => parseFloat(item.intr_rate)),
        ...depositData.value.map((item) => parseFloat(item.intr_rate)),
      ];
      const preferentialRates = [
        ...savingData.value.map((item) => parseFloat(item.intr_rate2)),
        ...depositData.value.map((item) => parseFloat(item.intr_rate2)),
      ];

      // 새로운 그래프 생성
      chartInstance.value = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: '기본 금리',
              data: baseRates,
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
            {
              label: '최고 우대금리',
              data: preferentialRates,
              backgroundColor: 'rgba(153, 102, 255, 0.6)',
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
          },
        },
      });
    };

    onMounted(async () => {
      try {
        await userStore.fetchUser();
        await store.send_saving();
        await store.send_deposit();
        savingData.value = store.filterData2.filter((item) =>
          user.value.saving.includes(item.id)
        );
        depositData.value = store.filterData.filter((item) =>
          user.value.deposit.includes(item.id)
        );
        renderChart();
      } catch (error) {
        console.error('데이터 로드 중 오류 발생:', error);
      }
    });

    return {
      user,
      savingData,
      depositData,
      deleteDeposit,
      deleteSaving,
    };
  },
};
</script>

<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background-color: #0f172a;
  color: #f8fafc;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.main-title {
  font-size: 2rem;
  margin-bottom: 30px;
  color: #93c5fd;
  text-align: center;
  margin-top: 50px;
}

.chart-container {
  width: 40%;
  background-color: #1e293b;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
  margin-bottom: 30px;
  
}

.products-container {
  display: flex;
  gap: 20px;
}

.card {
  background-color: #1e293b;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
  width: 400px;
  color: #f8fafc;
}

.delete-button {
  padding: 10px;
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-button:hover {
  background-color: #b91c1c;
}
</style>