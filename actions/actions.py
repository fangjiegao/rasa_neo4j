# coding=utf-8
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from actions.WeatherApis import get_weather_by_day
from requests import (
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    Timeout
)
import json
import cypher_generator.neo4j_mining_tool as nt
import cypher_generator.cypher_generator as cg
import re


ip_ = 'http://192.168.80.108:7474'
username_ = 'neo4j'
password_ = 'neo4j1'


class RelationForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "relation_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return []

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(slots)
        spl_name = tracker.get_slot("EQUIPMENT.eqm_name")
        eqm_name = tracker.get_slot("SUPPLIER.spl_name")

        """
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
        json_dic = dict()
        if spl_name != "" and eqm_name != "":
            json_dic["type"] = "relation"
            json_dic["relation"] = ""
            json_dic["head"] = []
            head_dic = dict()
            head_dic["label"] = "EQUIPMENT"
            head_dic["condition"] = {"eqm_name": eqm_name}
            json_dic["head"].append(head_dic)
            json_dic["query"] = []
            query_dic = dict()
            query_dic["label"] = "SUPPLIER"
            query_dic["attr"] = "spl_name"
            query_dic["condition"] = {"opt": ""}
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class SupplierEquipmentRelationForm(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "supplier_equipment_relation_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["EQUIPMENT.eqm_name"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print("slots:", slots)
        eqm_name = tracker.get_slot("EQUIPMENT.eqm_name")

        """
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
        json_dic = dict()
        # if spl_name != "" and eqm_name != "":
        if eqm_name != "" and eqm_name is not None:
            json_dic["type"] = "relation"
            json_dic["relation"] = "SUPPLIER_EQUIPMENT"
            json_dic["head"] = []
            head_dic = dict()
            head_dic["label"] = "EQUIPMENT"
            head_dic["condition"] = {"eqm_name": eqm_name}
            json_dic["head"].append(head_dic)
            json_dic["query"] = []
            query_dic = dict()
            query_dic["label"] = "SUPPLIER"
            query_dic["attr"] = "spl_name"
            query_dic["condition"] = {"opt": ""}
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class CompanyChemicalRelationForm(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "company_chemical_relation_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["CHEMICAL.chmc_name"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(slots)
        chmc_name = tracker.get_slot("CHEMICAL.chmc_name")
        comp_name = tracker.get_slot("COMPANY.comp_name")

        json_dic = dict()
        # if chmc_name != "" and comp_name != "":
        if chmc_name != "" and chmc_name is not None:
            json_dic["type"] = "relation"
            json_dic["relation"] = "COMPANY_CHEMICAL"
            json_dic["head"] = []
            head_dic = dict()
            head_dic["label"] = "CHEMICAL"
            head_dic["condition"] = {"chmc_name": chmc_name}
            json_dic["head"].append(head_dic)
            json_dic["query"] = []
            query_dic = dict()
            query_dic["label"] = "COMPANY"
            query_dic["attr"] = "comp_name"
            query_dic["condition"] = {"opt": ""}
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class CompanySupplierRelationForm(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "company_supplier_relation_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["SUPPLIER.spl_name"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(slots)
        spl_name = tracker.get_slot("SUPPLIER.spl_name")
        comp_name = tracker.get_slot("COMPANY.comp_name")

        json_dic = dict()
        # if spl_name != "" and comp_name != "":
        if spl_name != "" and spl_name is not None:
            json_dic["type"] = "relation"
            json_dic["relation"] = "COMPANY_SUPPLIER"
            json_dic["head"] = []
            head_dic = dict()
            head_dic["label"] = "SUPPLIER"
            head_dic["condition"] = {"spl_name": spl_name}
            json_dic["head"].append(head_dic)
            json_dic["query"] = []
            query_dic = dict()
            query_dic["label"] = "COMPANY"
            query_dic["attr"] = "comp_name"
            query_dic["condition"] = {"opt": ""}
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class CompanyAttrForm(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "company_industry_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["COMPANY.comp_name"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(type(slots), slots)
        # comp_industry = tracker.get_slot("COMPANY.comp_industry")
        comp_name = tracker.get_slot("COMPANY.comp_name")
        """
        {
            "type": "attr",
            "label": "企业实体",
            "query": [{
                "attr": "行业属性",
                "condition": [{
                    "name": "京博石化",
                    "opt": ""
                }]

            },
                {
                    "attr": "员工",
                    "condition": [{
                        "name": "京博石化",
                        "opt": ""
                    }]
                }
            ]
        }
        """
        json_dic = dict()
        # if spl_name != "" and comp_name != "":
        if comp_name != "" and comp_name is not None:
            json_dic["type"] = "attr"
            json_dic["label"] = "COMPANY"
            json_dic["query"] = []
            query_dic = dict()
            query_dic["attr"] = "comp_industry"
            query_dic["condition"] = []
            condition_dic = dict()
            condition_dic["comp_name"] = comp_name
            condition_dic["opt"] = ""
            query_dic["condition"].append(condition_dic)
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class ChemicalEquipmentRelationForm(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "chemical_equipment_relation_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["CHEMICAL.chmc_name"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(slots)
        chmc_name = tracker.get_slot("CHEMICAL.chmc_name")
        comp_name = tracker.get_slot("COMPANY.comp_name")

        json_dic = dict()
        # if spl_name != "" and comp_name != "":
        if chmc_name != "" and chmc_name is not None:
            json_dic["type"] = "relation"
            json_dic["relation"] = "EQUIPMENT_CHEMICAL"
            json_dic["head"] = []
            head_dic = dict()
            head_dic["label"] = "CHEMICAL"
            head_dic["condition"] = {"chmc_name": chmc_name}
            json_dic["head"].append(head_dic)
            json_dic["query"] = []
            query_dic = dict()
            query_dic["label"] = "EQUIPMENT"
            query_dic["attr"] = "eqm_name"
            query_dic["condition"] = {"opt": ""}
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class get_supplier_by_city_and_product_Form(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "get_supplier_by_city_and_product_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["SUPPLIER.spl_city", "SUPPLIER.spl_biz_scope"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(type(slots), slots)
        spl_city = tracker.get_slot("SUPPLIER.spl_city")
        spl_biz_scope = tracker.get_slot("SUPPLIER.spl_biz_scope")

        json_dic = dict()
        # if spl_name != "" and comp_name != "":
        if spl_city != "" and spl_city is not None and spl_biz_scope != "" and spl_biz_scope is not None:
            json_dic["type"] = "attr"
            json_dic["label"] = "SUPPLIER"
            json_dic["query"] = []
            query_dic = dict()
            query_dic["attr"] = "spl_name"
            query_dic["condition"] = []
            condition_dic_city = dict()
            condition_dic_city["spl_city"] = spl_city
            condition_dic_city["opt"] = ""
            query_dic["condition"].append(condition_dic_city)
            condition_dic_biz_scope = dict()
            condition_dic_biz_scope["spl_biz_scope"] = spl_biz_scope
            condition_dic_biz_scope["opt"] = ""
            query_dic["condition"].append(condition_dic_biz_scope)
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class chemical_by_chmc_poison_form(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "chemical_by_chmc_poison_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["CHEMICAL.chmc_poison"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(type(slots), slots)
        chmc_poison = tracker.get_slot("CHEMICAL.chmc_poison")
        if chmc_poison.find("有毒") != -1:
            chmc_poison = "有毒"
        if chmc_poison.find("无毒") != -1:
            chmc_poison = "无毒"

        json_dic = dict()
        # if spl_name != "" and comp_name != "":
        if chmc_poison != "" and chmc_poison is not None:
            json_dic["type"] = "attr"
            json_dic["label"] = "CHEMICAL"
            json_dic["query"] = []
            query_dic = dict()
            query_dic["attr"] = "chmc_name"
            query_dic["condition"] = []
            condition_dic = dict()
            condition_dic["chmc_poison"] = chmc_poison
            condition_dic["opt"] = ""
            query_dic["condition"].append(condition_dic)
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class CompanyZoneRequestRelationForm(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "company_zone_request_relation_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["COMPANY.comp_name"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(slots)
        comp_name = tracker.get_slot("COMPANY.comp_name")
        comp_name = tracker.get_slot("COMPANY.comp_name")

        json_dic = dict()
        # if spl_name != "" and comp_name != "":
        if comp_name != "" and comp_name is not None:
            json_dic["type"] = "relation"
            json_dic["relation"] = "COMPANY_ZONE"
            json_dic["head"] = []
            head_dic = dict()
            head_dic["label"] = "COMPANY"
            head_dic["condition"] = {"comp_name": comp_name}
            json_dic["head"].append(head_dic)
            json_dic["query"] = []
            query_dic = dict()
            query_dic["label"] = "ZONE"
            query_dic["attr"] = "zone_name"
            query_dic["condition"] = {"opt": ""}
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class ChemicalZoneRelationForm(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "chemical_zone_relation_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["CHEMICAL.chmc_name"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(slots)
        chmc_name = tracker.get_slot("CHEMICAL.chmc_name")
        comp_name = tracker.get_slot("COMPANY.comp_name")

        json_dic = dict()
        # if spl_name != "" and comp_name != "":
        if chmc_name != "" and chmc_name is not None:
            json_dic["type"] = "relation"
            json_dic["relation"] = "EQUIPMENT_CHEMICAL"
            json_dic["head"] = []
            head_dic = dict()
            head_dic["label"] = "CHEMICAL"
            head_dic["condition"] = {"chmc_name": chmc_name}
            json_dic["head"].append(head_dic)
            json_dic["query"] = []
            query_dic = dict()
            query_dic["label"] = "EQUIPMENT"
            query_dic["attr"] = "eqm_name"
            query_dic["condition"] = {"opt": ""}
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        s = "MATCH (n:CHEMICAL)-[:COMPANY_CHEMICAL]-(m:COMPANY)-[:COMPANY_ZONE]->(p:ZONE) where n.chmc_name= '%s' RETURN p.zone_address"

        cqls = cg.generator_cypher_by_json(info_json)
        cqls = s % chmc_name
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class get_chemical_chmc_boiling_attr_form(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "chemical_chmc_boiling_attr_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["CHEMICAL.chmc_name"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(slots)
        text = tracker.latest_message["text"]
        print(text)
        chmc_name = tracker.get_slot("CHEMICAL.chmc_name")
        comp_name = tracker.get_slot("COMPANY.comp_name")

        if text.find("CH4") != -1:
            chmc_name = "甲烷"
        elif text.find("NaNO2") != -1:
            chmc_name = "亚硝酸钠"
        elif text.find("羟基甲烷") != -1:
            chmc_name = "甲醇"
        elif text.find("胆矾") != -1:
            chmc_name = "硫酸"
        elif text.find("酒精") != -1:
            chmc_name = "乙醇"
        else:
            pass
        json_dic = dict()
        # if spl_name != "" and comp_name != "":
        if chmc_name != "" and chmc_name is not None:
            json_dic["type"] = "attr"
            json_dic["label"] = "CHEMICAL"
            json_dic["query"] = []
            query_dic = dict()
            query_dic["attr"] = "chmc_boiling"
            query_dic["condition"] = []
            condition_dic = dict()
            condition_dic["chmc_name"] = chmc_name
            condition_dic["opt"] = ""
            query_dic["condition"].append(condition_dic)
            json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))
        return []


class get_max_or_min_chemical_chmc_boiling_attr_form(RelationForm):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "max_or_min_chemical_chmc_boiling_attr_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["compare"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        slots = tracker.current_slot_values()
        print(slots)
        text = tracker.latest_message["text"]
        print(text)
        pat = '\d+'
        rst = re.search(pat, text)
        if rst is not None:
            rst = rst.group(0)
        compare = tracker.get_slot("compare")
        opt = ""
        if compare.find("最高") != -1 or compare.find("最大") != -1:
            opt = "max"
        elif compare.find("最低") != -1 or compare.find("最小") != -1:
            opt = "min"
        elif compare.find("低于") != -1 or compare.find("小于") != -1:
            opt = "<="
        elif compare.find("高于") != -1 or compare.find("大于") != -1:
            opt = ">="
        else:
            opt = ""

        json_dic = dict()
        json_dic["type"] = "attr"
        json_dic["label"] = "CHEMICAL"
        json_dic["query"] = []
        query_dic = dict()
        query_dic["attr"] = "chmc_name"
        query_dic["condition"] = []
        condition_dic = dict()
        if rst is not None:
            condition_dic["chmc_boiling"] = float(rst)
        else:
            condition_dic["chmc_boiling"] = ""
        condition_dic["opt"] = opt
        query_dic["condition"].append(condition_dic)
        json_dic["query"].append(query_dic)

        info_json = json.dumps(json_dic, ensure_ascii=False)

        print(info_json)

        cqls = cg.generator_cypher_by_json(info_json)
        print(cqls)
        neo4j_graph = nt.get_neo4j_connect(ip_, username_, password_)
        print(neo4j_graph)
        if isinstance(cqls, list):
            res = nt.run_cql(neo4j_graph, cqls[0])
            dispatcher.utter_message(str(res.data()))
        else:
            res = nt.run_cql(neo4j_graph, cqls)
            dispatcher.utter_message(str(res.data()))

        s = tracker.slots
        return []


class WeatherForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "weather_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["date_time", "address"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        address = tracker.get_slot('address')
        date_time = tracker.get_slot('date_time')

        date_time_number = text_date_to_number_date(date_time)

        if isinstance(date_time_number, str):  # parse date_time failed
            dispatcher.utter_message("暂不支持查询 {} 的天气".format([address, date_time_number]))
        else:
            weather_data = get_text_weather_date(address, date_time, date_time_number)
            print("action submit:", weather_data)
            dispatcher.utter_message(weather_data)
        return []


def get_text_weather_date(address, date_time, date_time_number):
    try:
        result = get_weather_by_day(address, date_time_number)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = "{} {} ({}) 的天气情况为: 白天 {}, 夜晚 {},气温:{}-{} 度"

        text_message = text_message_tpl.format(
            result['location']['name'],
            date_time,
            result['result']['date'],
            result['result']['text_day'],
            result['result']['text_night'],
            result['result']["high"],
            result['result']["low"],
        )

    return text_message


def text_date_to_number_date(text_date):
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "后天":
        return 2

    # Not supported by weather API provider freely
    if text_date == "大后天":
        # return 3
        return text_date

    if text_date.startswith("星期"):
        return text_date

    if text_date.startswith("下星期"):
        return text_date

    # follow APIs are not supported by weather API provider freely
    if text_date == "昨天":
        return text_date
    if text_date == "前天":
        return text_date
    if text_date == "大前天":
        return text_date
