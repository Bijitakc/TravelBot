from django import forms
from .models import BookHotel

class BookingForm(forms.ModelForm):
    class Meta:
        model = BookHotel
        checkin_date = forms.DateField(
            widget=forms.TextInput(     
                attrs={'type': 'date'} 
            )
        )  
        checkout_date = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
        )    
        fields = ['no_of_rooms', 'checkin_date', 'checkout_date']
    #added for placeholders
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        
        self.fields['checkin_date'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
        self.fields['checkout_date'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
