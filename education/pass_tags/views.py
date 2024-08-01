from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.forms import inlineformset_factory


# Create your views here.

from .models import PassTag, PassTagRequest, PassTagRequestItem
from .forms import PassTagForm, PassTagRequestForm, PassTagRequestItemForm

from education.metadata import get_dependencies

class PassTagDelete(DeleteView):
    model = PassTag
    success_url = reverse_lazy('pass_tag_list')
    template_name = 'object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['object_verbose_name'] = self.model._meta.verbose_name
        context['back_url'] = self.success_url
        return context

    def get(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        dependencies = get_dependencies(object_to_delete)
        context = {
            'username': request.user.username,
            'object': object_to_delete,
            'object_verbose_name': self.model._meta.verbose_name,
            'dependencies': dependencies,
            'back_url': self.success_url
        }
        if dependencies != {}:
            return render(request, 'object_cannot_delete.html', context)
        return super().get(request, *args, **kwargs)


@login_required(login_url='/login/')
def pass_tag_list(request):
    pass_tags = PassTag.objects.all()
    return render(request, 'entities/pass_tag/list.html', {'username': request.user.username, 'pass_tag_list': pass_tags})


@login_required(login_url='/login/')
def pass_tag_new(request):
    back_link = 'pass_tag_list'
    back_url = reverse_lazy(back_link)
    if request.method == "POST":
        form = PassTagForm(request.POST)
        if form.is_valid():
            pass_tag = form.save(commit=False)
            pass_tag.save()
            return redirect(back_link)
    else:
        form = PassTagForm()
    return render(request, 'entities/pass_tag/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


@login_required(login_url='/login/')
def pass_tag_edit(request, pk):
    back_link = 'pass_tag_list'
    back_url = reverse_lazy(back_link)
    pass_tag = get_object_or_404(PassTag, pk=pk)
    if request.method == 'POST':
        form = PassTagForm(request.POST, instance=pass_tag)
        if form.is_valid():
            pass_tag = form.save(commit=False)
            pass_tag.save()
            return redirect(back_link)
    else:
        form = PassTagForm(instance=pass_tag)
    return render(request, 'entities/pass_tag/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


class PassTagRequestDelete(DeleteView):
    model = PassTagRequest
    success_url = reverse_lazy('pass_tag_request_list')
    template_name = 'object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['object_verbose_name'] = self.model._meta.verbose_name
        context['back_url'] = self.success_url
        return context


@login_required(login_url='/login/')
def pass_tag_request_list(request):
    pass_tag_requests = PassTagRequest.objects.all()
    return render(request, 'entities/pass_tag_request/list.html', {'username': request.user.username, 'pass_tag_request_list': pass_tag_requests})


@login_required(login_url='/login/')
def pass_tag_request_new(request):
    back_link = 'pass_tag_request_list'
    back_url = reverse_lazy(back_link)
    if request.method == "POST":
        form = PassTagRequestForm(request.POST)
        if form.is_valid():
            pass_tag_request = form.save(commit=False)
            pass_tag_request.save()
            if request.POST.get('action') == 'save':
                return redirect(back_link)
            else:
                return redirect(back_link, pk=pass_tag_request.pk)
    else:
        form = PassTagRequestForm()
    return render(request, 'entities/pass_tag_request/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


@login_required(login_url='/login/')
def pass_tag_request_edit(request, pk):
    back_link = 'pass_tag_request_list'
    back_url = reverse_lazy(back_link)
    pass_tag_request = get_object_or_404(PassTagRequest, pk=pk)
    PassTagRequestItemFormSet = inlineformset_factory(
        PassTagRequest, PassTagRequestItem, form=PassTagRequestItemForm, extra=1, can_delete=True
    )
    if request.method == 'POST':
        form = PassTagRequestForm(request.POST, instance=pass_tag_request)
        formset = PassTagRequestItemFormSet(request.POST, instance=pass_tag_request)
        for formset_item in formset:
            formset_item.fields['holder'].required = False
        if form.is_valid() and formset.is_valid():
            pass_tag_request = form.save(commit=False)
            pass_tag_request.save()
            for formset_item in formset:
                if formset_item.instance.pk and formset_item.cleaned_data['holder'] is None:
                    formset_item.instance.delete()
            items = formset.save()
            for item in items:
                if item.holder is None:
                    item.delete()
                else:
                    item.pass_tag_request = pass_tag_request
                    item.save()
            if request.POST.get('action') == 'save':
                return redirect(back_link)
            else:
                return redirect(back_link, pk=pk)
    else:
        form = PassTagRequestForm(instance=pass_tag_request)
        formset = PassTagRequestItemFormSet(instance=pass_tag_request)
    return render(request, 'entities/pass_tag_request/edit.html', {'username': request.user.username, 'form': form, 'formset': formset, 'back_url': back_url})
