#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
from django.template import Library
from django.conf import settings

from collections import OrderedDict
register = Library()


# @register.inclusion_tag('rbac/static_menu.html')
# def static_menu(request):
#     """
#     创建一级菜单
#     :param request:
#     :return:
#     """
#
#     #获取数据库中is_menu为True的URL
#     menu_list = request.session[settings.MENU_SESSION_KEY]
#     current_url = request.path_info
#     return {'menu_list': menu_list,'current_url':current_url}
@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
    创建二级菜单
    :param request:
    :return:
    """

    #获取数据库中is_menu为True的URL
    menu_dict = request.session[settings.MENU_SESSION_KEY]
    print(request.current_selected_permission)
    #将字典进行排序
    key_list = sorted(menu_dict)

    # 生成空的有序字典
    ordered_dict = OrderedDict()

    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'

        for per in val['children']:
            if per['id'] == request.current_selected_permission:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val

    return {'menu_dict': ordered_dict}

