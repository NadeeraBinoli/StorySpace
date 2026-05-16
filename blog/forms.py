from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select Category"
        self.fields['category'].required = True
        # Set the 'Select Category' option as disabled and hidden in the browser
        self.fields['category'].widget.attrs.update({
            'onfocus': "this.options[0].disabled = true; this.options[0].hidden = true;"
        })

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

class CommentForm(forms.ModelForm):
    author_name = forms.CharField(max_length=100, required=False, label="Name (if anonymous)")
    
    class Meta:
        model = Comment
        fields = ['author_name', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
