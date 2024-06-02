from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django import forms
from .models import *
import re

class CustomLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    motdepass = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('motdepass')

        if email and password:
            user = authenticate(request=self.request, username=email, password=password)
            if not user:
                raise forms.ValidationError('Invalid email or password')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
    
class CandidatForm(forms.ModelForm):
    motdepass_confirm = forms.CharField(widget=forms.PasswordInput)
    motdepass = forms.CharField(widget=forms.PasswordInput)

    
    class Meta:
        model = Candidat
        fields = ["nom", "prenom", "address", "num_telephone", "presentation", "email", "motdepass"]
    
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        email = cleaned_data['email']
        base_username = slugify(email.split('@')[0])
        username = base_username
        counter = 1

        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}-{counter}"
            counter += 1

        user = CustomUser(
            username=username,
            email=email,
            password=make_password(cleaned_data['motdepass'])
        )
        if commit:
            user.save()
        
        candidat = super().save(commit=False)
        candidat.user = user
        if commit:
            candidat.save()
        return candidat
        
    def clean_motdepass(self):
        motdepass = self.cleaned_data.get('motdepass')
        
        if len(motdepass) < 8 or len(motdepass) > 16:
            raise ValidationError('Password must be between 8 and 16 characters.')
        if not re.search(r'[A-Z]', motdepass):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', motdepass):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', motdepass):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[\W_]', motdepass):  
            raise ValidationError('Password must contain at least one special character.')
        
        return motdepass
    
    
    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if not re.match(r'^[a-zA-Z]+$', nom):
            raise ValidationError('First name can only contain letters.')
        return nom
    
    def clean_num_telephone(self):
        num_telephone = self.cleaned_data.get('num_telephone')
        if not num_telephone.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        if len(num_telephone) != 10:
            raise ValidationError('Phone number must be 10 digits long.')
        return num_telephone
    
    def clean_prenom(self):
        prenom = self.cleaned_data.get('prenom')
        if not re.match(r'^[a-zA-Z]+$', prenom):
            raise ValidationError('Last name can only contain letters.')
        return prenom
    

    
    
    def clean(self):
        cleaned_data = super().clean()
        num_telephone = cleaned_data.get('num_telephone')
        nom = cleaned_data.get('nom')
        prenom = cleaned_data.get('prenom')
        email = cleaned_data.get('email')
        motdepass = cleaned_data.get('motdepass')
        motdepass_confirm = cleaned_data.get('motdepass_confirm')

        if email and Candidat.objects.filter(email=email).exists() and email or Recruteur.objects.filter(email=email).exists():
            self.add_error('email', 'This email already exists.')

        if num_telephone and Candidat.objects.filter(num_telephone=num_telephone).exists() or Recruteur.objects.filter(num_telephone=num_telephone).exists():
            self.add_error('num_telephone', 'This phone number already exists.')
            
            
        if not nom and not prenom:
            pass    
        
        elif nom and prenom and Candidat.objects.filter(nom=nom, prenom=prenom).exists():
            self.add_error('nom', 'This first name already exists.')
            self.add_error('prenom', 'This last name already exists.')

        elif nom and prenom and Candidat.objects.filter(nom=prenom, prenom=nom).exists() :
            self.add_error('nom', 'This first name already exists.')
            self.add_error('prenom', 'This last name already exists.')
            
        elif nom == prenom :
            self.add_error('nom', 'You cant put youre first name the same as youre last name.')
            self.add_error('prenom', 'You cant put youre last name the same as youre first name.')
            
        if motdepass and motdepass_confirm and motdepass != motdepass_confirm:
            self.add_error('motdepass_confirm', 'Passwords do not match.')
            self.add_error('motdepass', 'Passwords do not match.')
        
        return cleaned_data
    
    
    
    
    
