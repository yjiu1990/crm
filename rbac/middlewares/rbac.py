#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import re
from django.conf import settings

class RbacMiddleware(MiddlewareMixin):
    '''
    1.获取当前用户的url
    2.获取当前用户在session中的url权限列表
    3.权限信息进行匹配
    '''

    def process_request(self, request):
        '''
        当用户请求刚进入时执行
        :param request:
        :return:
        '''

        # 获取当前用户的url
        current_url = request.path_info
        # 如果当前用户访问的url在白名单内则可以访问
        for valid in settings.VALID_URL_LIST:
            if re.match(valid, current_url):
                return None

        # print(current_url)
        # 获取当前用户session中的存放的url
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        # print('permission', permission_list)
        # 如果没有session中不存在当前用户的信息则返回错误
        if not permission_list:
            return HttpResponse('未获取到用户信息，请登陆')

        flag = False
        # 循环session中的url,判断url是否与当前用户访问的url匹配，如果匹配则可以访问，匹配不成功则返回错误信息
        for item in permission_list:
            reg = '^%s$' % item['url']
            if re.match(reg, current_url):
                flag = True
                request.current_selected_permission = item['pid'] or item['id']
                break
        if not flag:
            return HttpResponse('无权访问')
