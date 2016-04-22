from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from models import UserProfile

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def get_search_fields(self, request):
        sfields = super(UserAdmin, self).get_search_fields(request)
        return sfields + ('profile__display_name', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
