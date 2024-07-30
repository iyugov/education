from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView


# Create your views here.

from .models import PassTag, PassTagRequest
from .forms import PassTagForm, PassTagRequestForm


class PassTagDelete(DeleteView):
    model = PassTag
    success_url = reverse_lazy('pass_tag_list')
    template_name = 'entities/pass_tag/confirm_delete.html'
    """
    def get(self, request, *args, **kwargs):
        pass_tag = self.get_object()
        pass_tag_requests = []
        dependencies = PassTagRequest.objects.filter(card=pass_tag)
        if dependencies.exists():
            pass_card_issues = [str(dependency) for dependency in dependencies]
        if pass_card_issues:
            return render(request, 'entities/pass_tag/cannot_delete.html', {'username': request.user.username, 'pass_tag': pass_tag, 'pass_card_issue_list': pass_card_issues})
        return super().get(request, *args, **kwargs)
"""


@login_required(login_url='/login/')
def pass_tag_list(request):
    pass_tags = PassTag.objects.all()
    return render(request, 'entities/pass_tag/list.html', {'username': request.user.username, 'pass_tag_list': pass_tags})


@login_required(login_url='/login/')
def pass_tag_new(request):
    if request.method == "POST":
        form = PassTagForm(request.POST)
        if form.is_valid():
            pass_tag = form.save(commit=False)
            pass_tag.save()
            return redirect('pass_tag_list')
    else:
        form = PassTagForm()
    return render(request, 'entities/pass_tag/edit.html', {'username': request.user.username, 'form': form})


@login_required(login_url='/login/')
def pass_tag_edit(request, pk):
    pass_tag = get_object_or_404(PassTag, pk=pk)
    if request.method == 'POST':
        form = PassTagForm(request.POST, instance=pass_tag)
        if form.is_valid():
            pass_tag = form.save(commit=False)
            pass_tag.save()
            return redirect('pass_tag_list')
    else:
        form = PassTagForm(instance=pass_tag)
    return render(request, 'entities/pass_tag/edit.html', {'username': request.user.username, 'form': form})


class PassTagRequestDelete(DeleteView):
    model = PassTagRequest
    success_url = reverse_lazy('pass_tag_request_list')
    template_name = 'entities/pass_tag_request/confirm_delete.html'


@login_required(login_url='/login/')
def pass_tag_request_list(request):
    pass_tag_requests = PassTagRequest.objects.all()
    return render(request, 'entities/pass_tag_request/list.html', {'username': request.user.username, 'pass_tag_request_list': pass_tag_requests})


@login_required(login_url='/login/')
def pass_tag_request_new(request):
    if request.method == "POST":
        form = PassTagRequestForm(request.POST)
        if form.is_valid():
            pass_tag_request = form.save(commit=False)
            pass_tag_request.save()
            return redirect('pass_tag_request_list')
    else:
        form = PassTagRequestForm()
    return render(request, 'entities/pass_tag_request/edit.html', {'username': request.user.username, 'form': form})


@login_required(login_url='/login/')
def pass_tag_request_edit(request, pk):
    pass_tag_request = get_object_or_404(PassTagRequest, pk=pk)
    if request.method == 'POST':
        form = PassTagRequestForm(request.POST, instance=pass_tag_request)
        if form.is_valid():
            pass_tag_request = form.save(commit=False)
            pass_tag_request.save()
            return redirect('pass_tag_request_list')
    else:
        form = PassTagRequestForm(instance=pass_tag_request)
    return render(request, 'entities/pass_tag_request/edit.html', {'username': request.user.username, 'form': form})
