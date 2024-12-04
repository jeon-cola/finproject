<template>
  <div>
    <nav
      class="navbar navbar-expand-lg bg-body-tertiary"
      :class="{ visible: isNavbarVisible }"
    >
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Navbar</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <RouterLink :to="{ name: 'home' }" id="link">home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'saving' }" id="link">saving</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'deposit' }" id="link">deposit</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'exchange_rate' }" id="link">exchange_rate</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'map' }" id="link">map</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'posts' }" id="link">게시물</RouterLink>
            </li>
            <li class="nav-item" v-if="!isAuthenticated">
              <RouterLink :to="{ name: 'login' }" id="link">login</RouterLink>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <button
                @click="handleLogout"
                id="link"
                style="background: none; border: none; cursor: pointer;"
              >
                logout
              </button>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink :to="{ name: 'profile' }" id="link">나의 프로필</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div>
      <AiView v-if="showAiView" @close="closeAiView" />
    </div>

    <!-- 오른쪽 하단 버튼 -->
    <button class="ai-button" @click="openAiView">
      문의
    </button>

    <nav class="show">
      <router-view />
    </nav>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { computed, ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { useCounterStore } from "./stores/counter";
import AiView from "@/views/AiView.vue";

// 상태 관리
const store = useCounterStore();
const userStore = useUserStore();

// AI 창 열기/닫기 상태
const showAiView = ref(false);

// Navbar 표시 여부
const isNavbarVisible = ref(false);

// 로그인 상태 확인
const isAuthenticated = computed(() => userStore.token !== null);

// 로그아웃 처리 함수
const handleLogout = async () => {
  try {
    await userStore.logout();
    alert("로그아웃 성공");
  } catch (error) {
    console.error("로그아웃 실패:", error);
    alert("로그아웃 중 문제가 발생했습니다.");
  }
};

// AI 창 열기/닫기 함수
const openAiView = () => {
  showAiView.value = true;
};
const closeAiView = () => {
  showAiView.value = false;
};

// 마우스 이동 감지
const handleMouseOver = (event) => {
  if (event.clientY < 50) {
    isNavbarVisible.value = true;
  } else {
    isNavbarVisible.value = false;
  }
};

// 앱 초기화 시 이벤트 리스너 추가
onMounted(() => {
  document.addEventListener("mousemove", handleMouseOver);
  store.getDeposit();
  store.getSaving();
});
</script>

<style scoped>
#link {
  text-decoration: none;
  color: inherit;
  display: inline-block;
  margin-right: 10px;
}
/* Navbar 기본 스타일 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: black !important;
  color: white;
  z-index: 9999;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out, background 0.3s ease-in-out;
  transform: translateY(-100%); /* 기본적으로 숨김 */
}
.navbar.visible {
  transform: translateY(0); /* 표시 */
  background: rgba(0, 0, 0, 0.6); /* 배경 색상 추가 */
}
.navbar-brand {
  font-size: 20px;
  font-weight: bold;
  color: #ffffff;
}
.navbar-nav .nav-item {
  margin-right: 15px;
}
.navbar-nav .nav-item #link {
  color: #ffffff;
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background 0.3s, color 0.3s;
}
.navbar-nav .nav-item #link:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}
.navbar-nav .nav-item button {
  color: #ffffff;
  font-size: 16px;
  font-weight: 500;
  background: none;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
}
.navbar-nav .nav-item button:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}
.navbar-collapse {
  justify-content: flex-end;
}
body {
  padding-top: 60px;
}
.show {
  background-color: black;
  color: white;
}
.ai-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: rgba(93, 173, 226, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  font-size: 18px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  z-index: 1000;
}
.ai-button:hover {
  background-color: #0056b3;
}
</style>