class CandidatUpdateForm(forms.ModelForm):
    motdepass = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Candidat
        fields = ["nom", "prenom", "address", "num_telephone", "presentation", "email"]

    def clean_motdepass(self):
        motdepass = self.cleaned_data.get('motdepass')
        if len(motdepass) < 8 or len(motdepass) > 16:
            raise ValidationError('Password must be between 8 and 16 characters.')
        if not re.search(r'[A-Z]', motdepass):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', motdepass):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', motdepass):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[\W_]', motdepass):  
            raise ValidationError('Password must contain at least one special character.')
        if not self.instance.user.check_password(motdepass):
            raise forms.ValidationError('Incorrect password.')
        return motdepass

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if not re.match(r'^[a-zA-Z]+$', nom):
            raise ValidationError('First name can only contain letters.')
        return nom

    def clean_prenom(self):
        prenom = self.cleaned_data.get('prenom')
        if not re.match(r'^[a-zA-Z]+$', prenom):
            raise ValidationError('Last name can only contain letters.')
        return prenom

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Candidat.objects.exclude(pk=self.instance.pk).filter(email=email).exists() or Recruteur.objects.filter(email=email).exists():
            raise ValidationError('This email already exists.')
        return email

    def clean_num_telephone(self):
        num_telephone = self.cleaned_data.get('num_telephone')
        if not num_telephone.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        if len(num_telephone) != 10:
            raise ValidationError('Phone number must be 10 digits long.')
        if Candidat.objects.exclude(pk=self.instance.pk).filter(num_telephone=num_telephone).exists() or Recruteur.objects.filter(num_telephone=num_telephone).exists():
            raise ValidationError('This phone number already exists.')
        return num_telephone
    
    def clean(self):
        cleaned_data = super().clean()
        num_telephone = cleaned_data.get('num_telephone')
        nom = cleaned_data.get('nom')
        prenom = cleaned_data.get('prenom')
        email = cleaned_data.get('email')
        motdepass = cleaned_data.get('motdepass')

        if not nom and not prenom:
            pass    
        elif nom and prenom and Candidat.objects.exclude(pk=self.instance.pk).filter(nom=nom, prenom=prenom).exists():
            self.add_error('nom', 'This first name already exists.')
            self.add_error('prenom', 'This last name already exists.')
        elif nom and prenom and Candidat.objects.exclude(pk=self.instance.pk).filter(nom=prenom, prenom=nom).exists():
            self.add_error('nom', 'This first name already exists.')
            self.add_error('prenom', 'This last name already exists.')
        elif nom == prenom :
            self.add_error('nom', 'You cant put your first name the same as your last name.')
            self.add_error('prenom', 'You cant put your last name the same as your first name.')
            
        
        return cleaned_data
    
    

    
    
    
