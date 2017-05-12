from django.conf.urls import url, patterns

urlpatterns = patterns('dnsmanage.views',
                       url(r'^$', 'dns_index', name='dns_index'),
                       url(r'^domain/add/$', 'domain_add', name='domain_add'),
                       url(r'^domain/del/$', 'domain_del', name='domain_del'),
                       url(r'^record/list/$', 'records_list', name='records_list'),
                       url(r'^record/add/$', 'record_add', name='record_add'),
                       url(r'^record/edit/$', 'record_edit', name='record_edit'),
                       url(r'^record/del/$', 'record_del', name='record_del'),
                       )
