from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, RedirectView
from .forms import RegisterrForm, LoginForm
from my_blog.utils import get_current_site, get_md5, send_email
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, logout
from django.utils.http import is_safe_url

logger = logging.Logger(__name__)

class RegisterView(FormView):
    # 表单类，用于 get_form() 方法
    form_class = RegisterrForm
    template_name = 'account/registration_form.html'

    def form_valid(self, form):
        """重写，处理验证过的表单

        :param form: 表单
        :return:return HttpResponseRedirect(self.get_success_url())
        """
        # Return True if the form has no errors, or False otherwise.
        if form.is_valid():
            # save方法有个参数叫commit, 默认是true, 即当使用f.save()的时候，会将数据保存到数据库，但是显示指出commit = false, 则不会保存到数据库
            user = form.save(False)
            # 在is_active 为False 时拒绝用户登录
            user.is_active = False
            user.source = 'Register'
            user.save(True)
            # 获取当前站点
            site = get_current_site().domain
            sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))

            # 非生产环境站点为127.0.0.1:8000
            if settings.DEBUG:
                site = '127.0.0.1:8000'

            path = reverse('account:result')
            url = f'http://{site}{path}?type=validation&id={user.id}&sign={sign}'
            # print(url)
            content = f"""
                            <p>请点击下面链接验证您的邮箱</p>
    
                            <a href="{url}" rel="bookmark">{url}</a>
    
                            再次感谢您！
                            <br />
                            如果上面链接无法打开，请将此链接复制至浏览器。
                            {url}
                            """
            send_email(emailto=[user.email,], title='验证您的电子邮箱', content=content)
            url = reverse('account:result') + '?type=register&id=' + str(user.id)
            return HttpResponseRedirect(url)

        else:
            return self.render_to_response({
                'form':form,
            })

def account_result(request):
    """注册结果视图

    :param request: request
    :return: 注册结果页面或者首页
    """
    type = request.GET.get('type')
    id = request.GET.get('id')

    # get_user_model() 实际获取的是settings.AUTH_USER_MODEL指定的User model
    user = get_object_or_404(get_user_model(), id=id)
    logger.info(type)

    # 账户已激活的话跳转到首页
    if user.is_active:
        return HttpResponseRedirect('/')

    if type and type in ['register', 'validation']:
        if type == 'register':
            content = f'''
    恭喜您注册成功，一封验证邮件已经发送到您 {user.email} 的邮箱，请验证您的邮箱后登录本站。
    '''
            title = '注册成功'
        else:
            c_sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))
            sign = request.GET.get('sign')

            if sign != c_sign:
                return HttpResponseForbidden
            user.is_active = True
            user.save()
            content = '''
            恭喜您已经成功的完成邮箱验证，您现在可以使用您的账号来登录本站。
            '''
            title = '验证成功'

        return render(request, 'account/result.html', {
            'title':title,
            'content':content,
        })
    else:
        return HttpResponseRedirect('/')

# todo:使用环境变量或者python-decouple. 后续会写一篇将配置上下线分离的文章
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = '/'
    # 重定向的name，默认为next，用来定义登陆成功之后的跳回之前访问界面的url，如果不想出现默认值，设置为空值即可。
    redirect_field_name = REDIRECT_FIELD_NAME

    # method_decorator的作用是为函数视图装饰器补充第一个self参数，以适配类视图方法
    # 隐藏敏感信息
    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = '/'
        # 如果获取不到跳转之前的页面，则跳转到首页
        kwargs['redirect_to'] = redirect_to

        return super(LoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():
            logger.info(self.redirect_field_name)

            # 登录
            login(self.request, form.get_user())
            
            return super(LoginView, self).form_valid(form)

        else:
            return self.render_to_response({
                'form':form,
            })

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=[self.request.get_host()]):
            redirect_to = self.success_url
        return redirect_to

class Loginout(RedirectView):
    url = '/login/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(Loginout, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Loginout, self).get(request, *args, **kwargs)