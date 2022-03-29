from django.forms import DecimalField, TextInput, ModelForm

from .models import Bid, Listing, Comment

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
    
class addBidForm(ModelForm):
    bid = DecimalField(initial=199.99, label='bid', widget=TextInput(attrs={"placeholder": "Your bid"}))

    class Meta:
        model = Bid
        fields = [
            'bid'
        ]

class addCommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = [
            'content'
        ]
