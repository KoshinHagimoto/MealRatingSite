from django import forms
from .models import Meal, MealRating


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["name", "description", "imageUrl", "countryOfOrigin", "typicalMealTime"]
        widgets = {
            "description": forms.Textarea(attrs={'rows':2, 'col':15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-4'


class MealRatingForm(forms.ModelForm):
    class Meta:
        model = MealRating
        fields = ["rating"]
        widgets = {
            "rating": forms.TextInput(attrs={
                "type": "range",
                "max": 5,
                "min": 0,
                "step": 0.1
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].widget.attrs['class'] = 'p'

