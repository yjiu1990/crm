#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.conf import settings

def PermissionSession(current_user, request):
    '''
    :param current_user: 当前用户对象
    :param request: 请求相关的数据
    :return:
    '''
    # 2.权限+菜单获取
    # 根据当前用户获取当前用户所对应所有的URL权限，并放入session中
    permission_queryset = current_user.roles.filter(permission__isnull=False).values('permission__url','permission__title','permission__nid','permission__icon','permission__is_menu').distinct()

    permission_list = []
    menu_list = []
    for item in permission_queryset:
        permission_list.append(item['permission__url'])
        if item['permission__is_menu']:
            temps = {
                'url':item['permission__url'],
                'icon':item['permission__icon'],
                'title':item['permission__title']
            }
            menu_list.append(temps)

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_list

