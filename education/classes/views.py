from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

# Create your views here.

from .models import Student, ClassGroup, ClassGroupEnrollment
from .forms import StudentForm, ClassGroupForm, ClassGroupEnrollmentForm


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('student_list')
    template_name = 'student_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        student = self.get_object()
        class_group_enrollments = []
        dependencies = ClassGroupEnrollment.objects.filter(student=student)
        if dependencies.exists():
            class_group_enrollments = [str(dependency) for dependency in dependencies]
        if class_group_enrollments:
            return render(request, 'student_cannot_delete.html',
                          {'student': student, 'class_group_enrollment_list': class_group_enrollments})
        return super().get(request, *args, **kwargs)


@login_required(login_url='/login/')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'student_list': students})


@login_required(login_url='/login/')
def student_new(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_edit.html', {'form': form})


@login_required(login_url='/login/')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_edit.html', {'form': form})


class ClassGroupDelete(DeleteView):
    model = ClassGroup
    success_url = reverse_lazy('class_group_list')
    template_name = 'class_group_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        class_group = self.get_object()
        class_group_enrollments = []
        dependencies = ClassGroupEnrollment.objects.filter(class_group=class_group)
        if dependencies.exists():
            class_group_enrollments = [str(dependency) for dependency in dependencies]
        if class_group_enrollments:
            return render(request, 'class_group_cannot_delete.html', {'class_group': class_group, 'class_group_enrollment_list': class_group_enrollments})
        return super().get(request, *args, **kwargs)


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


class ClassGroupEnrollmentDelete(DeleteView):
    model = ClassGroupEnrollment
    success_url = reverse_lazy('class_group_enrollment_list')
    template_name = 'class_group_enrollment_confirm_delete.html'


@login_required(login_url='/login/')
def class_group_enrollment_list(request):
    class_group_enrollments = ClassGroupEnrollment.objects.all()
    return render(request, 'class_group_enrollment_list.html', {'class_group_enrollment_list': class_group_enrollments})


@login_required(login_url='/login/')
def class_group_enrollment_new(request):
    if request.method == "POST":
        form = ClassGroupEnrollmentForm(request.POST)
        if form.is_valid():
            class_group_enrollment = form.save(commit=False)
            class_group_enrollment.save()
            return redirect('class_group_enrollment_list')
    else:
        form = ClassGroupEnrollmentForm()
    return render(request, 'class_group_enrollment_edit.html', {'form': form})


@login_required(login_url='/login/')
def class_group_enrollment_edit(request, pk):
    class_group_enrollment = get_object_or_404(ClassGroupEnrollment, pk=pk)
    if request.method == 'POST':
        form = ClassGroupEnrollmentForm(request.POST, instance=class_group_enrollment)
        if form.is_valid():
            class_group_enrollment = form.save(commit=False)
            class_group_enrollment.save()
            return redirect('class_group_enrollment_list')
    else:
        form = ClassGroupEnrollmentForm(instance=class_group_enrollment)
    return render(request, 'class_group_enrollment_edit.html', {'form': form})
