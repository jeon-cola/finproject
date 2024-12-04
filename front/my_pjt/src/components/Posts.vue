<template>
  <div class="board-container">
    <h1 class="main-title">게시물 목록</h1>

    <!-- 게시물 작성 버튼 -->
    <button class="create-post-button" v-if="isAuthenticated" @click="openCreateModal">
      게시물 작성
    </button>

    <!-- 작성 모달 -->
    <CreatePostModal
      v-if="showCreateModal"
      @close="closeCreateModal"
      @refresh="fetchPosts"
    />

    <!-- 게시물 목록 -->
    <div v-if="posts.length === 0" class="no-posts">
      <p>게시물이 없습니다.</p>
    </div>

    <div v-for="post in posts" :key="post.id" class="post-card">
      <div class="post-header">
        <h2>{{ post.title }}</h2>
        <p>작성자: {{ post.author_nickname }}</p>
        <p>작성일: {{ new Date(post.created_at).toLocaleString() }}</p>
      </div>
      <div class="post-body">
        <p>{{ post.content }}</p>
      </div>

      <!-- 삭제 버튼 -->
      <button
        class="delete-post-button"
        v-if="isAuthenticated && isAuthor(post)"
        @click="deletePost(post.id)"
      >
        게시물 삭제
      </button>

      <!-- 댓글 목록 -->
      <div class="comments">
        <h3>댓글</h3>
        <div v-for="comment in post.comments" :key="comment.id" class="comment">
          <p>{{ comment.content }}</p>
          <p>작성자: {{ comment.author_nickname }}</p>
          <p>작성일: {{ new Date(comment.created_at).toLocaleString() }}</p>
          <!-- 댓글 삭제 버튼 -->
          <button
            class="delete-comment-button"
            v-if="isAuthenticated && isAuthor(comment)"
            @click="deleteComment(comment.id)"
          >
            댓글 삭제
          </button>
        </div>
      </div>

      <!-- 댓글 작성 -->
      <div v-if="isAuthenticated" class="comment-form">
        <textarea v-model="newComments[post.id]" placeholder="댓글을 입력하세요..."></textarea>
        <button class="add-comment-button" @click="addComment(post.id)">댓글 작성</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import CreatePostModal from './CreatePostModal.vue';

export default {
  components: { CreatePostModal },
  setup() {
    const posts = ref([]);
    const newComments = ref({});
    const showCreateModal = ref(false);
    const userStore = useUserStore();

    const isAuthenticated = ref(false);
    if (userStore.token) {
      isAuthenticated.value = true;
    }

    const fetchPosts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/board/posts/');
        posts.value = response.data;
      } catch (error) {
        console.error('게시물을 가져오는 중 오류 발생:', error);
      }
    };

    const openCreateModal = () => {
      showCreateModal.value = true;
    };

    const closeCreateModal = () => {
      showCreateModal.value = false;
    };

    const addComment = async (postId) => {
      try {
        await axios.post(
          'http://localhost:8000/api/board/comments/',
          { post: postId, content: newComments.value[postId] },
          { headers: { Authorization: `Token ${userStore.token}` } }
        );
        newComments.value[postId] = '';
        fetchPosts();
      } catch (error) {
        console.error('댓글 작성 오류:', error);
      }
    };

    const deletePost = async (postId) => {
      try {
        await axios.delete(`http://localhost:8000/api/board/posts/${postId}/`, {
          headers: { Authorization: `Token ${userStore.token}` },
        });
        fetchPosts();
        alert('게시물이 삭제되었습니다.');
      } catch (error) {
        console.error('게시물 삭제 오류:', error);
      }
    };

    const deleteComment = async (commentId) => {
      try {
        await axios.delete(`http://localhost:8000/api/board/comments/${commentId}/`, {
          headers: { Authorization: `Token ${userStore.token}` },
        });
        fetchPosts();
        alert('댓글이 삭제되었습니다.');
      } catch (error) {
        console.error('댓글 삭제 오류:', error);
      }
    };

    const isAuthor = (item) => item.author === userStore.user.id;

    onMounted(() => {
      fetchPosts();
    });

    return {
      posts,
      newComments,
      showCreateModal,
      isAuthenticated,
      fetchPosts,
      openCreateModal,
      closeCreateModal,
      addComment,
      deletePost,
      deleteComment,
      isAuthor,
    };
  },
};
</script>

<style scoped>
html, body {
  height: 100%; /* 화면 전체를 커버 */
  margin: 0;
  background-color:#2563eb;
}

.board-container {
  background-color: #0f172a; /* 다크 블루 배경 */
  color: #f8fafc; /* 밝은 텍스트 */
  padding: 20px;
  min-height: 100vh;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.main-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #e2e8f0;
  margin-top: 50px;
}

.create-post-button {
  display: block;
  margin: 0 auto 20px;
  padding: 10px 20px;
  font-size: 1rem;
  color: #f8fafc;
  background: #2563eb; /* 고급스러운 블루 */
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.create-post-button:hover {
  background: #1d4ed8; /* 더 어두운 블루 */
}

.post-card {
  background-color: #1e293b; /* 카드 배경 어두운 네이비 */
  color: #f8fafc; /* 텍스트 밝게 */
  margin: 20px auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.6);
  width: 1000px;
}

.post-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #93c5fd; /* 밝은 블루로 강조 */
}

.post-body p {
  font-size: 1rem;
  line-height: 1.5;
}

button {
  padding: 10px 20px;
  font-size: 1rem;
  color: #f8fafc;
  background-color: #d97706; /* 오렌지 버튼 */
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background-color: #b45309; /* 어두운 오렌지 */
}

.comments {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #64748b;
}

.comment {
  background-color: #334155; /* 어두운 블루 */
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  color: #e2e8f0;
}

.comment-form textarea {
  width: 100%;
  background-color: #1e293b;
  color: #f8fafc;
  border: 1px solid #475569;
  border-radius: 8px;
  padding: 10px;
  margin-top: 10px;
}

.comment-form button {
  margin-top: 10px;
  background-color: #10b981; /* 밝은 그린 */
}

.comment-form button:hover {
  background-color: #059669; /* 더 어두운 그린 */
}

.no-posts {
  text-align: center;
  color: #64748b;
  font-size: 1.2rem;
}
</style>
