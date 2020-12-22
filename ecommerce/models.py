from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

CATEGORY = (
    ('S', 'Shirt'),
    ('SW', 'SportWear'),
    ('OW', 'OutWear'),
)

LABEL = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY, max_length=10)
    label = models.CharField(choices=LABEL, max_length=1)
    description = models.TextField(default='A Product')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ecommerce:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("ecommerce:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("ecommerce:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
