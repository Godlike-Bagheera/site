from django.contrib.auth.models import User
from shop.models import Category, Product, Order, OrderItem, Review

admin = User.objects.create_superuser('admin', 'admin@shop.ru', 'admin123')
client1 = User.objects.create_user('client1', 'c1@shop.ru', 'pass123')
client2 = User.objects.create_user('client2', 'c2@shop.ru', 'pass123')

cat1 = Category.objects.create(name='Электроника', slug='electronics')
cat2 = Category.objects.create(name='Книги', slug='books')
cat3 = Category.objects.create(name='Одежда', slug='clothing')

p1 = Product.objects.create(name='Смартфон', price=29990, category=cat1, in_stock=True)
p2 = Product.objects.create(name='Ноутбук', price=54990, category=cat1, in_stock=True)
p3 = Product.objects.create(name='Роман «Мастер и Маргарита»', price=890, category=cat2)
p4 = Product.objects.create(name='Футболка', price=1500, category=cat3)

o1 = Order.objects.create(user=client1, status='completed', total=29990)
OrderItem.objects.create(order=o1, product=p1, quantity=1, price=29990)

o2 = Order.objects.create(user=client2, status='new', total=890)
OrderItem.objects.create(order=o2, product=p3, quantity=1, price=890)

Review.objects.create(product=p1, user=client1, rating=5, text='Отличный телефон!')
Review.objects.create(product=p3, user=client2, rating=4, text='Хорошая книга.')
