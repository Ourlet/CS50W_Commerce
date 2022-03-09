from django.forms import CharField, DecimalField, HiddenInput, TextInput, ValidationError, ModelForm

from .models import Listing

class createListingForm(ModelForm):
    price = DecimalField(initial=199.99, label='bid', widget=TextInput(attrs={"placeholder": "Your bid"}))

    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'price',
            'category',
            'image'
        ]
    