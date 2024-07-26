from django import forms
from .models import Post, Comment, Question, Answer

class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 10}))
    class Meta:
        model = Post
        fields = ['category', 'content', 'image', 'video']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'video': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 3}))
    class Meta:
        model = Comment
        fields = ['content']

class TestForm(forms.Form):
    class Meta:
        model = Answer
        fields = ['question', 'answer']

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        questions = Question.objects.all().order_by('order')
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=[
                    ('1', '매우 아니다'),
                    ('2', '아니다'),
                    ('3', '보통이다'),
                    ('4', '그렇다'),
                    ('5', '매우 그렇다')
                ],
                widget = forms.RadioSelect,
                label = question.question
            )