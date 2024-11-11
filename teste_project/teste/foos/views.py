from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from foos.forms import FooForm
from foos.models import Foo


def foo_list(request):
    pre_context = {
        "card_title": "Lista de Foos",
    }
    context = {
        'foo_list': Foo.objects.all()
    }
    return render(request, 'foos/foo_list.html', {**pre_context, **context})


def foo_create(request):
    pre_context = {
        "card_title": "Recinto",
    }

    if request.method == 'GET':
        context = {
            "form": FooForm(),
        }

    if request.method == 'POST':
        form = FooForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.custom_save(request)
            return redirect('foo_list')
        else:
            context = {
                "form": form,
            }

    return render(request, 'foos/foo.html', {**pre_context, **context})


def foo_update(request, pk):
    pre_context = {
        "card_title": "Lista de Tipos de Ocorrências",
    }

    obj = get_object_or_404(Foo, id=pk)

    if request.method == 'GET':
        context = {
            "form": FooForm(instance=obj),
        }

    if request.method == 'POST':
        form = FooForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.custom_update(request)
            return redirect('foo_list')
        else:
            context = {
                "form": form,
            }

    return render(request, 'foos/foo.html', {**pre_context, **context})


def foo_delete(request, pk):
    obj = Foo.objects.get(id=pk)
    obj.custom_delete(request)
    return redirect('foo_list')
