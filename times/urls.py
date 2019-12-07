from django.urls import path
from times import views

urlpatterns = [
    path('', views.time, name='time'),
    path('<int:year>/<int:month>/<int:day>/', views.time, name='time'),
    path('add/<int:year>/<int:month>/<int:day>/', views.add_entry, name='add_entry'),
    path('edit/<int:pk>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:pk>/', views.delete_entry, name="delete_entry"),
    path('pick/', views.pick_date, name='pick_date'),
    path('start/<int:entry_id>/', views.start_timer, name='start'),
    path('stop/<int:entry_id>/', views.stop_timer, name='stop')
]
