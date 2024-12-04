<script setup>
import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps';
import { ref, onMounted,computed } from 'vue';
import { useKakao } from 'vue3-kakao-maps';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';
const store = useCounterStore();
const router = useRouter()
// 카카오 API 키 설정
const showCalculator = ref(false); // 계산기 패널 보임 여부
const showCalculatored = computed(showCalculator)
const targetAmount = ref(0); // 목표 금액
const interestRate = ref(0); // 금리 (%)
const currentAmount = ref(0); // 현재 보유 금액
const months = ref(0); // 기간 (개월)
const monthlyPayment = ref(null); // 매달 필요한 저축 금액

// 계산기 패널 보이기/숨기기
const toggleCalculator = () => {
  showCalculator.value = !showCalculator.value;
};

// 월 납입 금액 계산
const calculateMonthlyPayment = () => {
  if (months.value <= 0) {
    alert('기간은 1개월 이상이어야 합니다.');
    return;
  }

  const principalNeeded = targetAmount.value - currentAmount.value;
  if (principalNeeded <= 0) {
    alert('목표 금액이 이미 보유한 금액 이하입니다.');
    monthlyPayment.value = 0;
    return;
  }

  const ratePerMonth = interestRate.value / 100 / 12;
  if (ratePerMonth === 0) {
    // 이자가 없는 경우
    monthlyPayment.value = principalNeeded / months.value;
  } else {
    // 복리 계산 공식 사용
    monthlyPayment.value = principalNeeded * ratePerMonth / (1 - Math.pow(1 + ratePerMonth, -months.value));
  }
};
const kakaoApiKey = import.meta.env.VITE_APP_API_KEY;
console.log(import.meta.env)
useKakao(kakaoApiKey, ['services']);
const onPlaceNameClick = function(){
  router.push({name:'calculating'})
}
const map = ref(null);
const markerList = ref([]);
const searchKeyword = ref('');
const roadAddress=ref(null)
// 현재 위치 좌표 저장
const currentLocation = ref({ lat: 37.566826, lng: 126.9786567 }); // 기본값: 서울
// 현재 위치를 검색하고 지도 중심 설정
const searchCurrentLocation = () => {
  if (!navigator.geolocation) {
    alert('현재 위치를 검색할 수 없습니다.');
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      currentLocation.value = { lat, lng };

      if (map.value) {
        const center = new kakao.maps.LatLng(lat, lng);
        map.value.setCenter(center); // 지도 중심 설정
        map.value.setLevel(3); // 확대 수준 설정
        setTimeout(() => searchNearbyBanks(), 500); // 은행 검색 호출
      }
    },
    (error) => {
      console.error('현재 위치를 가져오지 못했습니다.', error);
      alert('현재 위치를 가져오지 못했습니다.');
    }
  );
};

// 맵 로드 후 초기 설정
const onLoadKakaoMap = (mapRef) => {
  map.value = mapRef;
  setTimeout(() => {
    map.value.relayout(); // 레이아웃 갱신
  }, 100);
  searchNearbyBanks(); // 근처 은행 검색
};

// 키워드 검색
const onSearch = async () => {
  if (searchKeyword.value.trim() === '') {
    alert('검색어를 입력하세요.');
    return;
  }

  // 장소 검색 실행
  searchPlaces(searchKeyword.value);

  const ps2 = new kakao.maps.services.Places();

  // Promise로 keywordSearch 감싸기
  const getKeywordSearchResult = (keyword) => {
    return new Promise((resolve, reject) => {
      ps2.keywordSearch(keyword, (data, status) => {
        if (status === kakao.maps.services.Status.OK && data.length > 0) {
          resolve(data[0].road_address_name);
        } else {
          reject(new Error('검색 실패 또는 결과 없음'));
        }
      });
    });
  };

  try {
    // 검색 결과를 가져오기 위해 await 사용
    const roadAddressResult = await getKeywordSearchResult(searchKeyword.value);
    roadAddress.value = roadAddressResult;

    // 법정동 ID 가져오기
    getLegalDongId(roadAddress.value);
  } catch (error) {
    console.error('도로명 주소를 가져오는 데 실패했습니다:', error);
  }
};

