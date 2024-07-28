from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

# Create your views here.

from .models import ClassGroup
from .forms import ClassGroupForm

class ClassGroupDelete(DeleteView):
    model = ClassGroup
    success_url = reverse_lazy('class_group_list')
    template_name = 'class_group_confirm_delete.html'


@login_required(login_url='/login/')
def class_group_list(request):
    class_groups = ClassGroup.objects.all()
    return render(request, 'class_group_list.html', {'class_group_list': class_groups})

@login_required(login_url='/login/')
def class_group_new(request):
    if request.method == "POST":
        form = ClassGroupForm(request.POST)
        if form.is_valid():
            class_group = form.save(commit=False)
            class_group.save()
            return redirect('class_group_list')
    else:
        form = ClassGroupForm()
    return render(request, 'class_group_edit.html', {'form': form})

@login_required(login_url='/login/')
def class_group_edit(request, pk):
    class_group = get_object_or_404(ClassGroup, pk=pk)
    if request.method == 'POST':
        form = ClassGroupForm(request.POST, instance=class_group)
        if form.is_valid():
            class_group = form.save(commit=False)
            class_group.save()
            return redirect('class_group_list')
    else:
        form = ClassGroupForm(instance=class_group)
    return render(request, 'class_group_edit.html', {'form': form})
