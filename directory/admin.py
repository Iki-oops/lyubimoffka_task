from django.contrib import admin
from .models import Company, Employee


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'name', 'description')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'position', 'work', 'company')
    fields = ('full_name', 'position', ('work', 'private', 'fax'), 'company', 'owner')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
