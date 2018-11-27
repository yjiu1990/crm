from django.db import models

# Create your models here.

class Permission(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题',max_length=64)
    url = models.CharField(verbose_name='含正则的URL',max_length=128)

    def __str__(self):
        return self.title

class Role(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='用户角色',max_length=64)
    permission = models.ManyToManyField(verbose_name='所拥有的权限',to='Permission',blank=True)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='用户名称',max_length=64)
    password = models.CharField(verbose_name='用户密码',max_length=64)
    email = models.EmailField(verbose_name='用户邮箱')
    roles = models.ManyToManyField(verbose_name='用户对应的角色',to='Role',blank=True)

    def __str__(self):
        return self.name