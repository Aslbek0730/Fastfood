from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, UpdateProfileForm
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import CustomUser, Saved, Order
from django.contrib.auth.mixins import LoginRequiredMixin
from foods.models import Food
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import json


class SignupView(SuccessMessageMixin, View):
    def get(self, request):
        return render(request, 'registration/signup.html', {'form': SignupForm()})
    
    def post(self, request):
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account is successfully created.')
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})

    
class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        return render(request, 'profile.html', {'customuser':user})
        pass
    
class UpdateProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        form = UpdateProfileForm(instance=request.user)
        return render(request, 'profile_update.html', {'form':form})
    
    def post(self, request):
        form = UpdateProfileForm(instance=request.user, data=request.POST, files=request.FILES )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account is successfully updated.')
            return redirect('users:profile', request.user)
        return render(request, 'registration/signup.html', {'form': form})
    
    
    
    
class BuyingView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request, food_id):
        food = get_object_or_404(Food, id=food_id)
        buy_food = Saved.objects.filter(author=request.user, food=food)
        if buy_food:
            buy_food.delete()
            messages.info(request, 'Cancelled')
        else:
            Saved.objects.create(author=request.user, food=food)
            messages.info(request, 'Buy a food.')
        return redirect(request.META.get("HTTP_REFERER"))
    

class BuyFoodView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        saveds = Saved.objects.filter(author=request.user)
        total_amount = sum(saved.total_price for saved in saveds)
        return render(request, 'buy_food.html', {
            'saveds': saveds,
            'total_amount': total_amount
        })

@method_decorator(csrf_exempt, name='dispatch')
class UpdateQuantityView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, saved_id):
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            
            if quantity < 1:
                return JsonResponse({'error': 'Quantity must be at least 1'}, status=400)
            
            saved = get_object_or_404(Saved, id=saved_id, author=request.user)
            saved.quantity = quantity
            saved.save()
            
            # Calculate new total amount
            total_amount = sum(saved.total_price for saved in Saved.objects.filter(author=request.user))
            
            return JsonResponse({
                'success': True,
                'total_amount': total_amount
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class CheckoutView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request):
        try:
            # Get cart items
            cart_items = Saved.objects.filter(author=request.user)
            if not cart_items.exists():
                messages.error(request, 'Your cart is empty')
                return redirect('users:buyed')
            
            # Calculate total amount
            total_amount = sum(item.total_price for item in cart_items)
            
            # Set delivery time to 2 minutes from now
            delivery_time = timezone.now() + timedelta(minutes=2)
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                address=request.POST.get('address'),
                card_number=request.POST.get('card_number')[-4:],  # Store only last 4 digits
                card_expiry=request.POST.get('card_expiry'),
                status='processing',  # Start with processing status
                delivery_time=delivery_time
            )
            
            # Add items to order
            order.items.set(cart_items)
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, f'Buyurtmangiz qabul qilindi! {delivery_time.strftime("%H:%M")} da yetkazib beriladi.')
            return redirect('users:order_history')
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
            return redirect('users:buyed')

class OrderHistoryView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        # Update order statuses
        current_time = timezone.now()
        processing_orders = Order.objects.filter(status='processing', delivery_time__lte=current_time)
        for order in processing_orders:
            order.status = 'completed'
            order.save()
        
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'order_history.html', {'orders': orders})

@method_decorator(csrf_exempt, name='dispatch')
class ConfirmDeliveryView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, order_id):
        try:
            order = get_object_or_404(Order, id=order_id, user=request.user)
            order.is_delivered = True
            order.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class SubmitRatingView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, order_id):
        try:
            data = json.loads(request.body)
            order = get_object_or_404(Order, id=order_id, user=request.user)
            
            if not order.is_delivered:
                return JsonResponse({'error': 'Buyurtma hali yetkazilmagan'}, status=400)
            
            order.rating = data.get('rating')
            order.review = data.get('review')
            order.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)