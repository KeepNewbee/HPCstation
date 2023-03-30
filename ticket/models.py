# Create your models here.
from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
from django.urls import reverse
# timezone 用于处理时间相关事务。
from django.utils import timezone

# 博客帖子数据模型
class TicketPost(models.Model):
    # 帖子id,主键
    id = models.AutoField(primary_key=True)    
    # 帖子作者。参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 帖子标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)
    # 帖子正文。保存大量文本使用 TextField
    body = models.TextField()
    # 帖子创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)
    # 帖子更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
    # 统计帖子浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 帖子分类字段 未启用
    #ticket_type = models.CharField(max_length=50)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将帖子标题返回
        return self.title
    
    # 获取帖子地址
    def get_absolute_url(self):
        return reverse('ticket:ticket_detail', args=[self.id])