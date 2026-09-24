#from django.db import models

# Create your models here.

from django.db import models
from products.models import Product
from users.models import User, Address


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carts'


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        db_column='cart_id'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        db_column='product_id'
    )
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart_items'
        unique_together = (('cart', 'product'),)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING,
        db_column='address_id'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=30,
        default='PENDING',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column='order_id'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        db_column='product_id'
    )
    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        managed = False
        db_table = 'order_items'