// 키워드로 장소 검색
const searchPlaces = (keyword) => {
  if (!window.kakao || !window.kakao.maps) {
    console.error('카카오 맵 서비스가 아직 로드되지 않았습니다.');
    return;
  }

  const ps = new kakao.maps.services.Places();
  ps.keywordSearch(keyword, placesSearchCB);
};

// 근처 은행 검색
const searchNearbyBanks = () => {
  if (!window.kakao || !window.kakao.maps || !kakao.maps.services.Places) {
    console.error('카카오 맵 서비스가 로드되지 않았습니다.');
    return;
  }

  const ps = new kakao.maps.services.Places();
  const center = map.value.getCenter();
  ps.keywordSearch('은행', placesSearchCB, {
    location: new kakao.maps.LatLng(center.getLat(), center.getLng()),
    radius: 5000,
  });
};

// 장소 검색 콜백
const placesSearchCB = (data, status) => {
  if (status === kakao.maps.services.Status.OK && data.length > 0) {
    const bounds = new kakao.maps.LatLngBounds();

    markerList.value = data.map((place) => {
      bounds.extend(new kakao.maps.LatLng(Number(place.y), Number(place.x)));
      return {
        key: place.id,
        name: place.place_name,
        address: place.road_address_name || place.address_name, // 도로명 주소 우선
        phone: place.phone || '전화번호 없음',
        category: place.category_group_name || '카테고리 없음',
        lat: Number(place.y),
        lng: Number(place.x),
        infoWindow: {
          content: `
            <div class="info-window" style="
              background-color: #ffffff; 
              color: #333333;
              padding: 15px;
              border-radius: 12px;
              font-size: 14px;
              max-width: 280px;
              text-align: left;
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
              border: 2px solid #3498db;">
              <div style="border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 10px;">
                <strong 
                  style="color: #3498db; font-size: 16px; cursor: pointer;" 
                  @click="onPlaceNameClick('${place}')">
                  ${place.place_name}
                </strong>
              </div>
              <div style="margin-bottom: 5px;">
                <span style="font-weight: bold;">주소:</span> ${place.road_address_name || place.address_name}
              </div>
              <div style="margin-bottom: 5px;">
                <span style="font-weight: bold;">전화:</span> ${place.phone || '전화번호 없음'}
              </div>
              <div>
                <span style="font-weight: bold;">카카오 페이지:</span> 
                ${place.place_url ? `<a href="${place.place_url}" target="_blank" rel="noopener noreferrer">${place.place_url}</a>` : '카카오 페이지 없음'}
              </div>
            </div>
          `,
          visible: false,
        },
      };
    });

    map.value?.setBounds(bounds); // 검색 결과에 맞게 지도 범위 설정
  } else {
    alert('검색 결과가 없습니다.');
    console.error('검색 결과가 없습니다.', status);
  }
};

// 마커 클릭 이벤트
const onClickMapMarker = (markerItem) => {
  markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
};
const onClickMapMarker2 = (markerItem) => {
  // 마커 클릭 시 해당 마커의 infoWindow 표시 상태를 반전
  markerItem.infoWindow.visible = !markerItem.infoWindow.visible;

  // infoWindow가 보이는 상태일 때만 이벤트 리스너 추가
  if (markerItem.infoWindow.visible) {
    // setTimeout을 사용해서 infoWindow가 DOM에 렌더링될 시간을 줍니다.
    setTimeout(() => {
      const infoWindowElement = document.querySelector(`.info-window[data-id="${markerItem.key}"] .place-name`);

      if (infoWindowElement) {
        // 이벤트 리스너 추가
        infoWindowElement.addEventListener('click', () => {
          onPlaceNameClick(markerItem);
        });
      }
    }, 0);
  }
};

// 리스트에서 은행 클릭 시 지도 중심 이동 및 마커 정보창 표시
const moveToBank = (bank) => {
  if (map.value) {
    const center = new kakao.maps.LatLng(bank.lat, bank.lng);
    map.value.setCenter(center); // 지도 중심 이동

    // 마커 리스트에서 해당 마커의 정보를 업데이트해서 정보창을 열기
    markerList.value.forEach((marker) => {
      if (marker.key === bank.key) {
        marker.infoWindow.visible = true;
      } else {
        marker.infoWindow.visible = false; // 다른 마커 정보창은 닫기
      }
    });
  }
};

