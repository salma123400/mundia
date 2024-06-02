from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models
from AUTH_APP.forms import *
from offre_demande.models import *


class OffreDEmploiForm(forms.ModelForm):
    class Meta:
        model = OffreDEmploi
        fields = ['titre_poste', 'description', 'date_publication_present', 'date_limite_candidature', 'salaire_propose', 'competence']
        widgets = {
            'titre_poste': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_titre_poste', 'placeholder': 'Titre du Poste'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'id_description', 'placeholder': 'Description'}),
            'date_publication_present': forms.DateInput(attrs={'class': 'form-control', 'id': 'id_date_publication_present', 'placeholder': 'Date de Publication'}),
            'date_limite_candidature': forms.DateInput(attrs={'class': 'form-control', 'id': 'id_date_limite_candidature', 'placeholder': 'Date Limite de Candidature'}),
            'competence': forms.TextInput(attrs={'class': 'form-control', 'id':'id_competence' ,'placeholder': 'competence'}),
            'salaire_propose': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_salaire_propose', 'placeholder': 'Salaire Proposé'}),

        }



class DemandeDEmploiForm(forms.ModelForm):
    
    class Meta:
        model = DemandeDEmploi
        fields = ['description']

    def __init__(self, *args, **kwargs):
        super(DemandeDEmploiForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})

        # Fetch all competences
        competences = Competence.objects.all()

        if self.instance and self.instance.pk:
            # Get the candidat from the instance
            candidat = self.instance.user

            # Get all posseders related to this candidat
            posseders = Posseder.objects.filter(candidat=candidat)

            for i, posseder in enumerate(posseders):
                field_name_competence = f'competence_{posseder.id}'
                field_name_niveau_maitrise = f'niveau_maitrise_{posseder.id}'

                # Set choices for niveau_maitrise
                niveau_maitrise_choices = [
                    ('Tres Bien', 'Tres Bien'),
                    ('Bien', 'Bien'),
                    ('Moyenne', 'Moyenne'),
                    ('Debutant', 'Debutant')
                ]

                # Add competence field
                self.fields[field_name_competence] = forms.ChoiceField(
                    choices=[(competence.id_competence, competence.nom_competence) for competence in competences],
                    initial=posseder.id_competence.id_competence if posseder.id_competence else None,
                    widget=forms.Select(attrs={'class': 'form-control', 'id': field_name_competence})
                )
                self.fields[field_name_competence].label = f'Competence {i + 1}'

                # Add niveau_maitrise field
                self.fields[field_name_niveau_maitrise] = forms.ChoiceField(
                    choices=niveau_maitrise_choices,
                    initial=posseder.niveau_metrise if posseder.niveau_metrise else None,
                    widget=forms.Select(attrs={'class': 'form-control', 'id': field_name_niveau_maitrise})
                )
                self.fields[field_name_niveau_maitrise].label = f'Niveau Maitrise {i + 1}'

    def clean(self):
        cleaned_data = super().clean()
        competences_data = {
            key: value for key, value in cleaned_data.items() if key.startswith('competence_')
        }

        # Get the candidat from the instance
        candidat = self.instance.user

        # Check for duplicate competences
        existing_competences = set()
        for posseder in Posseder.objects.filter(candidat=candidat):
            existing_competences.add(posseder.id_competence_id)

        for field_name, competence_id in competences_data.items():
            if competence_id in existing_competences:
                self.add_error(None, f"Competence '{Competence.objects.get(id_competence=competence_id)}' already exists for this candidate.")

        return cleaned_data

    def save(self, commit=True):
        instance = super(DemandeDEmploiForm, self).save(commit=False)
        if commit:
            instance.save()

            # Update or create posseder entries
            competences_data = {
                key: value for key, value in self.cleaned_data.items() if key.startswith('competence_')
            }

            for field_name, competence_id in competences_data.items():
                posseder_id = field_name.split('_')[1]
                posseder, created = Posseder.objects.get_or_create(id=posseder_id, candidat=instance.user)
                posseder.id_competence_id = competence_id

                # Update niveau_maitrise
                niveau_maitrise_field_name = f'niveau_maitrise_{posseder_id}'
                posseder.niveau_metrise = self.cleaned_data[niveau_maitrise_field_name]

                posseder.save()

        return instance