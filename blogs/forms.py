from tkinter.ttk import Button
from django import forms 
from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, Button           
INPUT_CLASSES = (
    'mt-2 block w-full rounded-xl border border-slate-300 bg-white px-4 py-3 '
    'text-slate-900 shadow-sm outline-none transition focus:border-indigo-500 '
    'focus:ring-4 focus:ring-indigo-100'
)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "excerpt",
            "content",
            "image",
            "category",
            "status",
            "published_at",
            "featured"
        ]

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Blog Information',
                Row(
                    Column('author', css_class='form-group col-md-6'),
                    Column('title', css_class='form-group col-md-6'),
                ),
                'content',
                'published_at',
                "excerpt",
                "image",
                "category",
                "status",
                "published_at",
                "featured"
            ),
            Submit('submit', 'Save Blog', css_class='btn btn-primary'),
            Button('cancel', 'Cancel', css_class='btn btn-secondary',
                   onclick="window.history.back();")
        )
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post

                     
#         widgets = {
#             "title": forms.TextInput(
#                   attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                     "placeholder": "Enter post title",
#                 }
#             ),

#             "excerpt": forms.Textarea(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                     "rows": 3,
#                     "placeholder": "Write a short summary of your post...",
#                 }
#             ),

#             "content": forms.Textarea(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                     "rows": 15,
#                     "placeholder": "Write your article here...",
#                 }
#             ),

#             "category": forms.Select(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                 }
#             ),

#             "status": forms.Select(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                 }
#             ),

#             "published_at": forms.DateTimeInput(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                     "type": "datetime-local",
#                 }
#             ),

#             "featured": forms.CheckboxInput(
#                 attrs={
#                     "class": "h-4 w-4 rounded border-gray-300 text-gold-600 focus:ring-gold-500",
#                 }
#             ),
            
#         }
class SubscribeForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "email@example.com",
                "class": INPUT_CLASSES,
            }
        ),
    )

    
