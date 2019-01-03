from django.contrib import admin

from capybara_forms.models import SelectData


class SelectDataAdmin(admin.ModelAdmin):
    fields = ('key', 'value')


admin.site.register(SelectData, SelectDataAdmin)
