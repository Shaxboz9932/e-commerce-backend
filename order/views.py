from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Order, OrderItem
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.models import CartItem
from rest_framework.views import APIView
from order.serializers import OrderSerializer
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_VERSION

class OrderListOrCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"detail": "Savat bo'sh..."}, status=400)

        # Tranzaksiya blokini ochamiz
        try:
            with transaction.atomic():
                # Order yaratish
                order = Order.objects.create(
                    user=user,
                    phone=request.data.get("phone"),
                    last_name=request.data.get("last_name"),
                    first_name=request.data.get("first_name"),
                    email=request.data.get("email"),
                    address=request.data.get("address"),
                    city=request.data.get("city"),
                    postal_code=request.data.get("postal_code")
                )
                

                # OrderItem'larni yaratish
                order_items = [
                    OrderItem(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity
                    ) for item in cart_items
                ]
                OrderItem.objects.bulk_create(order_items) # Tezroq ishlashi uchun bulk_create

                success_url = request.build_absolute_uri(reverse('order:completed'))
                cancel_url = request.build_absolute_uri(reverse('order:canceled'))

                session_data = {
                    "mode": "payment",
                    'client_reference_id': str(order.id),
                    "success_url": success_url,
                    "cancel_url": cancel_url,
                    'line_items': []
                }

                for item in order.items.all():
                    session_data['line_items'].append({
                        "price_data": {
                            "unit_amount": int(item.price * 100),
                            "currency": "usd",
                            "product_data": {
                                "name": item.product.title
                            }
                        },
                        "quantity": item.quantity
                    })

                session = stripe.checkout.Session.create(**session_data)

                send_mail(
                    subject="Order Created",
                    message=f"Your order has been created successfully. Your order id: {order.id}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[request.data.get("email")],
                    fail_silently=False,
                    html_message=render_to_string("email.html", {"order": order})
                )

                return Response({"order_id": order.id, "url": session.url}, status=201)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

def payment_process(request, pk):

    order_id = pk
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse('order:completed'))
        cancel_url = request.build_absolute_uri(reverse('order:canceled'))

        session_data = {
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            'line_items': []
        }

        for item in order.items.all():
            session_data['line_items'].append({
                "price_data": {
                    "unit_amount": int(item.price * 100),
                    "currency": "usd",
                    "product_data": {
                        "name": item.product.title
                    }
                },
                "quantity": item.quantity
            })

        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, 'process.html', locals())

def payment_completed(request):
    return render(request, 'completed.html')

def payment_canceled(request):
    return render(request, 'canceled.html')
