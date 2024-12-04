from django.shortcuts import render
# views.py
import requests
from django.http import JsonResponse
from .models import DepositModel,SavingModel
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import openai
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import xmltodict

API_KEY = config('API_KEY')
EXCHANGE_KEY = config('EXCHANGE_KEY')
DATAKEY=config('DATAKEY')
openai.api_key = config('AIKEY')

def get_saving(request):
    url = 'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
        'changeOrigin': True,
    }
    data=[]
    response = requests.get(url, params=params)
    data.append(response.json().get('result'))
    result=response.json()
    save_saving(result) 
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '030300',
        'changeOrigin': True,
    }
    for i in range(1,4):
        params['pageNo'] = i
        response = requests.get(url, params=params)
        data.append(response.json().get('result'))
        result=response.json()
        save_saving(result) 
    return JsonResponse(data,safe=False)


def get_deposit(request):
    url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
        'changeOrigin': True,
    }
    data=[]
    response = requests.get(url, params=params)
    data.append(response.json().get('result'))
    result=response.json()
    save_deposit(result)     

    params = {
        'auth': API_KEY,
        'topFinGrpNo': '030300',
        'changeOrigin': True,
    }
    for i in range(1,5):
        params['pageNo'] = i
        response = requests.get(url, params=params)
        result=response.json()
        save_deposit(result)    
        data.append(response.json()['result'])
    return JsonResponse(data,safe=False)

def send_deposit(request):
     d=DepositModel.objects.all()
     lst = [
    {
         'id':i.id,
        "kor_co_nm": i.kor_co_nm,
        "fin_prdt_nm": i.fin_prdt_nm,
        "join_way": i.join_way,
        "mtrt_int": i.mtrt_int,
        "spcl_cnd": i.spcl_cnd,
        "etc_note": i.etc_note,
        "intr_rate": i.intr_rate,
        "intr_rate2": i.intr_rate2,
        "intr_rate_type_nm": i.intr_rate_type_nm,
        "save_trm": i.save_trm,
    }
    for i in d
]
     return JsonResponse(lst,safe=False)
    
def save_deposit(data):
    # for result in data:  # data는 리스트이므로 각 요소를 순회
        baseList = data.get('result').get('baseList',[])
        optionList = data.get('result').get('optionList',[])
        for i in baseList:
             for j in optionList:
                  if i['fin_prdt_cd'] == j['fin_prdt_cd']:
                        # 중복 확인
                        if DepositModel.objects.filter(
                        kor_co_nm=i['kor_co_nm'],
                        fin_prdt_nm=i['fin_prdt_nm'],
                        join_way=i['join_way'],
                        mtrt_int=i['mtrt_int'],
                        spcl_cnd=i['spcl_cnd'],
                        etc_note=i['etc_note'],
                        intr_rate=j['intr_rate'],
                        intr_rate2=j['intr_rate2'],
                        intr_rate_type_nm=j['intr_rate_type_nm'],
                        save_trm=j['save_trm'],
                        ).exists():
                            # print('skip')
                            continue
                        else:
                        # 데이터 저장
                            DepositModel.objects.create(
                                kor_co_nm=i['kor_co_nm'],
                                fin_prdt_nm=i['fin_prdt_nm'],
                                join_way=i['join_way'],
                                mtrt_int=i['mtrt_int'],
                                spcl_cnd=i['spcl_cnd'],
                                etc_note=i['etc_note'],
                                intr_rate=j['intr_rate'],
                                intr_rate2=j['intr_rate2'],
                                intr_rate_type_nm=j['intr_rate_type_nm'],
                                save_trm=j['save_trm'],
                            )

