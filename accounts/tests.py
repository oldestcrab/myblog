from django.test import TestCase, RequestFactory, Client
from .models import BlogUser
from django.urls import reverse
from my_blog.utils import get_md5
from django.conf import settings
from my_blog.utils import get_current_site
# Create your tests here.
class AccountTest(TestCase):
    def setup(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_validate_register(self):
        # 确定测试数据库中不存在测试用户
        self.assertEqual(0, len(BlogUser.objects.filter(email='user_test@user.com')))
        # 用户注册
        response = self.client.post(reverse('account:register'), {
            'username': 'user_test',
            'email': 'user_test@user.com',
            'password1': 'password123!',
            'password2': 'password123!',
        })
        # 判断是否注册成功
        self.assertEqual(1, len(BlogUser.objects.filter(email='user_test@user.com')))
        user = BlogUser.objects.filter(email='user_test@user.com')[0]
        sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))
        path = reverse('account:result')
        url = f'{path}?type=validation&id={user.id}&sign={sign}'
        response = self.client.get(url)
        # 判断邮箱是否可以验证成功
        self.assertEqual(response.status_code, 200)

    def test_validate_account(self):
        site = get_current_site().domain

        user = BlogUser.objects.create_superuser(username='user_test', password='password123!', email='user_test@user.com')
        login_result = self.client.login(username='user_test', password='password123!')
        # 测试用户登录
        self.assertEqual(login_result, True)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
