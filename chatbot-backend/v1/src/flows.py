from pydantic import BaseModel
from v1.src.handler import TextHandler, ListenHandler, EndHandler
import networkx as nx
from v1.src.node import Node
from core.models.graph_model import Root
from pathlib import Path
import json
from v1.utils.mappings import NODE_MAPPINGS
from typing import List

class Flow(BaseModel):
    file_path: str = "flow_production.json"
    graph: nx.DiGraph 
    class Config:
        arbitrary_types_allowed = True
    @staticmethod
    def get_json(file_path: str = "flow_production.json"):
        json_path = str(Path(__file__).parent / f'flows/{file_path}')
        with open(json_path, 'r') as f:
            data = f.read()
        data = json.loads(data)
        workflow = Root(**data)
        return workflow
    
    @staticmethod
    def get_data_from_json(file_path: str = "flow_production.json"):
        data = Flow.get_json(file_path=file_path)
        node_dict = data.drawflow["Home"].model_dump(by_alias=True)["data"]
        return node_dict

    @staticmethod
    def create_handler_by_type(type, data):
        return NODE_MAPPINGS[type]["handler"](data)

    @staticmethod
    def parse_nodes(node_dict):
        nodes = []
        for id, node in node_dict.items():
            name = node["name"]
            id = str(node["id"])
            type = node["class"]
            if type == "startNode":
                id = "start00000000"
                name = "start00000000"
            data = node["data"]
            inputs = node["inputs"]["input_1"]["connections"]
            outputs = node["outputs"]["output_1"]["connections"]
            pos_x = node["pos_x"]
            pos_y = node["pos_y"]
            handler = Flow.create_handler_by_type(type, data)
            children = []
            parents = []
            for input in inputs:
                parents.append(input["node"])

            for output in outputs:
                children.append(output["node"])
            node_model = Node(
                id=id, 
                name=name, 
                type=type, 
                handler=handler,
                children=children, 
                parents=parents,
                data=data,
                pos_x=pos_x,
                pos_y=pos_y)
            nodes.append(node_model)

        return nodes

    @staticmethod
    def create_graph(nodes: List[Node]):
        g = nx.DiGraph()
        for node in nodes:
            g.add_node(node.id, **node.model_dump())
        for node in nodes:
            for parent in node.parents:
                g.add_edge(parent, node.id)
            for child in node.children:
                g.add_edge(node.id, child)
        return g
    
    @classmethod
    def from_json(cls, file_path: str = "flow_production.json"):
        data = cls.get_data_from_json(file_path)
        nodes = Flow.parse_nodes(data)
        g = Flow.create_graph(nodes)
        return cls(file_path=file_path,graph=g)



