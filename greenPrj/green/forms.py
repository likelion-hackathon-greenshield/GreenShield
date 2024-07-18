from django import forms
from .models import Question, Answer

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