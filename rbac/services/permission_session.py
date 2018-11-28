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
    permission_queryset = current_user.roles.filter(permission__isnull=False).values('permission__url',
                                                                                     'permission__title',
                                                                                     'permission__nid',
                                                                                     'permission__menu__icon',
                                                                                     'permission__menu__title',
                                                                                     'permission__menu_id').distinct()

    permission_list = []

    menu_dict = {}

    for item in permission_queryset:
        permission_list.append(item['permission__url'])

        menu_id = item['permission__menu_id']
        node = {'title': item['permission__title'], 'url': item['permission__url']}
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

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict
