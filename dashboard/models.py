from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from AUTH_APP.models import *
from offre_demande.models import *
# Create your models here.
