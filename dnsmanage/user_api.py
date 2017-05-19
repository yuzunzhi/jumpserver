from dnsmanage.models import Domain_List, Records
from time import strftime


def db_add_domain(zone=None):
    domain = Domain_List(zone=zone)
    domain.save()


def db_del_domain(domain_list):
    for domain in domain_list:
        Records.objects.filter(zone=domain).delete()
        Domain_List.objects.filter(zone=domain).delete()


def db_add_record(zone, host, data, type, ttl):
    record = Records(zone=zone, host=host, data=data, type=type, ttl=ttl)
    record.save()
    soa_record = Records.objects.get(zone=zone, type="SOA")
    soa_record.serial = soa_record.serial + 1
    soa_record.save()


def db_add_soa_record(zone, host, data, ttl):
    serial = int(strftime("%Y%m%d")) * 100
    soa_record = Records(
        zone=zone, host=host, data=data, type="SOA", ttl=ttl, refresh=600, retry=600, expire=3600, minimum=3600,
        serial=serial, resp_person="zunzhiyu", primary_ns=data)
    soa_record.save()



def db_edit_record(id, host, data, type, ttl):
    record = Records.objects.get(id=id)
    record.host, record.data, record.type, record.ttl = (host, data, type, ttl)
    record.save()
    soa_record = Records.objects.get(zone=record.zone, type="SOA")
    soa_record.serial = soa_record.serial + 1
    soa_record.save()


def db_del_record(record_id, zone):
    Records.objects.filter(id=record_id).delete()

    soa_record = Records.objects.get(zone=zone, type="SOA")
    soa_record.serial = soa_record.serial + 1
    soa_record.save()
