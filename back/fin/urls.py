"""
URL configuration for my_pjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
app_name='fin'

urlpatterns = [
    path('saving/',views.get_saving,name='get_saving'),
    path('deposit/',views.get_deposit,name='get_deposit'),
    path('exchange_rate/',views.exchange_rate,name='exchange_rate'),
    path('send_deposit/',views.send_deposit,name='send_deposit'),
    path('send_saving/',views.send_saving,name='send_saving'),
    path('saveSaving/',views.saveSaving,name='saveSaving'),
    path('saveDeposit/',views.saveDeposit,name='saveDeposit'),
    path('deleteSaving/',views.deleteSaving,name='delete_saving'),
    path('deleteDeposit/',views.deleteDeposit,name='delete_deposit'),
    path("api/openai", views.openai_recommendation, name="openai_recommendation"),
    path('legaldong/',views.legaldong,name='legadong')

]
