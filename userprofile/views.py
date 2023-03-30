from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile
from document.models import DocumentPost
from ticket.models import TicketPost
from comment.models import Comment
import markdown

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'],password=data['password'])
            if user:
                login(request, user)
                return redirect("mainpage:index")
            else:
                return HttpResponse("账号密码有误")
        else:
            return HttpResponse("账号密码不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form':user_login_form}
        return render(request,'userprofile/login.html',context)
    else:
        return HttpResponse("请求非法")

def user_logout(request):
    logout(request)
    return redirect("mainpage:index")

def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        print(user_register_form.is_valid())
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("mainpage:index")
        else:
            return HttpResponse(user_register_form.errors)
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请求非法")

@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    # user_id 是 OneToOneField 自动生成的字段
    #profile = Profile.objects.get(user_id = id)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("没有权限修改此用户信息")
        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            profile_cleaned_data = profile_form.cleaned_data
            profile.real_name = profile_cleaned_data['real_name']
            profile.department = profile_cleaned_data['department']
            profile.position = profile_cleaned_data['position']
            profile.college = profile_cleaned_data['college']
            #profile.avatar = profile_cleaned_data['avatar']
            profile.bio = profile_cleaned_data['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cleaned_data["avatar"]
                print(profile.avatar)
            profile.save()
            return redirect('mainpage:index')
        else:
            return HttpResponse(profile_form.errors)
    elif request.method == 'GET':
        context = { 'profile': profile, 'user': user }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请求非法")    
    
@login_required(login_url='/userprofile/login/')
def profile_display(request, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        ]
    )
    profile.bio = md.convert(profile.bio)
    context = { 'profile': profile, 'user': user }
    context['num_of_documents'] = DocumentPost.objects.filter(author=user).count()
    context['num_of_tickets'] = TicketPost.objects.filter(author=user).count()
    context['num_of_comments'] = Comment.objects.filter(user=user).count()
    return render(request, 'userprofile/display.html', context)