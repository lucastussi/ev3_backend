from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Asset
from .forms import AssetForm


class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'assets/asset_list.html'
    context_object_name = 'assets'

    def get_queryset(self):
        qs = Asset.objects.all().order_by('-created_at')
        if self.request.user.is_superuser:
            # Admin ve todos los assets
            return qs
        # Usuario normal ve solo los suyos
        return qs.filter(owner=self.request.user)


class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('assets:list')

    def form_valid(self, form):
        # Asignar automáticamente el owner
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('assets:list')

    def get_queryset(self):
        qs = Asset.objects.all()
        if self.request.user.is_superuser:
            # Admin puede editar cualquiera
            return qs
        # Usuario normal solo puede editar los suyos
        return qs.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        asset = self.get_object()
        if not (request.user.is_superuser or asset.owner == request.user):
            return HttpResponseForbidden("No tienes permiso para editar este asset.")
        return super().dispatch(request, *args, **kwargs)


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = 'assets/asset_confirm_delete.html'
    success_url = reverse_lazy('assets:list')

    def get_queryset(self):
        qs = Asset.objects.all()
        if self.request.user.is_superuser:
            # Admin puede eliminar cualquiera
            return qs
        # Usuario normal solo puede eliminar los suyos
        return qs.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        asset = self.get_object()
        if not (request.user.is_superuser or asset.owner == request.user):
            return HttpResponseForbidden("No tienes permiso para eliminar este asset.")
        return super().dispatch(request, *args, **kwargs)