from django.db import models

# Create your models here.

class Menu(models.Model):
    '''
    菜单表
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='一级菜单标题',max_length=64)
    icon = models.CharField(verbose_name='图标',max_length=32,null=True,blank=True)
    def __str__(self):
        return self.title


class Permission(models.Model):
    '''
    权限表
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题',max_length=64)
    url = models.CharField(verbose_name='含正则的URL',max_length=128)

    menu = models.ForeignKey(verbose_name='所属菜单',to='Menu',null=True,blank=True,help_text='null表示不是菜单，非NULL表示菜单',on_delete=models.CASCADE)

    pid = models.ForeignKey(verbose_name='关联的权限',to='Permission',null=True,blank=True,related_name='parents',help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开和选中菜单',on_delete='')
    def __str__(self):
        return self.title

class Role(models.Model):
    '''
    角色表
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='用户角色',max_length=64)
    permission = models.ManyToManyField(verbose_name='所拥有的权限',to='Permission',blank=True)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    '''
    用户表
    '''
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='用户名称',max_length=64)
    password = models.CharField(verbose_name='用户密码',max_length=64)
    email = models.EmailField(verbose_name='用户邮箱')
    roles = models.ManyToManyField(verbose_name='用户对应的角色',to='Role',blank=True)

    def __str__(self):
        return self.name