// 법정동 ID 가져오기 함수 수정 - 가져온 데이터에 맞는 마커 추가
const getLegalDongId = async (address) => {
  const geocoder = new kakao.maps.services.Geocoder();
  
  // addressSearch를 Promise로 변환
  const getAddressPromise = (address) => {
    return new Promise((resolve, reject) => {
      geocoder.addressSearch(address, (result, status) => {
        if (status === kakao.maps.services.Status.OK && result.length > 0) {
          const legalDongId = result[0].address.b_code;
          resolve(legalDongId);
        } else {
          reject(new Error('주소 검색 실패'));
        }
      });
    });
  };

  try {
    // 주소 검색 결과를 기다림
    const legalDongId = await getAddressPromise(address);
    console.log('전달할 법정동 코드:', legalDongId);
    
    // legalDong이 비동기 함수라면 await 추가
    await store.legalDong(legalDongId);

    // 이후 legalList의 데이터를 활용한 추가 로직 실행
    store.legalList.forEach((i) => {
      const keyword = `${i.umdNm} ${i.aptNm} 아파트`;
      const ps = new kakao.maps.services.Places();
      
      // keywordSearch 호출 시, keyword와 콜백 함수로 검색 진행
      ps.keywordSearch(keyword, (data, status) => {
        placesSearchCB2(data, status, i); // 추가 정보를 함께 전달
      });
    });

  } catch (error) {
    console.error('법정동 ID를 가져오는 데 실패했습니다:', error);
  }
};
const markerList2 = ref([]);
// 법정동 검색 콜백
const placesSearchCB2 = (data, status, aptInfo) => {
  console.log('확인',data,status,aptInfo)
  if (status === kakao.maps.services.Status.OK && data.length > 0) {
    const bounds = new kakao.maps.LatLngBounds();

    data.forEach((place) => {
      bounds.extend(new kakao.maps.LatLng(Number(place.y), Number(place.x)));

      markerList2.value.push({
        key: place.id,
        name: place.place_name,
        address: place.road_address_name || place.address_name, // 도로명 주소 우선
        lat: Number(place.y),
        lng: Number(place.x),
        infoWindow: {
          content: `
            <div class="info-window" style="
              background-color: #ffffff; 
              color: #333333;
              padding: 15px;
              border-radius: 12px;
              font-size: 14px;
              max-width: 280px;
              text-align: left;
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
              border: 2px solid #3498db;">
              <div style="border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 10px;">
                <strong style="color: #3498db; font-size: 16px;">${place.place_name}</strong>
              </div>
              <div style="margin-bottom: 5px;">
                <span style="font-weight: bold;">주소:</span> ${place.road_address_name || place.address_name}
              </div>
              <div style="margin-bottom: 5px;">
                <span style="font-weight: bold;">매매가:</span> ${aptInfo.dealAmount || '거래내역 없음'}만원
              </div>
              <div style="margin-bottom: 5px;">
                <span style="font-weight: bold;">매매일:</span> ${aptInfo.dealYear}년 ${aptInfo.dealMonth}월 ${aptInfo.dealDay}일
              </div>
              <div style="margin-bottom: 5px;">
                <span style="font-weight: bold;">평수:</span> ${aptInfo.excluUseAr}(㎡)
              </div>
              <div style="margin-bottom: 5px;">
                <span style="font-weight: bold;">층수:</span> ${aptInfo.floor || '데이터 없음'}층
              </div>
            </div>
          `,
          visible: false,
        },
      });
    });

    // map.value?.setBounds(bounds); // 검색 결과에 맞게 지도 범위 설정
  } else {
    console.error('법정동 검색 결과가 없습니다.', status);
  }
};

</script>

