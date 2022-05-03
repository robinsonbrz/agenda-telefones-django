from contatos.models import Contato
from django import forms
from django.db import models


class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        exclude = ('data_criacao',)
