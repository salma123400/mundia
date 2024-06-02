from django.shortcuts import render, redirect,get_object_or_404
from django.http import Http404
from django.contrib import messages
from .models import OffreDEmploi
from AUTH_APP.forms import  RecruteurForm ,CandidatUpdateForm,CandidatForm,RecruteurUpdateForm
from offre_demande.models import *
from .forms import *


def dashboard(request):
    # Vérifier si l'utilisateur actuel est un recruteur
    if not hasattr(request.user, 'recruteur'):
        raise Http404("Vous n'êtes pas autorisé à accéder à cette page.")
    
    # Filtrer les offres d'emploi par le recruteur authentifié
    recruteur = request.user.recruteur
    item = OffreDEmploi.objects.filter(recruteur=recruteur)
    
    return render(request, 'dashboard.html', {'postes':item})


def delete_OffreDEmploi(request, pk):
    #OffreDEmploi = get_object_or_404(OffreDEmploi, id=id_offre)
    OffreDEmploi.objects.get(id_offre=pk).delete()
    #OffreDEmploi.delete()
    return redirect('dashboard')




def modify_OffreDEmploi(request, pk):
    offre = get_object_or_404(OffreDEmploi, pk=pk)
    if request.method == "POST":
        form = OffreDEmploiForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Remplacez 'dashboard' par le nom réel de votre vue du tableau de bord
    else:
        form = OffreDEmploiForm(instance=offre)
    return render(request, 'modify_OffreDEmploi.html', {'form': form, 'OffreDEmploi': offre})





def dashboard_c(request):

    if not hasattr(request.user, 'candidat'):
        raise Http404("Vous n'êtes pas autorisé à accéder à cette page.")





    demandes = DemandeDEmploi.objects.all().filter(user=request.user.candidat).order_by('-date_soumission')

    if not demandes.exists():
        demandes = []

    for demande in demandes:
        demande.posseder_data = Posseder.objects.filter(candidat=demande.user)

    return render(request, 'dashboard_c.html', {'demandes': demandes})


def delete_DemandeDEmploi(request, pk):
    #OffreDEmploi = get_object_or_404(OffreDEmploi, id=id_offre)
    demande = get_object_or_404(DemandeDEmploi, pk=pk, user=request.user.candidat)    
    demande.delete()
    #OffreDEmploi.delete()
    return redirect('dashboard_c')




def modify_DemandeDEmploi(request, pk):
    demande = get_object_or_404(DemandeDEmploi, pk=pk)
    if request.method == 'POST':
        form = DemandeDEmploiForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            return redirect('dashboard_c')  # Replace with your desired redirect URL
    else:
        form = DemandeDEmploiForm(instance=demande)
    return render(request, 'modify_DemandeDEmploi.html', {'form': form})
