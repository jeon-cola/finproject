# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('board.urls')),  # 변경된 board 경로 포함
    path('api-auth/', include('rest_framework.urls')),
    path('fin/',include('fin.urls'))
]
