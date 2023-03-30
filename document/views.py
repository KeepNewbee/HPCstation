from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DocumentPost
from .form import DocumentPostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import markdown
# Create your views here.
def document_list(request):
    document_list = DocumentPost.objects.all()
    # paginator = Paginator(document_list,1)
    # # 获取 url 中的页码
    # page = request.GET.get('page')
    # # 将导航对象相应的页码内容返回给 articles
    # documents = paginator.get_page(page)
    context = {'documents': document_list}
    print(document_list[0].doc_type)
    return render(request, 'document/document_list.html',context)

def document_detail(request, id):
    document = DocumentPost.objects.get(id=id)
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        ]
    )
    document.body = md.convert(document.body)
    print(document.body)
    context = {'document': document, 'toc': md.toc }
    print(document)
    
    return render(request, 'document/document_detail.html',context)
@login_required(login_url='/userprofile/login/')
def document_create(request):
    if request.method == 'POST':
        document_post_form = DocumentPostForm(request.POST)
        if document_post_form.is_valid():
            new_document = document_post_form.save(commit=False)
            new_document.author = User.objects.get(id=request.user.id)
            new_document.save()
            print(document_post_form)
            return redirect("document:document_list")
        else :
            return HttpResponse(document_post_form.errors)
    else:
        document_post_form = DocumentPostForm(request.POST)
        context = {'document_post_form': document_post_form}
        return render(request, 'document/document_create.html',context)

@login_required(login_url='/userprofile/login/')
def document_delete(request, id):
    document = DocumentPost.objects.get(id=id)
    if request.user != document.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    document.delete()
    
    return redirect('document:document_list')

@login_required(login_url='/userprofile/login/')
def document_update(request, id):
    document = DocumentPost.objects.get(id=id)
    if request.user != document.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == 'POST':
        document_post_form = DocumentPostForm(request.POST)
        document_post_form.doc_type = document.doc_type
        if document_post_form.is_valid():
            document.title = request.POST['title']
            document.body = request.POST['body']
            
            document.save()
            print(document_post_form)
            return redirect("document:document_detail", id=id)
        else :
            return HttpResponse("表单信息有误")
    else:
        document_post_form = DocumentPostForm(request.POST)
        context = {'document':document, 'document_post_form': document_post_form}
        return render(request, 'document/document_update.html',context)



@csrf_exempt
def document_search(request):
    query = request.GET.get('q')
    if query:
        documents = DocumentPost.objects.filter(title__icontains=query) | DocumentPost.objects.filter(body__icontains=query)
    else:
        documents = DocumentPost.objects.all()
    return render(request, 'document/document_list.html', {'documents': documents, 'query': query})
    