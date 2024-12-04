import { ref, computed, resolveComponent } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios'; 
import { useUserStore } from './user';


export const useCounterStore = defineStore('counter', () => {

  const exchangeRateList=ref([])
  const filterData = ref(JSON.parse(localStorage.getItem('filterData')) || []);
  const filterData2 = ref(JSON.parse(localStorage.getItem('filterData2')) || []);
  const usertore = useUserStore()
  const result = ref(([]))
  const goToDetail = function(lst){
    result.value=lst
  }
  const result2 = ref(([]))
  const goToDetail2 = function(lst){
    result2.value=lst
  }
  const saveSaving = function(){
    console.log(usertore.token);
    axios.post('http://localhost:8000/fin/saveSaving/', result2.value, {
      withCredentials: true
    }, {
      headers: {
        Authorization: `Token ${usertore.token}` // CSRF 토큰 추가
      },
    })
    .then(async (response) => {
      window.alert(response.data.message);
      console.log(response);
      // 저장 후 최신 데이터를 다시 불러오기
      await send_saving();
    })
    .catch((error) => {
      console.log(error);
    });
  }
  const saveDeposit = function(){
    console.log(usertore.token);
    console.log('data', result.value);
    axios.post('http://localhost:8000/fin/saveDeposit/', result.value, {
      withCredentials: true
    }, {
      headers: {
        Authorization: `Token ${usertore.token}` // CSRF 토큰 추가
      },
    })
    .then(async (response) => {
      window.alert(response.data.message);
      console.log(response);
      // 저장 후 최신 데이터를 다시 불러오기
      await send_deposit();
    })
    .catch((error) => {
      console.log(error);
    });
  }
  const send_deposit = function() {
    axios.get('http://localhost:8000/fin/send_deposit/')
    .then((response) => {
      filterData.value = response.data;
      localStorage.setItem('filterData', JSON.stringify(filterData.value));
      console.log('예금 데이터 성공적으로 불러옴');
    })
    .catch((error) => {
      console.error('예금 데이터 불러오기 실패:', error);
    });
  };
  
  const send_saving = function() {
    axios.get('http://localhost:8000/fin/send_saving/')
    .then((response) => {
      filterData2.value = response.data;
      localStorage.setItem('filterData2', JSON.stringify(filterData2.value));
      console.log('적금 데이터 성공적으로 불러옴');
    })
    .catch((error) => {
      console.error('적금 데이터 불러오기 실패:', error);
    });
  };
  
  const getSaving = function() {
    axios.get('http://localhost:8000/fin/saving/')
    .then((response) => {
      console.log('적금 데이터', response.data)
    })
    .catch((error) => {
      console.error('에러 발생:', error.message);
    });
  };
  const getDeposit = function() {
    axios.get('http://localhost:8000/fin/deposit/')
    .then((response) => {
      console.log('예금 데이터',response.data)
    })
    .catch((error) => {
      console.error('에러 발생:', error.message);
    });
    
  };
  const getExchangeRate = function() {
    axios.get('http://localhost:8000/fin/exchange_rate/')
    .then((response) => {
      console.log('응답 데이터:', response.data),
      exchangeRateList.value=response.data
    })
    .catch((error) => {
      console.error('에러 발생:', error.message);
    });
  };
  const deleteDeposit = function(deposit){
    axios.post('http://localhost:8000/fin/deleteDeposit/', deposit, {
      withCredentials: true
    },{headers: {
      Authorization: `Token ${usertore.token}` // CSRF 토큰 추가
    },})
    .then((response)=>{
      window.alert(response.data.message)
      console.log(response)
    })
    .catch((error)=>{
      console.log(error)
    })
  }
  const deleteSaving = function(saving){
    axios.post('http://localhost:8000/fin/deleteSaving/', saving, {
      withCredentials: true
    },{headers: {
      Authorization: `Token ${usertore.token}` // CSRF 토큰 추가
    },})
    .then((response)=>{
      window.alert(response.data.message)
      console.log(response)
    })
    .catch((error)=>{
      console.log(error)
    })
    // 법정동 id 받아서 매매가격 보내주는 axios 로직
  }
  const legalList = ref([]);

const legalDong = async function(ID) {
  console.log("전달할 법정동 코드:", ID);
  
  try {
    const response = await axios.get('http://localhost:8000/fin/legaldong/', {
      params: { lawd_cd: ID } // 'lawd_cd' 파라미터를 전달
    });

    // 응답 데이터에서 필요한 정보를 legalList에 설정
    legalList.value = response.data.flatMap((element) =>
      element.response?.body?.items?.item || [] // 데이터가 없으면 빈 배열 반환
    );

    console.log("응답 데이터:", legalList.value);
  } catch (error) {
    console.log("오류 발생:", error);
  }
};
  return { 
    deleteDeposit,
    deleteSaving,
    getDeposit,getSaving,
    exchangeRateList,
    getExchangeRate,
    filterData,
    filterData2,
    goToDetail,
    result,
    send_deposit,
    send_saving, 
    goToDetail2,
    result2,
    saveSaving,
    saveDeposit,
    legalDong,
    legalList,
  };
});


