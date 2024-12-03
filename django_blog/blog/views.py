from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.
class RegisterView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'register.html'
    success_url = reverse_lazy('login/')

@login_required()
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('profile/')
    else:
        form = ProfileForm()
    return render(request, 'profile_edit.html', {'form': form})
@login_required()
def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'profile.html', {'profile': profile})