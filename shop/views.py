from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Product, Order, OrderItem, Review, Category

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_deleted=False, in_stock=True)
        category_id = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if category_id:
            qs = qs.filter(category_id=category_id)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    template_name = 'shop/order_create.html'

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        order = Order.objects.create(user=request.user, total=product.price)
        OrderItem.objects.create(order=order, product=product, quantity=1, price=product.price)
        return redirect('order-list')

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'text']
    template_name = 'shop/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product_id = self.kwargs['product_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product-detail', kwargs={'pk': self.kwargs['product_id']})

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')