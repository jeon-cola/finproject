// src/stores/user.js
import { defineStore } from 'pinia';
import axios from 'axios';

import { ref } from 'vue'

export const useUserStore = defineStore('userStore', {
  state: () => ({
    token: null,
    user: null,
  }),

  actions: {
    async initializeAuth() {
      const token = localStorage.getItem('token');
      console.log('초기화 토큰:', token); // 토큰 확인용 로그
      if (token) {
        try {
          const response = await axios.get('http://localhost:8000/accounts/profile/', {
            headers: {
              Authorization: `Token ${token}`,
            },
          });
          this.token = token;
          this.user = response.data;
          axios.defaults.headers.common['Authorization'] = `Token ${token}`;
          console.log('인증 초기화 성공:', this.user); // 성공 시 사용자 정보 로그
        } catch (error) {
          console.error('토큰 검증 실패:', error);
          this.clearAuth();
        }
      } else {
        console.log('토큰이 없습니다.');
      }
    },    

    clearAuth() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      delete axios.defaults.headers.common['Authorization'];
    },

    async signup(payload) {
      try {
        console.log(1)
        const response = await axios.post('http://localhost:8000/accounts/signup/', payload);
        console.log('회원가입 성공:', response.data);
        return response.data;
      } catch (error) {
        console.error('회원가입 오류:', error);
        throw error;
      }
    },

    async login(username, password) {
      try {
        const response = await axios.post('http://localhost:8000/accounts/login/', {
          username,
          password,
        });
        this.token = response.data.token;
        localStorage.setItem('token', this.token);
        axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;
        await this.fetchUser();
      } catch (error) {
        console.error('로그인 오류:', error);
        throw error;
      }
    },

    async fetchUser() {
      try {
        const response = await axios.get('http://localhost:8000/accounts/profile/');
        console.log(response.data)
        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(this.user));
        console.log('사용자 정보 가져오기 성공:', this.user);
      } catch (error) {
        console.error('사용자 정보 가져오기 오류:', error);
      }
    },

    async logout() {
      try {
        if (!this.token) throw new Error('로그인 상태가 아닙니다.');
        await axios.post('http://localhost:8000/accounts/logout/', null, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
      } catch (error) {
        console.warn('로그아웃 요청 실패:', error);
      } finally {
        this.clearAuth();
        window.location.reload();
      }
    },

    async updateProfile(payload) {
      try {
        const response = await axios.put('http://localhost:8000/accounts/profile/', payload, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        console.log(response.data)
        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(this.user));
        console.log('프로필 수정 성공:', this.user);
        return response.data;
      } catch (error) {
        console.error('프로필 수정 오류:', error);
        throw error;
      }
    },
  },
});
