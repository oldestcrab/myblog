#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: forms.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/9/19 10:45
# @description： 账户模块验证的表单

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import widgets
from django.contrib.auth import get_user_model
from django.forms import ValidationError

class RegisterrForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterrForm, self).__init__(*args, **kwargs)

        # Widget负责渲染网页上HTML表单的输入元素和提取提交的原始数据
        self.fields['username'].widget = widgets.TextInput(attrs={'placeholder':'用户名', 'class':'form-control'})
        self.fields['email'].widget = widgets.EmailInput(attrs={'placeholder':'邮箱', 'class':'form-control'})
        self.fields['password1'].widget = widgets.PasswordInput(attrs={'placeholder':'密码', 'class':'form-control'})
        self.fields['password2'].widget = widgets.PasswordInput(attrs={'placeholder':'再次输入密码', 'class':'form-control'})


    def clean_email(self):
        email = self.cleaned_data['email']
        # 在 AUTH_USER_MODEL 设置为自定义用户模型时，如果你直接引用User（例如：通过一个外键引用它），你的代码将不能工作。你应该使用django.contrib.auth.get_user_model()来引用用户模型————指定的自定义用户模型或者User
        if get_user_model().objects.filter(email=email).exists():
            # 如果邮箱已存在，抛出一个自定义的表达错误
            raise ValidationError('该邮箱已存在！')
        return email

    class Meta:
        # 通过get_user_model获取当前模型，表单字段修改为用户名，邮箱，密码与验证密码
        model = get_user_model()
        fields = ('username', 'email')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'placeholder':'用户名', 'class':'form-control'})
        self.fields['password'].widget = widgets.PasswordInput(attrs={'placeholder':'密码', 'class':'form-control'})