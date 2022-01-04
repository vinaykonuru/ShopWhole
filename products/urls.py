from django.urls import path,include
from . import views
urlpatterns = [
    path('<int:product_id>',views.detail,name='detail'),
    path('<int:product_id>/order',views.order,name='order'),
    path('<int:product_id>/remove',views.removeItem,name='removeItem')
]
