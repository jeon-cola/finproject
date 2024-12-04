<template>
  <div class="section">
    <!-- 배경 동영상 섹션 -->
    <div class="home-kv-video">
      <video autoplay muted loop class="video-background">
        <source src="@/assets/background.mp4" type="video/mp4" />
        <!-- 브라우저가 지원하지 않을 경우 -->
        Your browser does not support the video tag.
      </video>
      <div class="text-overlay">
        <h1>당신의 금융을 새롭게 정의하다</h1>
        <div>
          <div v-if="userStore.user">
            <button class="cta-button" @click="goDeposit">예금 상품 보기</button>  
            <button class="cta-button" @click="goSaving">적금 상품 보기</button>
          </div>
          <div v-else>
            <button class="cta-button" @click="goClick">로그인하기</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';
const router = useRouter()
const goDeposit = function(){
  router.push({name:'deposit'})
}
const goSaving = function(){
  router.push({name:'saving'})
}
const goClick = function(){
  router.push({name:'login'})
}
// Pinia 스토어를 컴포넌트 내부에서 호출
const userStore = useUserStore();
</script>

<style scoped>
.section {
  position: relative;
  width: 100%;
  height: 100vh;
  background-color: #000;
}

.home-kv-video {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.video-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.text-overlay {
  position: absolute;
  top: 30%;
  left: 5%;
  color: #fff;
  text-align: left;
}

.text-overlay h1 {
  font-family: 'Inter', sans-serif;
  font-size: 64px;
  line-height: 1.2;
  margin-bottom: 20px;
}

.text-overlay p {
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  margin-bottom: 30px;
}

.cta-button {
  background-color: #0078D6;
  border: 1px solid #0078D6;
  border-radius: 2px;
  padding: 12px 30px;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 30px;
  margin-right: 20px;
}

.cta-button:hover {
  background-color: #005bb5;
}
</style>
