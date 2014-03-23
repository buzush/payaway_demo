from django.contrib import admin
from bills.models import Bill, Type, UserProfile

# Register your models here.
class BillAdmin(admin.ModelAdmin):
	list_display = ('m_name', 'm_type', 'm_payDate')

admin.site.register(Bill, BillAdmin)
admin.site.register(Type)
admin.site.register(UserProfile)	# chapter 8 - user authentication