def save_saving(data):
    # for result in data:  # data는 리스트이므로 각 요소를 순회
        baseList = data.get('result').get('baseList',[])
        optionList = data.get('result').get('optionList',[])
        for i in baseList:
             for j in optionList:
                  if i['fin_prdt_cd'] == j['fin_prdt_cd']:
                        # 중복 확인
                        if SavingModel.objects.filter(
                        kor_co_nm=i['kor_co_nm'],
                        fin_prdt_nm=i['fin_prdt_nm'],
                        join_way=i['join_way'],
                        mtrt_int=i['mtrt_int'],
                        spcl_cnd=i['spcl_cnd'],
                        etc_note=i['etc_note'],
                        intr_rate=j['intr_rate'],
                        intr_rate2=j['intr_rate2'],
                        intr_rate_type_nm=j['intr_rate_type_nm'],
                        save_trm=j['save_trm'],
                        rsrv_type_nm= j['rsrv_type_nm']
                        ).exists():
                            # print('skip')
                            continue
                        else:
                        # 데이터 저장
                            SavingModel.objects.create(
                                kor_co_nm=i['kor_co_nm'],
                                fin_prdt_nm=i['fin_prdt_nm'],
                                join_way=i['join_way'],
                                mtrt_int=i['mtrt_int'],
                                spcl_cnd=i['spcl_cnd'],
                                etc_note=i['etc_note'],
                                intr_rate=j['intr_rate'],
                                intr_rate2=j['intr_rate2'],
                                intr_rate_type_nm=j['intr_rate_type_nm'],
                                save_trm=j['save_trm'],
                                rsrv_type_nm= j['rsrv_type_nm']
                            )
def send_saving(request):
     d=SavingModel.objects.all()
     lst = [
    {
        'id':i.id,
        "kor_co_nm": i.kor_co_nm,
        "fin_prdt_nm": i.fin_prdt_nm,
        "join_way": i.join_way,
        "mtrt_int": i.mtrt_int,
        "spcl_cnd": i.spcl_cnd,
        "etc_note": i.etc_note,
        "intr_rate": i.intr_rate,
        "intr_rate2": i.intr_rate2,
        "intr_rate_type_nm": i.intr_rate_type_nm,
        "save_trm": i.save_trm,
        'rsrv_type_nm':i.rsrv_type_nm,
    }
    for i in d
]
     return JsonResponse(lst,safe=False)

def exchange_rate(request):
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        'authkey': EXCHANGE_KEY,
        'data':'AP01',
        'searchdate': '20241118',
    }
    response = requests.get(url, params=params,verify=False)
    print('---------------------')
    print(response)
    data = response.json()
    return JsonResponse(data,safe=False)

@api_view(['POST'])  # REST API 뷰 데코레이터 사용
@authentication_classes([TokenAuthentication])  # TokenAuthentication 활성화
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def saveSaving(request):
    data = json.loads(request.body)

    # 요청에서 saving_id 가져오기
    saving_id = data.get('id')
    print(saving_id)
    # SavingModel 객체 가져오기
    saving = SavingModel.objects.get(id=saving_id)
    # ManyToMany 관계 추가
    if not request.user.saving.filter(id=saving.id).exists():
        request.user.saving.add(saving)
        return JsonResponse({'message': '저장 성공'}, status=201)
    else:
        return JsonResponse({'message': '이미 저장된 정보입니다.'}, status=200)
    
@api_view(['POST'])  # REST API 뷰 데코레이터 사용
@authentication_classes([TokenAuthentication])  # TokenAuthentication 활성화
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def saveDeposit(request):
    data = json.loads(request.body)
    print('data',data)
    # 요청에서 saving_id 가져오기
    deposit_id = data.get('id')
    print(deposit_id)
    # SavingModel 객체 가져오기
    deposit = DepositModel.objects.get(id=deposit_id)
    # ManyToMany 관계 추가
    if not request.user.deposit.filter(id=deposit.id).exists():
        request.user.deposit.add(deposit)
        return JsonResponse({'message': '저장 성공'}, status=201)
    else:
        return JsonResponse({'message': '이미 저장된 정보입니다.'}, status=200)
    
@api_view(['POST'])  # REST API 뷰 데코레이터 사용
@authentication_classes([TokenAuthentication])  # TokenAuthentication 활성화
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def deleteDeposit(request):
    data = json.loads(request.body)
    print('data',data)
    # 요청에서 saving_id 가져오기
    deposit_id = data.get('id')
    # SavingModel 객체 가져오기
    deposit = DepositModel.objects.get(id=deposit_id)
    # ManyToMany 관계 추가
    if request.user.deposit.filter(id=deposit.id).exists():
        request.user.deposit.remove(deposit_id)
        return JsonResponse({'message': '삭제 성공'}, status=201)
    else:
        return JsonResponse({'message': '없는 데이터 입니다'}, status=200)
    
