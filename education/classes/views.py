from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.forms import inlineformset_factory

# Create your views here.

from .models import Student, ClassGroup, ClassGroupEnrollment, ClassGroupEnrollmentItem, ClassGroupEnrollmentRegistryItem
from .forms import StudentForm, ClassGroupForm, ClassGroupEnrollmentForm, ClassGroupEnrollmentItemForm

from education.metadata import get_dependencies


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('student_list')
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
def student_list(request):
    students = Student.objects.all()
    return render(request, 'entities/student/list.html', {'username': request.user.username, 'student_list': students})


@login_required(login_url='/login/')
def student_new(request):
    back_link = 'student_list'
    back_url = reverse_lazy(back_link)
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect(back_link)
    else:
        form = StudentForm()
    return render(request, 'entities/student/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


@login_required(login_url='/login/')
def student_edit(request, pk):
    back_link = 'student_list'
    back_url = reverse_lazy(back_link)
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect(back_link)
    else:
        form = StudentForm(instance=student)
    return render(request, 'entities/student/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


class ClassGroupDelete(DeleteView):
    model = ClassGroup
    success_url = reverse_lazy('class_group_list')
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
def class_group_list(request):
    class_groups = ClassGroup.objects.all()
    return render(request, 'entities/class_group/list.html', {'username': request.user.username, 'class_group_list': class_groups})


@login_required(login_url='/login/')
def class_group_new(request):
    back_link = 'class_group_list'
    back_url = reverse_lazy(back_link)
    if request.method == "POST":
        form = ClassGroupForm(request.POST)
        if form.is_valid():
            class_group = form.save(commit=False)
            class_group.save()
            return redirect(back_link)
    else:
        form = ClassGroupForm()
    return render(request, 'entities/class_group/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


@login_required(login_url='/login/')
def class_group_edit(request, pk):
    back_link = 'class_group_list'
    back_url = reverse_lazy(back_link)
    class_group = get_object_or_404(ClassGroup, pk=pk)
    if request.method == 'POST':
        form = ClassGroupForm(request.POST, instance=class_group)
        if form.is_valid():
            class_group = form.save(commit=False)
            class_group.save()
            return redirect(back_link)
    else:
        form = ClassGroupForm(instance=class_group)
    return render(request, 'entities/class_group/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


class ClassGroupEnrollmentDelete(DeleteView):
    model = ClassGroupEnrollment
    success_url = reverse_lazy('class_group_enrollment_list')
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
        ClassGroupEnrollmentRegistryItem.objects.filter(class_group_enrollment=object_to_delete).delete()
        return super().get(request, *args, **kwargs)


@login_required(login_url='/login/')
def class_group_enrollment_list(request):
    class_group_enrollments = ClassGroupEnrollment.objects.all()
    return render(request, 'entities/class_group_enrollment/list.html', {'username': request.user.username, 'class_group_enrollment_list': class_group_enrollments})


@login_required(login_url='/login/')
def class_group_enrollment_new(request):
    back_link = 'class_group_enrollment_list'
    back_url = reverse_lazy(back_link)
    if request.method == "POST":
        form = ClassGroupEnrollmentForm(request.POST)
        if form.is_valid():
            class_group_enrollment = form.save(commit=False)
            class_group_enrollment.save()
            ClassGroupEnrollmentRegistryItem.objects.filter(class_group_enrollment=class_group_enrollment).delete()
            if request.POST.get('action') == 'save':
                return redirect(back_link)
            else:
                return redirect('class_group_enrollment_edit', pk=class_group_enrollment.pk)
    else:
        form = ClassGroupEnrollmentForm()
    return render(request, 'entities/class_group_enrollment/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


@login_required(login_url='/login/')
def class_group_enrollment_edit(request, pk):
    back_link = 'class_group_enrollment_list'
    back_url = reverse_lazy(back_link)
    class_group_enrollment = get_object_or_404(ClassGroupEnrollment, pk=pk)
    PassTagRequestItemFormSet = inlineformset_factory(
        ClassGroupEnrollment, ClassGroupEnrollmentItem, form=ClassGroupEnrollmentItemForm, extra=40, can_delete=True
    )
    if request.method == 'POST':
        form = ClassGroupEnrollmentForm(request.POST, instance=class_group_enrollment)
        formset = PassTagRequestItemFormSet(request.POST, instance=class_group_enrollment)
        for formset_item in formset:
            formset_item.fields['student'].required = False
        if form.is_valid() and formset.is_valid():
            class_group_enrollment = form.save(commit=False)
            class_group_enrollment.save()
            ClassGroupEnrollmentRegistryItem.objects.filter(class_group_enrollment=class_group_enrollment).delete()
            for formset_item in formset:
                if formset_item.instance.pk and formset_item.cleaned_data['student'] is None:
                    formset_item.instance.delete()
            items = formset.save()
            print(items)
            for item in items:
                if item.student is None:
                    item.delete()
                else:
                    item.class_group_enrollment = class_group_enrollment
                    item.save()
            class_group_enrollment_items = ClassGroupEnrollmentItem.objects.filter(class_group_enrollment=class_group_enrollment)
            for class_group_enrollment_item in class_group_enrollment_items:
                    ClassGroupEnrollmentRegistryItem.objects.create(
                        class_group_enrollment=class_group_enrollment,
                        enrollment_date=class_group_enrollment.enrollment_date,
                        student=class_group_enrollment_item.student,
                        class_group=class_group_enrollment_item.class_group
                    )
            if request.POST.get('action') == 'save':
                return redirect(back_link)
            else:
                return redirect('class_group_enrollment_edit', pk=pk)
    else:
        form = ClassGroupEnrollmentForm(instance=class_group_enrollment)
        formset = PassTagRequestItemFormSet(instance=class_group_enrollment)
    return render(request, 'entities/class_group_enrollment/edit.html', {'username': request.user.username, 'form': form, 'formset': formset, 'back_url': back_url})
