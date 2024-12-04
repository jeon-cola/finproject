<template>
  <div class="create-post-page">
    <h1 class = 'title'>게시물 작성</h1>
    <form @submit.prevent="createPost">
      <input v-model="title" placeholder="제목" required />
      <textarea v-model="content" placeholder="내용" required></textarea>
      <button type="submit">작성</button>
      <button type="button" @click="$emit('close')">취소</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  emits: ['close', 'refresh'],
  setup(_, { emit }) {
    const title = ref('');
    const content = ref('');

    const createPost = async () => {
      console.log('보내는 데이터:', { title: title.value, content: content.value });

      try {
        await axios.post('http://localhost:8000/api/board/posts/', {
          title: title.value,
          content: content.value,
        }, {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`,
          },
        });
        alert('게시물이 작성되었습니다.');
        emit('refresh'); // 부모 컴포넌트에 새로고침 이벤트 전송
        emit('close');   // 모달 닫기 이벤트 전송
      } catch (error) {
        console.error('게시물 작성 오류:', error.response?.data || error.message);
        alert('게시물 작성 중 문제가 발생했습니다.');
      }
    };

    return {
      title,
      content,
      createPost,
    };
  },
};
</script>

<style scoped>
.create-post-page {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}
.title {
  color: #000000; /* 제목만 검은색 */
  font-size: 24px;
  margin-bottom: 20px;
}
input, textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
button {
  margin-right: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
