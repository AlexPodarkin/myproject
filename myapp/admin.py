from django.contrib import admin
from . import models


class AdminAddress(admin.ModelAdmin):
    list_display = ['sketch_number', 'foto', 'price', 'date_added']
    ordering = ['date_added']
    readonly_fields = ['date_added']
    list_filter = ['price', 'date_added']
    fieldsets = [
        (
            'Загрузите фото таблички',
            {
                'classes': ['wide'],
                'fields': ['foto'],
            },
        ),
        (
            'Укажите УНИКАЛЬНЫЙ номер таблички (номер будет использован при заказе)',
            {
                'classes': ['wide'],
                'fields': ['sketch_number'],
            },
        ),
        (
            'Укажите цену таблички',
            {
                # 'classes': ['wide'],
                'fields': ['price'],
            },
        ),
        (
            'Дата добавления таблички (устанавливается автоматически)',
            {
                # 'classes': ['wide'],
                'fields': ['date_added'],

            },
        ),
    ]


class AdminOrder(admin.ModelAdmin):
    list_display = ['pk', 'form_sign', 'color_sign',
                    'address_sign', 'customer_name', 'customer_email', 'customer_phone']


admin.site.register(models.Address, AdminAddress)
admin.site.register(models.Order, AdminOrder)
admin.site.register(models.Review)
