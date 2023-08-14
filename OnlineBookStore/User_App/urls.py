from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home),
    path('showFilterBook/<id>',views.showFilterBook),
    path('ViewDetails/<id>',views.ViewDetails),
    path('user_login', views.user_login),
    path('signUp', views.signUp),
    path('logOut', views.logOut),
    path('addToCart', views.addTocart),
    path('showMycart',views.showMycart),
    path('Make_payment',views.Make_payment),
    path('buy_now',views.buy_now),
    path('myOrder',views.myOrder),
    path('contact',views.contact),
    path('address',views.address),
    path('search',views.search),
]
