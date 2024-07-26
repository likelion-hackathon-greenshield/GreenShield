from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=30, label="이름")
    phone_number = forms.CharField(max_length=11, label="전화번호")
    birth_date = forms.DateField(label="생년월일", widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput,
        min_length=8,
        max_length=20,
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput,
        min_length=8,
        max_length=20,
    )
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'phone_number', 'email', 'birth_date')
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6 or len(username) > 20:
            raise ValidationError("아이디는 6자 이상 20자 이하로 입력해야 합니다.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("이 아이디는 이미 사용 중입니다.")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        if not any(char.isalpha() for char in password1) or not any(char.isdigit() for char in password1):
            raise ValidationError("비밀번호에는 문자와 숫자가 모두 포함되어야 합니다.")
        if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>/?`~' for char in password1):
            raise ValidationError("비밀번호에는 최소 하나의 특수문자가 포함되어야 합니다.")
        if len(password1) > 20:
            raise ValidationError("비밀번호는 20자를 초과할 수 없습니다.")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        return password2