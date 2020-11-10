
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from newapp.models import User


class UserAdmin(BaseUserAdmin):

	list_display = ('email','username','phone','is_admin','is_staff','timestamp')
	search_fields = ('email','username',)
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(User, BaseUserAdmin)