@api_view(['POST'])  # REST API 뷰 데코레이터 사용
@authentication_classes([TokenAuthentication])  # TokenAuthentication 활성화
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def deleteSaving(request):
    data = json.loads(request.body)
    print('data',data)
    # 요청에서 saving_id 가져오기
    saving_id = data.get('id')
    # SavingModel 객체 가져오기
    saving = SavingModel.objects.get(id=saving_id)

    # ManyToMany 관계 추가
    if request.user.saving.filter(id=saving.id).exists():
        request.user.saving.remove(saving_id)
        return JsonResponse({'message': '삭제 성공'}, status=201)
    else:
        return JsonResponse({'message': '없는 데이터 입니다'}, status=200)
    

@csrf_exempt
def openai_recommendation(request):
    if request.method == "POST":

        # 요청 데이터 파싱
        data = json.loads(request.body)
        question = data.get("question", "")

        # 적금/예금 관련 질문 여부 확인
        if "적금" in question:
            savings = SavingModel.objects.all().values("kor_co_nm", "fin_prdt_nm", "intr_rate", "intr_rate2",'intr_rate_type_nm','rsrv_type_nm')
            # 적금/예금 추천 메시지 구성
            messages = [
                {"role": "system", "content": '너는 금융권에서 20년 근무한 프로인데 지금 고객을 상대로 상품을 추천하고 있어. 너는 금융권에서 근무한 기간이 많아서 어떤 것을 원해도 고객의 요청에 맞는 최상의 제품을 추천해주는 프로야. 제품을 추천하는 이유와 그 상품이 어떤 상황에서 좋은지 최대한 친절하게 대답해줘'},
                {
                    "role": "user",
                    'content':
                            f"질문: {question}\n"
                            f"아래 데이터 중에서 최대 3개의 적절한 예금 및 적금을 추천해 주세요.\n"
                            f"적금: {savings}",
                },
            ]
        elif "예금" in question:
            deposits = DepositModel.objects.all().values("kor_co_nm", "fin_prdt_nm", "intr_rate", "intr_rate2",'intr_rate_type_nm')
            # 적금/예금 추천 메시지 구성
            messages = [
                {"role": "system", "content": '너는 금융권에서 20년 근무한 프로인데 지금 고객을 상대로 상품을 추천하고 있어. 너는 금융권에서 근무한 기간이 많아서 어떤 것을 원해도 고객의 요청에 맞는 최상의 제품을 추천해주는 프로야. 제품을 추천하는 이유와 그 상품이 어떤 상황에서 좋은지 최대한 친절하게 대답해줘'},
                {
                    "role": "user",
                    "content": 
                                f"질문: {question}\n"
                                f"아래 데이터 중에서 최대 3개의 적절한 예금 및 적금을 추천해 주세요.\n"
                                f"예금: {deposits}",
                },
            ]
        else:
            # 일반 질문 처리 메시지 구성
            messages = [
                {"role": "system", "content": '너는 금융권에서 20년 근무한 프로인데 지금 고객이 상품이랑은 다른 질문을 하는 거 같은데 그래도 최대한 친절하게 대답해줘'},
                {"role": "user", "content": question},
            ]
        try:
        # OpenAI API 호출
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=messages,
            )
        except Exception as e:
            print(e)
        # OpenAI 응답 처리
        content = response.choices[0].message.content  # 첫 번째 메시지의 내용 추출

        return JsonResponse({
            "response": content
        })


@csrf_exempt
def legaldong(request):
    # GET 요청에서 'lawd_cd' 파라미터 추출
    lawd_cd = request.GET.get('lawd_cd')[:5]  # GET 요청에서 'lawd_cd' 값을 추출
    print('요청된 법정동 코드:', lawd_cd)
    data_lst=[]
    for year in range(2017,2025):
        for date in range(1,12):
    # print(DATAKEY)
    # 국토교통부 API URL 및 파라미터 설정

    # url = 'http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade'
    # params = {
    #     'LAWD_CD': lawd_cd,
    #     'DEAL_YMD': '202411',
    #     'serviceKey': DATAKEY,
    # }
            url = f'http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade?LAWD_CD={lawd_cd}&DEAL_YMD={year}{date}&serviceKey={DATAKEY}'
            print(url)
            # response = requests.get(url, params=params)
            response = requests.get(url)
            # print('응답 본문:', response.text) 
            print('요청 상태 코드:', response.status_code)
            # response=requests.get(url)
            # 요청 성공 여부 확인
            xml_data = response.text
            json_data = xmltodict.parse(xml_data)
            data_lst.append(json_data)

    return JsonResponse(data_lst, safe=False)
