# Generated by Django 4.1.13 on 2025-02-25 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_discount_tax_remove_order_total_price_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'verbose_name': 'Скидка', 'verbose_name_plural': 'Скидки'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'Сервисный сбор', 'verbose_name_plural': 'Сервисные сборы'},
        ),
    ]
