from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.core.files.storage import FileSystemStorage # for manually upload files
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from .forms import RegistrationForm, LoginForm, UserForm, ProfileForm
from .models import User, Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


# register user
class RegisterView(View):
    form_class = RegistrationForm
    template_name = "users/register.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    @transaction.atomic
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            # save user
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User(username=username,email=email,first_name=first_name,last_name=last_name)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            # save profile
            '''
            # need to process file upload
            # we can manually upload files
            img = request.FILES['photo']
            if img:
                fs = FileSystemStorage()
                filename = fs.save(img.name, img)
                saved_url = fs.url(filename)

            profile = Profile(
                ser=user,
                birth_date=form.cleaned_data['birth_date'],
                #photo=saved_url # use this if I need to change the name of the file upload
            )
            profile.save()
            '''

            Profile.objects.create(
                user=user,
                birth_date=form.cleaned_data['birth_date'],
                photo=request.FILES['photo'] if request.FILES else None   # auto upload file
            )
            # login user
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')

        return render(request, self.template_name, {'form': form})


# login user
class LoginView(View):
    form_class = LoginForm
    template_name = "users/login.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data.get('password')
            # authenticate
            user = authenticate(username=username, password=password)
            # check user
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.add_message(request, messages.WARNING,
                                         _('User is disabled!'))
                    return redirect('users:login')
            else:
                messages.add_message(request, messages.WARNING, _('Login Failed, password was incorrect!'))
                return redirect('users:login')
        return render(request, self.template_name, {'form': form})


# logout user
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')


# update user model and profile
class UpdateView(LoginRequiredMixin, View):
    template_name = "users/update.html"

    @transaction.atomic
    def post(self, request, pk):
        uf = UserForm(request.POST)
        upf = ProfileForm(request.POST)

        if uf.is_valid() and upf.is_valid():
            # update user info
            user = get_object_or_404(User, pk=pk)
            user.first_name = uf.cleaned_data['first_name']
            user.last_name = uf.cleaned_data['last_name']
            user.email = uf.cleaned_data['email']
            user.save()
            # update profile
            profile = user.profile
            profile.birth_date = upf.cleaned_data['birth_date']
            profile.user = user
            if request.FILES:
                if profile.photo:
                    profile.photo.delete()
                profile.photo = request.FILES['photo']
            profile.save()

            messages.success(request, _('Your profile was successfully updated!'))

        # get user and profile
        user = get_object_or_404(User, pk=pk)
        profile = user.profile
        photo_url = profile.photo.url if profile.photo else ''  # photo url
        uf = UserForm(instance=user)
        upf = ProfileForm(instance=profile)
        return render(request, self.template_name, {'uf': uf, 'upf': upf, 'photo': photo_url})

    def get(self, request, pk):
        # check the user
        user = request.user
        try:
            u = User.objects.get(pk=pk)
            if u.pk != user.pk:
                messages.warning(request, 'Permission Denied!')
                return redirect('home')
        except User.DoesNotExist:
            messages.warning(request, 'Permission Denied!')
            return redirect('home')

        # get the profile
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            # create profile if not exist
            profile = Profile.objects.create(
                user=user,
                photo=None  # auto upload file
            )
        upf = ProfileForm(instance=profile)
        photo_url = profile.photo.url if profile.photo else ''
        uf = UserForm(instance=user)
        return render(request, self.template_name, {'uf': uf, 'upf': upf, 'photo': photo_url})
