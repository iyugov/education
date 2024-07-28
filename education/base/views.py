from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView


# Create your views here.

from .models import Individual
from .forms import IndividualForm

from pass_cards.models import PassCardIssue
from classes.models import ClassGroupEnrollment


class IndividualDelete(DeleteView):
    model = Individual
    success_url = reverse_lazy('individual_list')
    template_name = 'individual_confirm_delete.html'
    
    def get(self, request, *args, **kwargs):
        individual = self.get_object()
        pass_card_issues = []
        dependencies = PassCardIssue.objects.filter(individual=individual)
        if dependencies.exists():
            pass_card_issues = [str(dependency) for dependency in dependencies]
        class_group_enrollments = []
        dependencies = ClassGroupEnrollment.objects.filter(student=individual)
        if dependencies.exists():
            class_group_enrollments = [str(dependency) for dependency in dependencies]
        if pass_card_issues or class_group_enrollments:
            return render(request, 'individual_cannot_delete.html', {'individual': individual, 'pass_card_issue_list': pass_card_issues, 'class_group_enrollment_list': class_group_enrollments})
        return super().get(request, *args, **kwargs)


@login_required(login_url='/login/')
def individual_list(request):
    individuals = Individual.objects.all()
    return render(request, 'individual_list.html', {'individual_list': individuals})


@login_required(login_url='/login/')
def individual_new(request):
    if request.method == "POST":
        form = IndividualForm(request.POST)
        if form.is_valid():
            individual = form.save(commit=False)
            individual.save()
            return redirect('individual_list')
    else:
        form = IndividualForm()
    return render(request, 'individual_edit.html', {'form': form})


@login_required(login_url='/login/')
def individual_edit(request, pk):
    individual = get_object_or_404(Individual, pk=pk)
    if request.method == 'POST':
        form = IndividualForm(request.POST, instance=individual)
        if form.is_valid():
            individual = form.save(commit=False)
            individual.save()
            return redirect('individual_list')
    else:
        form = IndividualForm(instance=individual)
    return render(request, 'individual_edit.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'logout.html', {})


def home(request):
    return render(request, 'home.html', {})
