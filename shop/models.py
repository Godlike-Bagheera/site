from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('URL-идентификатор', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    price = models.DecimalField(
        'Цена', max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='products'
    )
    in_stock = models.BooleanField('В наличии', default=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_deleted = models.BooleanField('Удален', default=False)

    class Meta:
        verbose_name = 'Товар'        
        verbose_name_plural = 'Товары' 
        ordering = ['-created_at']

    def __str__(self):              
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Клиент',
        related_name='orders'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    status = models.CharField(
        'Статус', max_length=20, choices=STATUS_CHOICES, default='new'
    )
    total = models.DecimalField(
        'Сумма', max_digits=12, decimal_places=2, default=0
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ №{self.id} от {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Товар',
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField(
        'Цена на момент заказа', max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        'Оценка', choices=[(i, str(i)) for i in range(1, 6)]
    )
    text = models.TextField('Текст отзыва', blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ('product', 'user')

    def __str__(self):
        return f'Отзыв от {self.user.username} на {self.product.name}'