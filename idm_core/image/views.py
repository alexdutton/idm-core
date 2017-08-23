from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, View
from django.views.generic.detail import SingleObjectMixin
from sendfile import sendfile

from idm_core.identity.models import Identity
from idm_core.utils.mixins import FSMTransitionViewMixin

from . import forms, models


class ImageView(View):
    model = models.Image
    identity = None
    is_self = None

    def dispatch(self, request, *args, **kwargs):
        if 'identity_type' in self.kwargs:
            self.is_self = False
            self.identity = Identity.objects.get(id=self.kwargs['identity_id']).identity
            if self.kwargs['identity_type'] != self.identity.type_slug:
                raise Http404
        elif self.request.user.identity:
            self.is_self = True
            self.identity = self.request.user.identity
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(identity_id=self.identity.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'identity': self.identity,
            'is_self': self.is_self,
        })
        return context


class ImageListView(ImageView, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = {context: {}
                             for context in models.ImageContext.objects.all()}
        for image in self.get_queryset():
            context['images'][image.context][image.state] = image
        return context


class ImageDetailView(FSMTransitionViewMixin, ImageView, DetailView):
    available_transitions = {'accept', 'reject'}


class ImageFileView(SingleObjectMixin, View):
    model = models.Image

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return sendfile(request, self.object.image.path)


class ImageCreateView(ImageView, CreateView):
    form_class = forms.ImageForm

    def post(self, request, **kwargs):
        with transaction.atomic():
            return super().post(self, request, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.model(identity_content_type=ContentType.objects.get_for_model(self.identity),
                                        identity_id=self.identity.id,
                                        context=get_object_or_404(models.ImageContext, id=self.kwargs['context']))
        return kwargs

    def get_success_url(self):
        if self.is_self:
            return reverse('image:image-list-self')
        else:
            return reverse('image:image-list', args=(self.identity.type_slug, self.identity.id))
