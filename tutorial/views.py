from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TutorialPost
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import markdown
# Create your views here.from django.shortcuts import render

# Create your views here.
def tutorial_detail(request, id):
    tutorial = TutorialPost.objects.get(id=id)
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        ]
    )
    tutorial.body = md.convert(tutorial.body)
    tutorial_list = TutorialPost.objects.all().order_by('id')
    print(tutorial.body)
    context = {'tutorial': tutorial, 'tutorial_list':tutorial_list}
    print(tutorial)
    
    return render(request, 'tutorial/tutorial_detail.html',context)



    #可以添加toc
