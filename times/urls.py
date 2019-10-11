from times.views import Time
from django.urls import path

urlpatterns = [
    path('', Time.time, name='time'),
    path('<int:year>/<int:month>/<int:day>/', Time.time, name='time'),
    path('add/<int:year>/<int:month>/<int:day>/', Time.add_entry, name='add_entry'),
    path('edit/<int:pk>/', Time.edit_entry, name='edit_entry'),
    path('delete/<int:pk>/', Time.delete_entry, name="delete_entry"),
    path('pick/', Time.pick_date, name='pick_date'),
    path('start/<int:entry_id>/', Time.start_timer, name='start'),
    path('stop/<int:entry_id>/', Time.stop_timer, name='stop')
]
