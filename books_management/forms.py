from django.forms import ModelForm
from .models import Book
 
class createbookform(ModelForm):
    class Meta:
        model=Book
        fields='__all__'