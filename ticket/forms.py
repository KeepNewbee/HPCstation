from django import forms
from .models import TicketPost

class TicketPostForm(forms.ModelForm):
    class Meta:
        #指明数据模型来源
        model = TicketPost
        # 定义表单包含的字段
        fields = ('title', 'body')