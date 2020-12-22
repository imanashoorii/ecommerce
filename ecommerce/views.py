from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib import messages


# Create your views here.

# def homepage(request):
#     """
#     show homepage
#     """
#     context = {
#         'items': Item.objects.all()
#     }


#     return render(request, 'home-page.html', context)

def checkout(request):
    return render(request, 'checkout-page.html')


def product(request):
    context = {
        'items': Item.objects.all()
    }

    return render(request, 'product-page.html', context)


class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


class OrderSummaryView(DetailView):
    model = Order
    template_name = 'order_summary.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("ecommerce:product", slug=slug)
        else:
            messages.info(request, "This item was successfully added to your cart.")
            order.item.add(order_item)
            return redirect("ecommerce:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, "This item was successfully added to your cart.")
    return redirect("ecommerce:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.item.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("ecommerce:product", slug=slug)
        else:
            # add a message saying the user doesnt have an order
            messages.info(request, "You do not have an active order")
            return redirect("ecommerce:product", slug=slug)
    else:
        # add a message saying the user doesnt have an order
        messages.info(request, "This item was not in to your your cart.")
        return redirect("ecommerce:product", slug=slug)
