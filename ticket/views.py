from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

# 视图函数
from .models import TicketPost
from comment.models import Comment
def ticket_list(request):
    ticket = TicketPost.objects.all()
    # 需要传递给模板（templates）的对象
    context = { 'tickets': ticket }
    # render函数：载入模板，并返回context对象
    return render(request, 'tickets/list.html', context)

# 根据用户id返回该作者的帖子
def ticket_userList(request, id):
    ticket = TicketPost.objects.filter(author_id=id)
    context = {'tickets': ticket}
    return render(request, 'tickets/list.html', context)


import markdown
def ticket_detail(request, id):
    # 取出相应的文章
    tickets = TicketPost.objects.get(id=id)
    comments = Comment.objects.filter(ticket=id)
    # 统计帖子浏览量
    tickets.total_views += 1
    tickets.save(update_fields=['total_views'])
    #Markdown
    tickets.body = markdown.markdown(tickets.body, 
        extensions=[
        #包含 缩写、表格等常用扩展 
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])
    # 需要传递给模板的对象
    context = { 'tickets': tickets, 'comments': comments}
    # 载入模板，并返回context对象
    return render(request, 'tickets/detail.html', context)
  

# 引入redirect用于重定向地址
from django.shortcuts import render, redirect
# 引入刚才定义的TicketPostForm表单类
from .forms import TicketPostForm

# 写文章的视图
def ticket_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        tickets_post_form = TicketPostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if tickets_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_ticket = tickets_post_form.save(commit=False)
            # 作者为当前请求的用户名
            new_ticket.author = request.user
            # 将新文章保存到数据库中
            new_ticket.save()
            # 完成后返回到文章列表
            return redirect("ticket:ticket_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        tickets_post_form = TicketPostForm()
        # 赋值上下文
        context = { 'tickets_post_form': tickets_post_form }
        # 返回模板
        return render(request, 'tickets/create.html', context)
    
# 删文章
def ticket_delete(request, id):
    print(request.method)
    if request.method == 'POST':
        # 根据 id 获取需要删除的文章
        ticket = TicketPost.objects.get(id=id)
        # 调用.delete()方法删除文章
        ticket.delete()
        return redirect("ticket:ticket_list")
    else:
        return HttpResponse("仅允许post请求")
    
# 更新文章
def ticket_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    ticket = TicketPost.objects.get(id=id)
    print(request.method == "POST")
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        ticket_post_form = TicketPostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if ticket_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            ticket.title = request.POST['title']
            ticket.body = request.POST['body']
            ticket.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("ticket:ticket_detail", id=id)
            #return redirect("ticket:ticket_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        ticket_post_form = TicketPostForm()
        # 赋值上下文，将 ticket 帖子对象也传递进去，以便提取旧的内容
        context = { 'ticket': ticket, 'ticket_post_form': ticket_post_form }
        # 将响应返回到模板中
        return render(request, 'tickets/update.html', context)