from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from ticket.models import TicketPost
from .forms import CommentForm

# Create your views here.
# 文章评论
#@login_required(login_url='/userprofile/login/') #接入用户应用启用
def comment_post(request, ticket_id):
    ticket = get_object_or_404(TicketPost, id=ticket_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.ticket = ticket
            new_comment.user = request.user
            new_comment.save()
            return redirect(ticket)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")