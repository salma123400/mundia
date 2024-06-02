from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomLoginForm
from django.urls import reverse
from .models import *
from .forms import *


def home(request):
    return render(request, 'home.html',{})


def sign_upc(request):
    if request.user.is_authenticated:
        return redirect('base')
    else:
        if request.method == "POST":
            form = CandidatForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been created successfully!')
                return redirect('sign_upc')   
            else:           
                messages.error(request, "There was a problem creating your account!")
        else:
            form = CandidatForm()
        return render(request, 'sign_upc.html', {'form' : form})

def sign_upr(request):
    if request.user.is_authenticated:
        return redirect('base')
    else:
        if request.method == "POST":
            form = RecruteurForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been created successfully!')
                return redirect('sign_upr')   
            else:           
                messages.error(request, "There was a problem creating your account!")
        else:
            form = RecruteurForm()
        return render(request, 'sign_upr.html', {'form' : form})
    
    
class CustomLoginView(LoginView):
    form_class = CustomLoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            user = authenticate(request=request, username=form.cleaned_data['email'], password=form.cleaned_data['motdepass'])
            if user is not None:
                login(request, user)
                return redirect('navbar')  # Redirect to the desired page after successful login
        else:
            messages.error(request, "Invalid email or password!")
        return render(request, 'login.html', {'form': form})




def update_candidat(request):
    try:
        # Get the existing Candidat instance associated with the logged-in user
        candidat = get_object_or_404(Candidat, user=request.user)

        if request.method == 'POST':
            # Initialize form with POST data and the existing instance
            form = CandidatUpdateForm(request.POST, instance=candidat)
            if form.is_valid():
                candidat = form.save(commit=False)
                user = candidat.user
                user.username = form.cleaned_data['email'].split('@')[0]
                user.email = form.cleaned_data['email']
                user.save()
                candidat.save()
                user = authenticate(request=request, username=form.cleaned_data['email'], password=form.cleaned_data['motdepass'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Profile updated successfully !')
                    return render(request,'update_candidat.html',{'form' : CandidatUpdateForm(instance=candidat)}) 
                else:
                    messages.error(request, "There was a problem updating your profile !")
                    return render(request,'update_candidat.html',{'form' : CandidatUpdateForm(instance=candidat)})
            else:
                messages.error(request, 'There was a problem updating your profile!')
        else:
            # Initialize form with the existing instance
            form = CandidatUpdateForm(instance=candidat)

        return render(request, 'update_candidat.html', {'form': form})

    except Candidat.DoesNotExist:
        messages.error(request, 'Candidat profile does not exist.')
        return redirect(reverse('login'))

    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect(reverse('login'))

def update_recruteur(request):
    try:
        # Get the existing Candidat instance associated with the logged-in user
        recruteur = get_object_or_404(Recruteur, user=request.user)

        if request.method == 'POST':
            # Initialize form with POST data and the existing instance
            form = RecruteurUpdateForm(request.POST, instance=recruteur)
            if form.is_valid():
                recruteur = form.save(commit=False)
                user = recruteur.user
                user.username = form.cleaned_data['email'].split('@')[0]
                user.email = form.cleaned_data['email']
                user.save()
                recruteur.save()
                user = authenticate(request=request, username=form.cleaned_data['email'], password=form.cleaned_data['motdepass'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Profile updated successfully !')
                    return render(request,'update_recruteur.html',{'form' : RecruteurUpdateForm(instance=recruteur)}) 
                else:
                    messages.error(request, "There was a problem updating your profile !")
                    return render(request,'update_recruteur.html',{'form' : RecruteurUpdateForm(instance=recruteur)})
            else:
                messages.error(request, 'There was a problem updating your profile!')
        else:
            # Initialize form with the existing instance
            form = RecruteurUpdateForm(instance=recruteur)

        return render(request, 'update_recruteur.html', {'form': form})

    except Recruteur.DoesNotExist:
        messages.error(request, 'Candidat profile does not exist.')
        return redirect(reverse('login'))

    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect(reverse('login'))




def logoutUser(request):
    logout(request)
    return redirect(reverse('login'))