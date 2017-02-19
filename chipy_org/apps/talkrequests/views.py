from django.views.generic import ListView, FormView
from django.contrib import messages
from django.views.generic.list import MultipleObjectMixin
from django.core.urlresolvers import reverse_lazy
from . import models
from . import forms


class TalkRequestList(MultipleObjectMixin, FormView):
    form_class = forms.TalkRequestSubmissionForm
    model = models.TalkRequest
    success_url = reverse_lazy("talkrequests_list")
    context_object_name = "talkrequests"
    template_name = "talkrequests/talkrequests_list.html"
    paginate_by = 50

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.category = request.GET.get('category')
        self.object_list = self.get_queryset()
        return super(TalkRequestList, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        category_slugs = models.TalkCategory.objects.values_list('slug', flat=True)
        category_slug = self.category
        kwargs = {}
        if category_slug in category_slugs:
            kwargs.update({"category__slug": category_slug})
        return models.TalkRequest.objects.active().filter(**kwargs)

    def form_valid(self, form):
        talk_request = form.save(commit=False)
        talk_request.submitter = self.request.user
        talk_request.save()
        messages.add_message(self.request, messages.INFO, 'Thank you for your idea.')
        return super(TalkRequestList, self).form_valid(form)




# class TalkRequestList(ListView):
#     model = models.TalkRequest
#     context_object_name = "talkrequests"
#     template_name = "talkrequests/talkrequests_list.html"
#     paginate_by = 50
#     http_method_names = ['get', 'post']
#
#     def dispatch(self, request, *args, **kwargs):
#         self.category = request.GET.get('category')
#         self.form = forms.TalkRequestSubmissionForm
#         return super(TalkRequestList, self).dispatch(
#             request, *args, **kwargs)
#
#     def post(self, *args, **kwargs):
#
#         return super(TalkRequestList, self).get(*args, **kwargs)
#
#     def get_queryset(self):
#         category_slugs = models.TalkCategory.objects.values_list('slug', flat=True)
#         category_slug = self.category
#         kwargs = {}
#         if category_slug in category_slugs:
#             kwargs.update({"category__slug": category_slug})
#         return models.TalkRequest.objects.active().filter(**kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(TalkRequestList, self).get_context_data(**kwargs)
#         context['form'] = self.form
#         return context
