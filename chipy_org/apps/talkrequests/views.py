from django.views.generic import ListView
from . import models


class TalkRequestList(ListView):
    model = models.TalkRequest
    context_object_name = "talkrequests"
    template_name = "talkrequests/talkrequests_list.html"

    def dispatch(self, request, *args, **kwargs):
        self.category = request.GET.get('category')
        return super(TalkRequestList, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        category_slugs = models.TalkCategory.objects.values_list('slug', flat=True)
        category_slug = self.category
        kwargs = {}
        if category_slug in category_slugs:
            kwargs.update({"category__slug": category_slug})
        return models.TalkRequest.objects.active().filter(**kwargs)
