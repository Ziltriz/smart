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

from django.db import models

class Discount(models.Model):
    # Название купона (отображается клиентам)
    name = models.CharField(max_length=255, verbose_name='Название', blank=True, null=True)

    # Скидка в процентах (percent_off)
    percent_off = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Скидка в процентах',
        blank=True,
        null=True,
        help_text="Значение от 0 до 100. Если указано, то amount_off не должно быть установлено."
    )

    # Скидка в валюте (amount_off)
    amount_off = models.PositiveIntegerField(
        verbose_name='Скидка в валюте',
        blank=True,
        null=True,
        help_text="Положительное целое число, представляющее сумму скидки в минимальных единицах валюты (например, центы)."
    )

    # Валюта для amount_off
    currency = models.CharField(
        max_length=3,
        verbose_name='Валюта',
        blank=True,
        null=True,
        help_text="Трехбуквенный код ISO для валюты (требуется, если указан amount_off)."
    )

    # Длительность действия скидки
    DURATION_CHOICES = [
        ('forever', 'Forever'),
        ('once', 'Once'),
        ('repeating', 'Repeating'),
    ]
    duration = models.CharField(
        max_length=10,
        choices=DURATION_CHOICES,
        default='once',
        verbose_name='Длительность',
        help_text="Как долго будет действовать скидка: forever, once или repeating."
    )

    # Длительность в месяцах (только для duration='repeating')
    duration_in_months = models.PositiveIntegerField(
        verbose_name='Длительность в месяцах',
        blank=True,
        null=True,
        help_text="Требуется только если duration='repeating'. Количество месяцев, в течение которых действует скидка."
    )

    # Метаданные (необязательно)
    metadata = models.JSONField(
        verbose_name='Метаданные',
        blank=True,
        null=True,
        help_text="Набор пар ключ-значение для хранения дополнительной информации о купоне."
    )

    def __str__(self):
        return self.name or f"Discount #{self.id}"

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def clean(self):
        """
        Проверяем, что либо percent_off, либо amount_off указаны, но не оба одновременно.
        Также проверяем, что currency указано, если используется amount_off.
        """
        if self.percent_off and self.amount_off:
            raise ValueError("Можно указать только один из параметров: percent_off или amount_off.")

        if not self.percent_off and not self.amount_off:
            raise ValueError("Необходимо указать хотя бы один из параметров: percent_off или amount_off.")

        if self.amount_off and not self.currency:
            raise ValueError("Параметр currency обязателен, если указан amount_off.")

        if self.duration == 'repeating' and not self.duration_in_months:
            raise ValueError("Параметр duration_in_months обязателен, если duration='repeating'.")
        

class Tax(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    inclusive = models.BooleanField(verbose_name='Добавляется ли процент налога к общей сумме или включается в нее', default = False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ='Сервисный сбор'
        verbose_name_plural='Сервисные сборы'

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
        return f"Заказ #{self.id}"
    
    class Meta:
        verbose_name ='Заказ'
        verbose_name_plural='Заказы'
    
