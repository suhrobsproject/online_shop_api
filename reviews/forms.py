from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i} yulduz") for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Bahoingiz"
    )

    class Meta:
        model = Comment
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Mahsulot haqidagi fikringizni yozing...'
            }),
        }
        labels = {
            'comment': 'Sharhingiz'
        }