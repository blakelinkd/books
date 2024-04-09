from django.shortcuts import redirect, render
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup:success')
    else:
        form = SignupForm()

    return render(request, 'signup/index.html', {'form': form})

def success(request):
    return render(request, 'signup/success.html')