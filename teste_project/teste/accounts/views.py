from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from accounts.forms import CustomUserForm, CustomUserLoginForm, ChangePasswordForm, GroupForm, CustomUserUpdateForm, \
    CustomUserReadonlyForm
from accounts.models import Account

default_password = 'Ictb@1234'


def account_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    pre_context = {

    }

    if request.method == 'GET':
        context = {
            'form': CustomUserForm(),
        }

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registrado com sucesso.')
            return redirect('account_login')

    return render(request, 'accounts/register.html', {**pre_context, **context})


def account_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        form = CustomUserLoginForm()

    if request.method == 'POST':

        # Caso senha incorreta, mantem username na tela
        request.session['username'] = request.POST['username']

        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                login(request, user)

                # se senha for senha padrao, redireciona para pagina de mudança de senha
                if user.check_password(default_password):
                    return redirect('account_change_password')

                return redirect('home')
        else:
            pass
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def account_logout(request):
    logout(request)
    return redirect('account_login')


@login_required
def home(request):
    context = {

    }
    return render(request, 'accounts/home.html', context)


@login_required
def account_list(request):
    pre_context = {
        "card_title": "Lista de Usuários",
    }
    context = {
        'account_list': Account.objects.all()
    }
    return render(request, 'accounts/account_list.html', {**pre_context, **context})


@login_required
def account_read(request, pk):
    context = {
        'account': Account.objects.get(id=pk)
    }
    return render(request, 'accounts/account_view.html', context)


@login_required
def account_update(request, pk):
    obj = get_object_or_404(Account, id=pk)
    if request.method == 'POST':
        account_status = request.POST.get('status', False)

        group = Group.objects.get(id=request.POST['grupo'])
        group.user_set.add(obj)

        obj.is_active = account_status

        obj.save()

        return redirect('account_list')

    context = {
        'readonly_form': CustomUserReadonlyForm(instance=obj),
        'form': CustomUserUpdateForm(instance=obj),
        'is_edit': True,
        'account': obj,
        'group_list': Group.objects.all(),
    }
    return render(request, 'accounts/account.html', context)


@login_required
def account_delete(request, pk):
    obj = Account.objects.get(id=pk)
    # se usuario nunca logou na conta
    if obj.date_joined == obj.last_login:
        obj.delete()
    return redirect('account_list')


@login_required
def account_reset_password(request, pk):
    obj = Account.objects.get(id=pk)
    obj.set_password(default_password)
    obj.save()
    messages.success(request, 'Senha redefinida com sucesso. Ultilize "' + default_password + '" no proximo acesso.')
    return redirect('account_update', pk)


@login_required
def account_change_password(request):
    pre_context = {
        'card_title': 'Redefinir senha',
    }

    if request.method == 'GET':
        context = {
            'form': ChangePasswordForm(request.user),
        }

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('login')
        else:
            context = {
                'form': form,
            }
    return render(request, 'accounts/change_password.html', {**pre_context, **context})


@login_required
def group_list(request):
    pre_context = {
        "card_title": "Lista de Grupo",
    }
    context = {
        'group_list': Group.objects.all()
    }
    return render(request, 'accounts/group_list.html', {**pre_context, **context})


@login_required
def group_read(request, pk):
    pre_context = {
        "card_title": "Grupo",
    }

    obj = get_object_or_404(Group, id=pk)

    context = {
        "is_view": True,
        "form": GroupForm(instance=obj, readonly=True),
    }
    return render(request, 'accounts/group.html', {**pre_context, **context})


@login_required
def group_create(request):
    pre_context = {
        "card_title": "Grupo",
    }

    if request.method == 'GET':
        context = {
            "form": GroupForm(),
        }

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            return redirect('group_list')
        else:
            context = {
                "form": form,
            }

    return render(request, 'accounts/group.html', {**pre_context, **context})


@login_required
def group_update(request, pk):
    pre_context = {
        "card_title": "Grupo",
    }

    obj = get_object_or_404(Group, id=pk)

    if request.method == 'GET':
        context = {
            "form": GroupForm(instance=obj),
        }

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            return redirect('group_list')
        else:
            context = {
                "form": form,
            }

    return render(request, 'accounts/group.html', {**pre_context, **context})


@login_required
def group_delete(request, pk):
    obj = get_object_or_404(Group, id=pk)
    if obj.delete():
        return redirect('group_list')
    return redirect('group_update', obj.id)
