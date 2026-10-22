from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum
from django.utils.dateparse import parse_date
from .models import Category, Product, Order, OrderItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'in_stock', 'is_deleted', 'created_at')
    list_filter = ('category', 'in_stock', 'is_deleted')
    search_fields = ('name',)
    list_editable = ('price', 'in_stock') 

    def get_queryset(self, request):
        return Product.objects.all()

    def delete_model(self, request, obj):
        obj.is_deleted = True
        obj.save()

    def delete_queryset(self, request, queryset):
        queryset.update(is_deleted=True)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-report/', self.admin_site.admin_view(self.sales_report),
                 name='sales-report'),
        ]
        return custom_urls + urls

    def sales_report(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')
        orders = Order.objects.filter(status='completed')
        
        if start:
            orders = orders.filter(created_at__date__gte=parse_date(start))
        if end:
            orders = orders.filter(created_at__date__lte=parse_date(end))

        total_sales = orders.aggregate(total=Sum('total'))['total'] or 0
        
        context = {
            'orders': orders,
            'total_sales': total_sales,
            'start': start or '',
            'end': end or '',
            **self.admin_site.each_context(request),
        }
        return render(request, 'admin/sales_report.html', context)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)