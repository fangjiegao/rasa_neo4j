# coding=utf-8
import json
# import sys
# sys.path.append("..")
import cypher_generator.cql_string as cql_string


def generator_oneD_relation_cypher_by_jsonOb(json_ob):
    end_str = ""
    end_attr = ""
    c_sqls = []
    heads = json_ob["head"]
    relation_str = json_ob["relation"]
    if relation_str != "":
        relation_str = ":" + relation_str
    # print(heads)
    for head in heads:
        head_str = head["label"]
        where_str = ""
        if len(head["condition"].keys()) != 0:
            # print(head["condition"].keys())
            condition_key = list(head["condition"].keys())[0]
            condition_value = head["condition"][condition_key]
            where_str = cql_string.sub_where % (condition_key, condition_value)
            # print(where_str)

        querys = json_ob["query"]
        # print(querys)
        for query in querys:
            end_str = query["label"]
            end_attr = query["attr"]

        if where_str != "":
            where_str = "where " + where_str
        c_sql = cql_string.oneD_relation_hcomplex % (head_str, relation_str, end_str, where_str, end_attr)
        print(c_sql)
        c_sqls.append(c_sql)
    return c_sqls


def generator_attr_cypher_by_jsonOb(json_ob):
    label = json_ob["label"]
    querys = json_ob["query"]
    sub_where_str = set()
    sub_return_str = set()
    max_or_min = ""
    for query in querys:
        attr = query["attr"]
        sub_return = cql_string.return_attr % (attr)
        sub_return_str.add(sub_return)
        conditions = query["condition"]
        for condition in conditions:
            if len(condition.keys()) >= 2:
                for key in condition.keys():
                    op_str = ""
                    condition_attr = ""
                    condition_value = ""
                    if key == "opt":
                        continue
                    else:
                        condition_attr = key
                        condition_value = condition[key]
                    op_str = condition["opt"]
                    if op_str == "":
                        op_str = "="
                    elif op_str == "max":
                        max_or_min = cql_string.max_or_min % (label, op_str, condition_attr)
                        op_str = "="
                        condition_value = "MMcost"
                    elif op_str == "min":
                        max_or_min = cql_string.max_or_min % (label, op_str, condition_attr)
                        op_str = "="
                        condition_value = "MMcost"
                    else:
                        pass
                    if condition_value != "MMcost":
                        if isinstance(condition_value, int) or isinstance(condition_value, float):
                            sub_where = cql_string.sub_where_not_str_attr % (condition_attr, op_str, condition_value)
                            sub_where_str.add(sub_where)
                        else:
                            sub_where = cql_string.sub_where_attr % (condition_attr, op_str, condition_value)
                            sub_where_str.add(sub_where)
                    else:
                        sub_where = cql_string.sub_where_attr_value % (condition_attr, op_str, condition_value)
                        sub_where_str.add(sub_where)

    return_str = ",".join(sub_return_str)
    where_str = "where " + " and ".join(sub_where_str)
    res_cql = cql_string.attr_hcomplex % (max_or_min, label, where_str, return_str)
    return res_cql


def generator_cypher_by_json(json_str):
    json_ob = json.loads(json_str)
    if json_ob["type"] == "relation":
        return generator_oneD_relation_cypher_by_jsonOb(json_ob)
    elif json_ob["type"] == "attr":
        return generator_attr_cypher_by_jsonOb(json_ob)
    else:
        print("type error......")
        return None


if __name__ == '__main__':
    json_data = """
    {
        "type": "relation",
        "head": [{
            "label": "EQUIPMENT",
            "condition": {
                "eqm_name": "锅炉1"
            }
        }],
        "relation": "",
        "query": [{
            "label": "SUPPLIER",
            "attr": "spl_name",
            "condition": {
                "opt": "",
                "": ""
            }
        }]
    }
    """
    res = generator_cypher_by_json(json_data)
    print(res)

    json_data = """
    {
        "type": "relation",
        "head": [{
            "label": "供应商",
            "condition": {
                "供应商名": "富士通"
            }
        }],
             "relation":"relation_label",
        "query": [{     "label": "企业",
                "attr": "企业名",
                "condition": {
                },
                "opt": ""
            }
        ]
    }
    """
    generator_cypher_by_json(json_data)
    json_data = """
    {
        "type": "relation",
        "head": [{
            "label": "化学品",
            "condition": {
                "化学品名 ": "硫酸"
            }
        }],
             "relation":"relation_label",
        "query": [{     "label": "设备",
                "attr": "设备名",
                "condition": {
                },
                "opt": ""
            }
        ]
    }
    """
    generator_cypher_by_json(json_data)
    json_data = """
    {
        "type": "relation",
        "head": [{
            "label": "企业",
            "condition": {
                "企业名": "中国石油公司"
            }
        }],
             "relation":"relation_label",
        "query": [{     "label": "园区",
                "attr": "园区名",
                "condition": {
                },
                "opt": ""
            }
        ]
    }
    """
    res = generator_cypher_by_json(json_data)
    print(res)

    json_data = """
    {
        "type": "attr",
        "label": "COMPANY",
        "query": [{
                "attr": "comp_industry",
                "condition": [{
                    "comp_name": "京博石化有限公司",
                    "opt": ""
                }]

            },
            {
                "attr": "employee_amount",
                "condition": [{
                    "comp_name": "京博石化有限公司",
                    "opt": ""
                }]
            }
        ]
    }
    """
    res = generator_cypher_by_json(json_data)
    print(res)


    json_data = """
    {
        "type": "attr",
        "label": "CHEMICAL",
        "query": [{
            "attr": "chmc_name",
            "condition": [{
                "chmc_boiling": "","opt": "max"
            }]
        }]
    }
    """
    cql = generator_cypher_by_json(json_data)
    print(cql)
