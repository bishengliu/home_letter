from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import hashers
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.db import transaction

from .forms import RegistrationForm, UserForm, ProfileForm
from .models import User, Profile
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
            username = form.cleaned_data['username']
            password = hashers.make_password(form.cleaned_data['password1'])
            email = form.cleaned_data['email']
            # save user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

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
                photo=request.FILES['photo']  # auto upload file
            )
            # login user
            user = authenticate(username=username, password=password)
            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('home')

        return render(request, self.template_name, {'form': form})


# update User Model and profile
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