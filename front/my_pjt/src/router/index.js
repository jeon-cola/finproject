import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import SavingView from '@/views/SavingView.vue';
import depositView from '@/views/depositView.vue';
import ExchangeRateView from '@/views/ExchangeRateView.vue';
import MapView from '@/views/MapView.vue';
import Login from '@/components/Login.vue';
import Posts from '@/components/Posts.vue';
import MyProfile from '@/components/MyProfile.vue';
import EditProfile from '@/components/EditProfile.vue';
import Signup from '@/components/Signup.vue';
import CreatePostModal from '@/components/CreatePostModal.vue';
import DetailView from '@/views/DetailView.vue';
import DetailSaving from '@/views/detailSaving.vue';
import AiView from '@/views/AiView.vue';
import MyProduct from '@/components/MyProduct.vue';
import { useUserStore } from '@/stores/user';
import CalculatingView from '@/views/CalculatingView.vue';



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/saving',
      name: 'saving',
      component: SavingView
    },
    {
      path: '/deposit',
      name: 'deposit',
      component: depositView
    },
    {
      path:'/exchange_rate',
      name:'exchange_rate',
      component:ExchangeRateView
    },
    {
      path:'/detail',
      name:'detail',
      component:DetailView,
      props:true},
      {
        path:'/detailsaving',
        name:'detailsaving',
        component:DetailSaving,
        props:true},
    {
      path:'/map',
      name:'map',
      component:MapView
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
    {
      path:'/posts',
      name:'posts',
      meta: { requiresAuth: true },
      component:Posts
    },
    {
      path:'/profile',
      name:'profile',
      meta: { requiresAuth: true },
      component:MyProfile
    },
    {
      path: '/profile/edit',
      name: 'editProfile',
      meta: { requiresAuth: true },
      component:EditProfile
    },
    {
      path: '/createPostModal',
      name: 'createPost',
      component:CreatePostModal
    },
    {
      path:'/ai',
      name:'ai',
      component:AiView
    },
    {
      path: '/myproduct',
      name: 'myproduct',
      component: MyProduct,
    },
    {
      path:'/calculating',
      name:'calculating',
      component:CalculatingView
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();

  // 인증 상태가 초기화되지 않은 경우 초기화
  if (!userStore.token) {
    await userStore.initializeAuth(); // 인증 상태 복원 시도
  }

  if (to.meta.requiresAuth && !userStore.token) {
    next({ name: 'login' });
  } else {
    next();
  }
});


export default router
