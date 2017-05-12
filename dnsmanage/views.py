# coding: utf-8
from django.shortcuts import render
from jumpserver.api import *
from dnsmanage.user_api import *
from django.db.models import Q
from .models import Domain_List, Records
# Create your views here.

@require_role(role='super')
def dns_index(request):
    """
    域名列表
    """
    header_title, path1, path2 = '域名列表', 'DNS管理', '域名列表'
    keyword = request.GET.get('search', '')
    domain_list = Domain_List.objects.all().order_by('zone')
    group_id = request.GET.get('id', '')

    # 搜索时过滤主机名或地址
    if keyword:
        domain_list = domain_list.filter(Q(host__icontains=keyword) | Q(data__icontains=keyword))

    # 暂时没用
    if group_id:
        domain_list = domain_list.filter(id=int(group_id))

    domain_list, p, domain, page_range, current_page, show_first, show_end = pages(domain_list, request)
    return my_render('dnsmanage/domain_list.html', locals(), request)

@require_role(role='super')
def domain_add(request):
    """
    domain add view for route
    添加域名的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加域名', 'DNS管理', '添加域名'
    domain_all = Domain_List.objects.all()

    if request.method == 'POST':
        domain_name = request.POST.get('domain_name', '')

        try:
            if not domain_name:
                error = u'域名 不能为空'
                raise ServerError(error)

            if Domain_List.objects.filter(zone=domain_name):
                error = u'域名已存在'
                raise ServerError(error)
            db_add_domain(zone=domain_name)
        except ServerError:
            pass
        except TypeError:
            error = u'添加域名失败'
        else:
            msg = u'添加域名 %s 成功' % domain_name

    return my_render('dnsmanage/domain_add.html', locals(), request)

@require_role(role='super')
def domain_del(request):
    """
    del a domain
    删除用户组
    """
    domains = request.GET.get('zone', '')
    domain_list = domains.split(',')
    db_del_domain(domain_list)
    return HttpResponse('删除成功')

@require_role(role='super')
def records_list(request):
    """
    域名解析记录列表
    """
    domain = request.GET.get('zone')
    header_title, path1, path2 = '%s记录列表' % domain, 'DNS管理', domain
    keyword = request.GET.get('search', '')
    records_list = Records.objects.filter(zone=domain)
    group_id = request.GET.get('id', '')

    # 搜索时过滤主机名或地址
    if keyword:
        records_list = records_list.filter(Q(host__icontains=keyword) | Q(data__icontains=keyword))

    # 暂时没用
    if group_id:
        records_list = records_list.filter(id=int(group_id))

    ecords_list, p, records, page_range, current_page, show_first, show_end = pages(records_list, request)
    return my_render('dnsmanage/record_list.html', locals(), request)

@require_role(role='super')
def record_add(request):
    """
    record add view for route
    添加解析记录的视图
    """
    error = ''
    msg = ''
    domain = request.GET.get('zone')
    header_title, path1, path2 = '添加解析记录', 'DNS管理', domain
    record_all = Records.objects.all()

    if request.method == 'POST':
        host = request.POST.get('host')
        data = request.POST.get('data')
        type = request.POST.get('type')
        ttl = request.POST.get('ttl')


        try:
            if not host or not data or not type or not ttl:
                error = u'主机记录或记录值或记录类型或TTL 不能为空'
                raise ServerError(error)

            if Records.objects.filter(zone=domain, host=host, data=data, type=type):
                error = u'主机记录已存在'
                raise ServerError(error)

            if type == "SOA" and Records.objects.filter(zone=domain, type="SOA"):
                error = u'SOA记录已存在'
                raise ServerError(error)

            db_add_record(domain, host, data, type, ttl)

        except ServerError:
            pass
        except TypeError:
            error = u'添加主机记录失败'
        else:
            msg = u'添加主机记录成功'

    return my_render('dnsmanage/record_add.html', locals(), request)

@require_role(role='super')
def record_del(request):
    """
    del a record
    删除主机记录
    """
    record_id = request.GET.get('id', '')
    record_id_list = record_id.split(',')
    db_del_record(record_id_list)

    return HttpResponse('删除成功')

@require_role(role='super')
def record_edit(request):
    """
    record edit view for route
    编辑解析记录的视图
    """
    error = ''
    msg = ''
    domain = request.GET.get('zone')
    record_id = request.GET.get('record_id')
    header_title, path1, path2 = '解析记录变更', 'DNS管理', domain
    record = Records.objects.get(id=record_id)

    if request.method == 'POST':
        id = record_id
        host = request.POST.get('host')
        data = request.POST.get('data')
        ttl = request.POST.get('ttl')
        type = request.POST.get('type')

        try:
            if not data or not type or not ttl:
                error = u'主机记录或记录值或记录类型或TTL 不能为空'
                raise ServerError(error)

            db_edit_record(id, host, data, type, ttl)
        except ServerError:
            pass
        except TypeError:
            error = u'编辑主机记录失败'
        else:
            msg = u'编辑主机记录成功'

    return my_render('dnsmanage/record_edit.html', locals(), request)