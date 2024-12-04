<template>
  <div class="chat-box">
    <div class="chat-header">
      <span>AI 도움말</span>
      <button class="close-button" @click="$emit('close')">X</button>
    </div>
    <div class="chat-content">
      <!-- 대화 내역 -->
      <div class="chat-history">
        <div
          v-for="(message, index) in chatHistory"
          :key="index"
          class="chat-message"
        >
          <p class="chat-user"><strong>사용자:</strong> {{ message.question }}</p>
          <p class="chat-ai">
            <strong>AI:</strong> {{ message.response }}
          </p>
        </div>
      </div>

      <!-- 질문 입력 -->
      <form @submit.prevent="askQuestion" class="chat-form">
        <input
          type="text"
          v-model="question"
          placeholder="질문을 입력하세요"
          class="chat-input"
        />
        <button type="submit" class="submit-button">전송</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

// Pinia 스토어
const counterStore = useCounterStore();
const filterData = counterStore.filterData; // 예금 데이터
const filterData2 = counterStore.filterData2; // 적금 데이터

// 상태 변수
const question = ref(""); // 사용자 질문
const chatHistory = ref([]); // 대화 내역
const isLoading = ref(false); // 로딩 상태

// 질문 처리 함수
const askQuestion = async () => {
  if (!question.value.trim()) {
    chatHistory.value.push({
      question: question.value,
      response: "질문을 입력해주세요!",
    });
    return;
  }

  // 대화 내역에 질문 추가
  chatHistory.value.push({
    question: question.value,
    response: "대답 생성 중...",
  });

  isLoading.value = true;

  try {
    // OpenAI API 호출
    const response = await axios.post("http://localhost:8000/fin/api/openai", {
      question: question.value,
      deposits: filterData,
      savings: filterData2,
    });

    // OpenAI의 응답으로 대화 내역 갱신
    chatHistory.value[chatHistory.value.length - 1].response =
      response.data.response;
  } catch (error) {
    console.error("OpenAI 호출 중 오류 발생:", error);
    chatHistory.value[chatHistory.value.length - 1].response =
      "추천 생성 중 오류가 발생했습니다.";
  } finally {
    isLoading.value = false;
    question.value = ""; // 입력 필드 초기화
  }
};

// 데이터 초기화
counterStore.send_deposit(); // 예금 데이터 가져오기
counterStore.send_saving(); // 적금 데이터 가져오기
</script>

<style scoped>
/* 동일한 스타일 */
.chat-box {
  position: fixed;
  bottom: 90px;
  right: 20px;
  width: 300px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 1001;
  display: flex;
  flex-direction: column;
}
.chat-header {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  display: flex;
  justify-content: space-between;
}
.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
}
.chat-content {
  padding: 10px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  max-height: 200px;
  margin-bottom: 10px;
  padding-right: 5px;
}
.chat-message {
  margin-bottom: 10px;
}
.chat-user {
  color: #000;
  margin: 0;
}
.chat-ai {
  color: #007bff;
  margin: 0;
}
.chat-form {
  display: flex;
  gap: 10px;
}
.chat-input {
  flex-grow: 1;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.submit-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
}
</style>
