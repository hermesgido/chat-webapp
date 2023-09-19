

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('group_chat/<str:id>/', views.group_chat, name="group_chat"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout"),
    
    path('user_profile/', views.user_profile, name="user_profile"),
    path('add_group_member/<str:id>/', views.add_group_member, name="add_group_member"),

    path('buy_product/', views.buy_product, name="buy_product"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
