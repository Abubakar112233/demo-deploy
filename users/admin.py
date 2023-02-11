from django.contrib import admin
from .models import CustomUser, SubscribedUsers, Currency

class CurrencyAdmin(admin.ModelAdmin):
	list_display=('currency_name','currency_symbol','currency_short_name','currency_price')
admin.site.register(Currency, CurrencyAdmin)

class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_date')

admin.site.register(CustomUser)
admin.site.register(SubscribedUsers, SubscribedUsersAdmin)