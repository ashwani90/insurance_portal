from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='insurance_listing'),
    path('<int:insurance_id>/<str:errorMessage>', views.edit_insurance, name='edit_insurance'),
    path('edit', views.edit_action, name='edit_action'),
    path('charts', views.charts, name='chart'),
]