from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('make-order/', views.make_order, name='make_order'),
    path('our_works/', views.our_works, name='our_works'),
    path('printing_on_mugs/', views.printing_on_mugs, name='printing_on_mugs'),
    path('printing_shirts/', views.printing_shirts, name='printing_shirts'),
    path('assortment_gifts/', views.assortment_gifts, name='assortment_gifts'),
]
