from django.forms import DecimalField, ModelForm

from .models import Bid, Listing, Comment

class createListingForm(ModelForm):
    price = DecimalField(initial="Your price")

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
    bid = DecimalField(initial="Your bid")

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
