from django.db import models


class Address(models.Model):
    foto = models.ImageField(blank=False, null=False)
    sketch_number = models.SmallIntegerField(blank=False, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Эскиз № {self.sketch_number}, цена: {self.price}'


class Order(models.Model):
    form_sign = models.ForeignKey(Address, on_delete=models.CASCADE)
    color_sign = models.CharField(max_length=50, default='Синий')
    address_sign = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=50)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30)
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ № {self.pk}'


class Review(models.Model):
    name_autor = models.CharField(max_length=20, blank=False)
    review_autor = models.TextField(max_length=100, blank=False)

    def __str__(self):
        return f'Автор отзыва: {self.name_autor}'