class RecruteurForm(forms.ModelForm):
    motdepass_confirm = forms.CharField(widget=forms.PasswordInput)
    motdepass = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Recruteur
        fields = ["type_recruteur", "address", "num_telephone", "secteur_activite", "nom_recruteur", "presentation", "email", "motdepass"]
    
    
    def save(self, commit=True):
        email = self.cleaned_data['email']
        base_username = slugify(email.split('@')[0])
        username = base_username
        counter = 1

        # Ensure the username is unique
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}-{counter}"
            counter += 1

        user_data = {
            'username': username,
            'email': email,
            'password': make_password(self.cleaned_data['motdepass'])
        }
        user = CustomUser.objects.create(**user_data)
        
        recruteur = super().save(commit=False)
        recruteur.user = user
        if commit:
            recruteur.save()
        return recruteur
    
    def clean_motdepass(self):
        motdepass = self.cleaned_data.get('motdepass')
        
        if len(motdepass) < 8 or len(motdepass) > 16:
            raise ValidationError('Password must be between 8 and 16 characters.')
        if not re.search(r'[A-Z]', motdepass):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', motdepass):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', motdepass):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[\W_]', motdepass):  
            raise ValidationError('Password must contain at least one special character.')
        return motdepass

    def clean_nom_recruteur(self):
        nom_recruteur = self.cleaned_data.get('nom_recruteur')
        if not re.match(r'^[a-zA-Z\s]+$', nom_recruteur):
            raise ValidationError('Retruter name can only contain letters.')
        return nom_recruteur
    
    def clean_num_telephone(self):
        num_telephone = self.cleaned_data.get('num_telephone')
        if not num_telephone.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        if len(num_telephone) != 10:
            raise ValidationError('Phone number must be 10 digits long.')
        return num_telephone
    
    def clean_secteur_activite(self):
        secteur_activite = self.cleaned_data.get('secteur_activite')
        if not re.match(r'^[a-zA-Z\s]+$', secteur_activite):
            raise ValidationError('Your field can only contain letters.')
        return secteur_activite
    
    def clean(self):
        cleaned_data = super().clean()
        num_telephone = cleaned_data.get('num_telephone')
        nom_recruteur = cleaned_data.get('nom_recruteur')
        email = cleaned_data.get('email')
        motdepass = cleaned_data.get('motdepass')
        motdepass_confirm = cleaned_data.get('motdepass_confirm')

        if email and Recruteur.objects.filter(email=email).exists() or Candidat.objects.filter(email=email).exists():
            self.add_error('email', 'This email already exists.')

        if num_telephone and Recruteur.objects.filter(num_telephone=num_telephone).exists() or  Candidat.objects.filter(num_telephone=num_telephone).exists():
            self.add_error('num_telephone', 'This phone number already exists.')
            
        if nom_recruteur and Recruteur.objects.filter(nom_recruteur=nom_recruteur).exists():
            self.add_error('nom_recruteur', 'This name already exists.')

        if motdepass and motdepass_confirm and motdepass != motdepass_confirm:
            self.add_error('motdepass_confirm', 'Passwords do not match.')
            self.add_error('motdepass', 'Passwords do not match.')
            
        return cleaned_data   
    
    
    
    

    
    
    


class RecruteurUpdateForm(forms.ModelForm):
    motdepass = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Recruteur
        fields = ["type_recruteur", "address", "num_telephone", "secteur_activite", "nom_recruteur", "presentation", "email"]

    def clean_motdepass(self):
        motdepass = self.cleaned_data.get('motdepass')
        if len(motdepass) < 8 or len(motdepass) > 16:
            raise ValidationError('Password must be between 8 and 16 characters.')
        if not re.search(r'[A-Z]', motdepass):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', motdepass):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', motdepass):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[\W_]', motdepass):  
            raise ValidationError('Password must contain at least one special character.')
        if not self.instance.user.check_password(motdepass):
            raise forms.ValidationError('Incorrect password.')
        return motdepass
        

    def clean_nom_recruteur(self):
        nom_recruteur = self.cleaned_data.get('nom_recruteur')
        if not re.match(r'^[a-zA-Z\s]+$', nom_recruteur):
            raise ValidationError('Recruiter name can only contain letters.')
        return nom_recruteur

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Recruteur.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('This email already exists.')
        return email

    def clean_num_telephone(self):
        num_telephone = self.cleaned_data.get('num_telephone')
        if not num_telephone.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        if len(num_telephone) != 10:
            raise ValidationError('Phone number must be 10 digits long.')
        if Recruteur.objects.exclude(pk=self.instance.pk).filter(num_telephone=num_telephone).exists():
            raise ValidationError('This phone number already exists.')
        return num_telephone
    
    def clean(self):
        cleaned_data = super().clean()
        num_telephone = cleaned_data.get('num_telephone')
        nom_recruteur = cleaned_data.get('nom_recruteur')
        email = cleaned_data.get('email')
        motdepass = cleaned_data.get('motdepass')

        if email and Recruteur.objects.exclude(pk=self.instance.pk).filter(email=email).exists() or Candidat.objects.filter(email=email).exists():
            self.add_error('email', 'This email already exists.')

        if num_telephone and Recruteur.objects.exclude(pk=self.instance.pk).filter(num_telephone=num_telephone).exists() or  Candidat.objects.filter(num_telephone=num_telephone).exists():
            self.add_error('num_telephone', 'This phone number already exists.')
            
        if nom_recruteur and Recruteur.objects.exclude(pk=self.instance.pk).filter(nom_recruteur=nom_recruteur).exists():
            self.add_error('nom_recruteur', 'This name already exists.')

            
        return cleaned_data
 