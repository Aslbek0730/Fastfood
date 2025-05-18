from .views import SignupView, ProfileView, UpdateProfileView, BuyingView, BuyFoodView, UpdateQuantityView, CheckoutView, OrderHistoryView, ConfirmDeliveryView, SubmitRatingView
from django.urls import path


app_name = 'users'
urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('Profile/<str:username>/', ProfileView.as_view(), name='Profile'),
    path('update', UpdateProfileView.as_view(), name='update'),
    path('buyafood/<int:food_id>', BuyingView.as_view(), name='buyafood'),
    path('buyed', BuyFoodView.as_view(), name='buyed'),
    path('update-quantity/<int:saved_id>/', UpdateQuantityView.as_view(), name='update_quantity'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderHistoryView.as_view(), name='order_history'),
    path('confirm-delivery/<int:order_id>/', ConfirmDeliveryView.as_view(), name='confirm_delivery'),
    path('submit-rating/<int:order_id>/', SubmitRatingView.as_view(), name='submit_rating'),
]
