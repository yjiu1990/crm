#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse,render,redirect
from rbac import models
from django.contrib import auth

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    user = request.POST.get('name')
    pwd = request.POST.get('pwd')

    current_user = models.UserInfo.objects.filter(name=user,password=pwd).first()
    if not current_user:
        return render(request,'login.html',{'msg':'用户名或密码错误'})
    #根据当前用户获取当前用户所对应所有的URL权限，并放入session中
    permission_queryset= current_user.roles.filter(permission__isnull=False).values('permission__url').distinct()

    permission_list = [item['permission__url'] for item in permission_queryset]

    request.session['crm_url_key'] = permission_list
    return redirect('/customer/list/')

def logout(request):
    auth.logout(request)
    return redirect('/login/')