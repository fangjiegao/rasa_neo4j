# coding=utf-8
# 查找所有关系
# match (n:CHEMICAL {chmc_name: '甲醇'})-[r:relation_label]->(m:ZONE) return m.zone_address
oneD_relation = "match (n:%s {%s: '%s'})-[r%s]->(m:%s) return m.%s"
# match (n:EQUIPMENT)-[r:relation_label]->(m:SUPPLIER)  where n.eqm_name = '锅炉1' return m.spl_name
# head_label, relation_label, end_label, where_str，end_attr
oneD_relation_hcomplex = "match (n:%s)-[r%s]-(m:%s) %s return m.%s"
sub_where = "n.%s = '%s'"
# match (n:COMPANY) where n.comp_name='京博石化有限公司' and  return n.comp_industry
# MATCH (p:CHEMICAL) WITH max(p.chmc_boiling) as MMcost MATCH (p2:CHEMICAL) where p2.chmc_boiling=MMcost return p2;
# maxormin, label, where_str, return_str
attr_hcomplex = "%s match (n:%s) %s return %s"
# attr, opt, value
sub_where_attr = "n.%s %s '%s'"
sub_where_not_str_attr = "n.%s %s %s"
sub_where_attr_value = "n.%s %s %s"
# attr
return_attr = "n.%s"
# MATCH (p:CHEMICAL) WITH max(p.chmc_boiling) as MMcost
# max or min
max_or_min = "MATCH (p:%s) WITH %s(p.%s) as MMcost"