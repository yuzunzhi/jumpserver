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


def db_edit_record(id, host, data, type, ttl):
    record = Records.objects.get(id=id)
    record.host, record.data, record.type, record.ttl = (host, data, type, ttl)
    record.save()
    soa_record = Records.objects.get(zone=record.zone, type="SOA")
    soa_record.serial = soa_record.serial + 1
    soa_record.save()


def db_del_record(record_id_list):
    zone = Records.objects.get(id=record_id_list[0]).zone

    for record_id in record_id_list:
        Records.objects.filter(id=record_id).delete()

    soa_record = Records.objects.get(zone=zone, type="SOA")
    soa_record.serial = soa_record.serial + 1
    soa_record.save()
