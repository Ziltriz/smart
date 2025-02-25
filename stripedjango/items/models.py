from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(max_length=3, default='usd', verbose_name='Валюта') 

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Discount(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Tax(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField('Item', related_name='orders')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.CharField(max_length=3, default='usd')

    @property
    def total_price(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total -= total * (self.discount.percentage / 100)
        if self.tax:
            total += total * (self.tax.percentage / 100)
        return total

    def __str__(self):
        return f"Order #{self.id}"
    
