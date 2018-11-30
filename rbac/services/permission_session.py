#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.conf import settings


def PermissionSession(current_user, request):
    '''
    :param current_user: 当前用户对象
    :param request: 请求相关的数据
    :return:
    '''
    # 2.权限+菜单信息初始化
    # 根据当前用户获取当前用户所对应所有的URL权限，并放入session中
    permission_queryset = current_user.roles.filter(permission__isnull=False).values('permission__url',
'permission__title',
'permission__nid',
'permission__pid',
'permission__url_name',
'permission__pid__url',
'permission__pid__title',
'permission__menu__icon',
'permission__menu__title',
 'permission__menu_id').distinct()

    permission_dict = {}

    menu_dict = {}

    for item in permission_queryset:
        permission_dict[item['permission__url_name']]={
            'id':item['permission__nid'],
            'url':item['permission__url'],
            'pid':item['permission__pid'],
            'title':item['permission__title'],
            'p_title':item['permission__pid__title'],
            'p_url':item['permission__pid__url'],
        }

        menu_id = item['permission__menu_id']
        node = {
            'id':item['permission__nid'],
            'title': item['permission__title'],
            'url': item['permission__url'],
        }

        if not menu_id:
            continue
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permission__menu__title'],
                'icon': item['permission__menu__icon'],
                'children': [node, ]
            }

    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
