from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.views.generic import UpdateView
User = get_user_model()

from .models import UserProfile
from .forms import ProfileForm


class ProfilesList(ListView):
    context_object_name = 'profiles'
    template_name = 'profiles/list.html'
    queryset = User.objects.filter(profile__show=True)


class ProfileEdit(UpdateView):
    form_class = ProfileForm
    template_name = "profiles/edit.html"
    success_url = '/'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)
