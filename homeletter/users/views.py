from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.views import View
# from django.contrib.auth import hashers
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.core.files.storage import FileSystemStorage # for manually upload files
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from .forms import RegistrationForm, LoginForm, UserForm, ProfileForm
from .models import User, Profile
from django.shortcuts import get_object_or_404
# Create your views here.


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
            #check user
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


# update User Model and profile
class UpdateView(View):
    template_name = "users/update.html"

    def post(self, request, pk):
        uf = UserForm(request.POST,instance=User())
        upf = ProfileForm(request.POST, instance=Profile())

        if uf.is_valid() and upf.is_valid():
            uf.save()
            upf.save()
            messages.success(request, _('Your profile was successfully updated!'))

        # get user and profile
        user = get_object_or_404(User, pk=pk)
        profile = user.profile
        photo_url = profile.photo.url if profile.photo else ''  # photo url
        return render(request, self.template_name, {'uf': uf, 'upf': upf, 'photo': photo_url})

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
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
        return render(request, self.template_name, {'uf': uf, 'upf': upf, 'photo': photo_url })






"""
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


    //in html
    <form method="post">
      {% csrf_token %}
      {{ user_form.as_p }}
      {{ profile_form.as_p }}
      <button type="submit">Save changes</button>
    </form>

    users = User.objects.all().select_related('profile')
    REF:
    https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    https://mayukhsaha.wordpress.com/2013/05/09/simple-login-and-user-registration-application-using-django/
    http://musings.tinbrain.net/blog/2014/sep/21/registration-django-easy-way/
"""