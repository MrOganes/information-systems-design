from django.urls import path
from cabinet import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:page>', views.home, name='home'),
    path('delete/<int:customer_id>/', views.delete, name='delete'),
    path('delete/<int:customer_id>/<int:page>', views.delete, name='delete_and_redirect'),
    path('update/<int:customer_id>/', views.update, name='update'),
    path('add/', views.add, name='add'),
]
