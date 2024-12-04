import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';
import { useUserStore } from './stores/user';

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);

const userStore = useUserStore();

// 인증 초기화가 완료된 후 앱을 마운트
userStore.initializeAuth().then(() => {
  app.mount('#app');
});
