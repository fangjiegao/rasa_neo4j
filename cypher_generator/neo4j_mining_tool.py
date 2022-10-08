# coding=utf-8
from py2neo import Graph, RelationshipMatcher, NodeMatcher


BATCH_SIZE = 10000


def get_neo4j_connect(ip, username, password):
    return Graph(ip, username=username, password=password)


def get_relation_matcher(graph):
    relation_matcher = RelationshipMatcher(graph)
    node_selector = NodeMatcher(graph)
    return relation_matcher, node_selector


def run_cql(graph, cql):
    cypher = graph.run
    return cypher(cql)


if __name__ == '__main__':
    ip_ = 'http://192.168.80.108:7474'
    username_ = 'neo4j'
    password_ = 'neo4j1'

    graph_ = get_neo4j_connect(ip_, username_, password_)
    print(graph_)
    cql_ = "match (n:COMPANY) where n.comp_name = '京博石化有限公司' return n.employee_amount,n.comp_industry"
    res = run_cql(graph_, cql_)
    print(res.data())
