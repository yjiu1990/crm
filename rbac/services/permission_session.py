#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.conf import settings

def PermissionSession(current_user, request):
    '''
    :param current_user: 当前用户对象
    :param request: 请求相关的数据
    :return:
    '''
    # 2.权限信息初始化
    # 根据当前用户获取当前用户所对应所有的URL权限，并放入session中
    permission_queryset = current_user.roles.filter(permission__isnull=False).values('permission__url').distinct()

    permission_list = [item['permission__url'] for item in permission_queryset]

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
