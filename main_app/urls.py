from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('designers/', views.DesignerList.as_view(), name="designer_list"),
    path('designers/new/', views.DesignerCreate.as_view(), name="designer_create"),
    path('designers/<int:pk>/', views.DesignerDetail.as_view(), name="designer_detail"),
    path('designers/<int:pk>/update',views.DesignerUpdate.as_view(), name="designer_update"),
    path('designers/<int:pk>/delete',views.DesignerDelete.as_view(), name="designer_delete"),
    path('designers/<int:pk>/items/new/', views.ItemCreate.as_view(), name="item_create"),
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
]