<template>
  <div class="map-container">
    <!-- 은행 리스트 -->
    <div class="bank-list">
      <div
        v-for="bank in markerList"
        :key="bank.key"
        class="bank-item"
        @click="moveToBank(bank)"
      >
        <h4>{{ bank.name }}</h4>
        <p>{{ bank.address }}</p>
        <p>{{ bank.phone }}</p>
        <p>{{ bank.category }}</p>
      </div>
    </div>

    <!-- 검색 기능 -->
    <div class="search-container">
      <div class="search-bar">
        <input
          v-model="searchKeyword"
          placeholder="검색어를 입력하세요"
        />
        <button @click="onSearch">검색</button>
        <button @click="searchNearbyBanks">근처 은행</button>
        <button @click="searchCurrentLocation">현재 위치</button>
      </div>
    </div>

    <!-- 계산하기 버튼 -->
    <div class="calculating">
      <button class="calc-btn" @click="toggleCalculator">계산하기</button>
    </div>

    <!-- 계산기 패널: 버튼 누를 때만 보이도록 설정 -->
    <div class="calculator-panel" v-show="showCalculator">
      <h3>목표 금액 계산기</h3>
      <label>목표 금액 (₩):
        <input type="number" v-model.number="targetAmount" />
      </label>
      <label>금리 (%):
        <input type="number" v-model.number="interestRate" />
      </label>
      <label>현재 보유 금액 (₩):
        <input type="number" v-model.number="currentAmount" />
      </label>
      <label>기간 (개월):
        <input type="number" v-model.number="months" />
      </label>
      <button @click="calculateMonthlyPayment">계산</button>
      <div v-if="monthlyPayment !== null">
        <p style="color: black;">매달 필요한 저축 금액: {{ monthlyPayment.toLocaleString() }} 원</p>
      </div>
    </div>

    <!-- 카카오 맵 -->
    <KakaoMap
      class="kakao-map"
      :lat="currentLocation.lat"
      :lng="currentLocation.lng"
      style="width: 100%; height: 100%;"
      @onLoadKakaoMap="onLoadKakaoMap"
    >
      <KakaoMapMarker
        class="blue"
        v-for="marker in markerList"
        :key="marker.key"
        :lat="marker.lat"
        :lng="marker.lng"
        :infoWindow="marker.infoWindow"
        :clickable="true"
        @onClickKakaoMapMarker="() => onClickMapMarker(marker)"
      />
      <KakaoMapMarker
        class="red"
        v-for="marker in markerList2"
        :key="marker.key"
        :lat="marker.lat"
        :lng="marker.lng"
        :image="{
          imageSrc: 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
          imageWidth: 64,
          imageHeight: 64,
          imageOption: {}
        }"
        :infoWindow="marker.infoWindow"
        :clickable="true"
        @onClickKakaoMapMarker="() => onClickMapMarker2(marker)"
      />
    </KakaoMap>
  </div>
</template>


<style scoped>
.map-container {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.kakao-map {
  width: 100%;
  height: 100%;
}

.bank-list {
  color: black;
  position: absolute;
  left: 10px;
  top: 50px;
  z-index: 1000;
  width: 250px;
  max-height: 400px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  overflow-y: auto;
  padding: 10px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.bank-item {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  font-size: 14px;
}

.bank-item:last-child {
  border-bottom: none;
}

.bank-item:hover {
  background: #f0f8ff;
  color: #3498db;
}

.calculator-panel {
  position: absolute;
  z-index: 1100;
  top: 120px;
  right: 20px;
  background: #ffffff;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  width: 300px;
}

.calculator-panel h3 {
  color: #333333;
  margin-bottom: 15px;
}

.calculator-panel label {
  display: block;
  margin-bottom: 10px;
  color: #333333;
}

.calculator-panel input {
  width: calc(100% - 10px);
  padding: 8px;
  margin-top: 5px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.calculator-panel button {
  margin-top: 15px;
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.calculator-panel button:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.calculating {
  position: absolute;
  z-index: 1000;
  top: 50px;
  right: 5px;
  padding: 15px;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.calc-btn {
  background: #3498db;
  color: #ffffff;
  border: none;
  padding: 12px 25px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.calc-btn:hover {
  background: #2980b9;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.calc-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.search-container {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  padding: 20px 25px;
  border-radius: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  margin-top: 30px;
}

.search-bar {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-bar input {
  flex: 1;
  padding: 12px 15px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 25px;
  outline: none;
}

.search-bar button {
  padding: 12px 20px;
  font-size: 14px;
  color: white;
  background-color: #5dade2;
  border: none;
  border-radius: 25px;
  cursor: pointer;
}

.search-bar button:hover {
  background-color: #3498db;
  transform: scale(1.05);
}
</style>
