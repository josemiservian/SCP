from django import forms
 
class SelectDateWidget(forms.SelectDateWidget):

    years = range(1900, 2030)