
from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', views.AccountListCreate.as_view(), name='account-list'),
    path('accounts/<int:pk>/', views.AccountDetailDelete.as_view(), name='account-detail'),
    path('accounts/<int:pk>/destinations/', views.DestinationListCreate.as_view(), name='destination-list'),
    path('server/incoming_data/', views.IncomingDataView.as_view(), name='incoming-data'),

]
