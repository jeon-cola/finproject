<!-- src/charts/ProductChart.vue -->
<template>
  <div>
    <h3>가입한 상품 금리 정보</h3>
    <canvas id="product-chart"></canvas>
  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js'

export default {
  props: ['products'],
  data() {
    return {
      chart: null,
    }
  },
  mounted() {
    this.fetchProductRates()
  },
  watch: {
    products() {
      this.fetchProductRates()
    },
  },
  methods: {
    fetchProductRates() {
      // 상품 금리 정보를 가져오는 API 호출 (예시)
      axios.get('/api/product-rates/', {
        params: {
          products: this.products,
        },
      })
        .then(response => {
          this.renderChart(response.data)
        })
        .catch(error => {
          console.error(error)
        })
    },
    renderChart(data) {
      if (this.chart) {
        this.chart.destroy()
      }
      const ctx = document.getElementById('product-chart').getContext('2d')
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.product_name),
          datasets: [{
            label: '금리 (%)',
            data: data.map(item => item.interest_rate),
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
          }],
        },
        options: {
          scales: {
            yAxes: [{
              ticks: { beginAtZero: true },
            }],
          },
        },
      })
    },
  },
}
</script>
