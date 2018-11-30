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
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        # print('permission', permission_list)
        # 如果没有session中不存在当前用户的信息则返回错误
        if not permission_dict:
            return HttpResponse('未获取到用户信息，请登陆')

        flag = False

        url_record = [
            {'title': '首页', 'url': '#'}
        ]
        # 循环session中的url,判断url是否与当前用户访问的url匹配，如果匹配则可以访问，匹配不成功则返回错误信息
        for item in permission_dict.values():
            reg = '^%s$' % item['url']
            if re.match(reg, current_url):
                flag = True
                # 获取pid或id,如果pid为True传给current_selected_permission，为False则把ID传给current_selected_permission
                request.current_selected_permission = item['pid'] or item['id']
                if not item['pid']:
                    url_record.extend([{'title': item['title'], 'url': item['url'],'class':'active'}])
                else:
                    url_record.extend(
                        [{'title': item['p_title'], 'url': item['p_url']},
                         {'title': item['title'], 'url': item['url'],'class':'active'},
                         ]
                    )
                request.url_record = url_record
                break

        if not flag:
            return HttpResponse('无权访问')
