from django.shortcuts import render
from .forms import ProfileForm
from .models import Profile

def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    print(profile.avatar.url)

    if form.is_valid():
        form.save()
        confirm = True
    
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'Profile/main.html', context)
