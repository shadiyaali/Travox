from django.urls import path
 
from .views import *

urlpatterns = [
 
   path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
   path('admin-create/', AdminCreateView.as_view(), name='admin-create'),
   path('admins-all/', AdminListView.as_view(), name='admin-list'),
   path('admin/<int:id>/', AdminDetailView.as_view(), name='admin-detail'),
   path('admin-update/<int:pk>/', AdminUpdateView.as_view(), name='admin-update'),
   path('admin-block/<int:pk>/', BlockUnblockAdminView.as_view(), name='toggle-admin-status'),
   path('admin-delete/<int:pk>/', AdminDeleteView.as_view(), name='admin-delete'),
   path('subscriptions-create/', SubscriptionCreateView.as_view(), name='subscription-create'),
   path('subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),
   path('subscriptions/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription-detail'),
   path('subscriptions-update/<int:pk>/', SubscriptionUpdateView.as_view(), name='subscription-update'),
   path('subscriptions-delete/<int:pk>/', SubscriptionDeleteView.as_view(), name='subscription-delete'),
   path('users-create/', UsersCreateView.as_view(), name='request-subscription'),
   path('users/', UsersListView.as_view(), name='users-list'),
   path('users/<int:id>/', UsersDetailView.as_view(), name='users-detail'),
   path('users-update/<int:id>/', UsersUpdateView.as_view(), name='users-update'),
   path('users-delete/<int:id>/', UsersDeleteView.as_view(), name='users-delete'),
   path('user-block/<int:pk>/', BlockUnblockUsersView.as_view(), name='block-unblock-user'),
   path('staff-create/', StaffCreateView.as_view(), name='admin-create'),
   path('staff-all/', StaffListView.as_view(), name='admin-list'),
   path('staff/<int:id>/', StaffDetailView.as_view(), name='admin-detail'),
   path('staff-update/<int:pk>/', StaffUpdateView.as_view(), name='admin-update'),
   path('staff-block/<int:pk>/', BlockUnblockStaffView.as_view(), name='toggle-admin-status'),
   path('staff-delete/<int:pk>/', StaffDeleteView.as_view(), name='admin-delete'),
]