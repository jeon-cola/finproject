from PublicDataReader import TransactionPrice

service_key = "WQLW+PJ8NopQUJEWI6ZQQyNbVHGAZp+MOk5OcaRMk015ya+8Q4YC4lEJml8tMQXNxHW7AEQaCcejFWvh7bYxvw=="
api = TransactionPrice(service_key)

# 단일 월 조회
df = api.get_data(
    property_type="아파트",
    trade_type="매매",
    sigungu_code="11650",
    year_month="202212",
)

# 기간 내 조회
df = api.get_data(
    property_type="아파트",
    trade_type="매매",
    sigungu_code="11650",
    start_year_month="202201",
    end_year_month="202212",
)

df.tail()