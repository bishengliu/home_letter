from django.shortcuts import render
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import hashers



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

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # save user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=hashers.make_password(form.cleaned_data['password1']),
                email=form.cleaned_data['email']
            )

            # save profile
            profile = Profile.object().create(
                user=user,
                birth_date=form.cleaned_data['birth_date'],
                photo=form.cleaned_data['photo']
            )

            #login user






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
"""