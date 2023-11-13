#!/usr/bin/env python3.11
from dataclasses import dataclass
import random
import numpy as np
from scipy import linalg as la

@dataclass
class ChainNode:
    name: str

    def __repr__(self) -> str:
        return self.name

@dataclass
class ObservationState:
    name: str

    def __repr__(self) -> str:
        return self.name

@dataclass
class Edge:
    src: ChainNode
    dst: ChainNode
    weight: float

@dataclass
class ObservationEdge:
    observed: ChainNode
    state: ObservationState
    weight: float

@dataclass
class ObservedNode:
    node: ChainNode
    observation: ObservationState

    def __repr__(self) -> str:
        return f"{self.node}->{self.observation}"


class MarkovChain:
    def __init__(self, edges: list[Edge]):
        self.nodes: list[ChainNode] = []
        for edge in edges:
            for node in (edge.src, edge.dst):
                if node not in self.nodes:
                    self.nodes.append(node)
        self.edges = np.zeros(shape=(len(self.nodes), len(self.nodes)))
        for edge in edges:
            self.edges[self.node_index(edge.src), self.node_index(edge.dst)] = edge.weight
        print(la.eig(self.edges, left=True, right=False))
        assert self.is_normalised()

    def is_normalised(self) -> bool:
        return all(sum(row) == 1 for row in self.edges)

    def node_index(self, node: ChainNode) -> int:
        return self.nodes.index(node)

    def get_next_state(self, node: ChainNode) -> ChainNode:
        index = self.node_index(node)
        row = self.edges[index]
        return random.choices(self.nodes, row)[0]

    def random_walk(self, start_node: ChainNode | None = None, length: int = 3) -> list[ChainNode]:
        if start_node:
            node = start_node
        else:
            node = random.choice(self.nodes)
        walk = []
        for _ in range(length):
            walk.append(node)
            node = self.get_next_state(node)
        return walk


class HMM:
    def __init__(self, chain: MarkovChain, edges: list[ObservationEdge]):
        self.chain = chain
        self.states: list[ObservationState] = []
        for edge in edges:
            if edge.state not in self.states:
                self.states.append(edge.state)
        self.edges = np.zeros(shape=(len(self.chain.nodes), len(self.states)))
        for edge in edges:
            self.edges[self.chain.node_index(edge.observed)
                       ][self.state_index(edge.state)] = edge.weight
        assert self.is_normalised()

    def is_normalised(self) -> bool:
        return all(sum(row) == 1 for row in self.edges)

    def state_index(self, state: ObservationState) -> int:
        return self.states.index(state)

    def get_observation(self, node: ChainNode) -> ObservationState:
        index = self.chain.node_index(node)
        row = self.edges[index]
        return random.choices(self.states, row)[0]

    def get_observations(self, walk: list[ChainNode]) -> list[ObservationState]:
        observations = []
        for node in walk:
            observations.append(self.get_observation(node))
        return observations

    def observed_walk(self, length: int = 3) -> list[ObservedNode]:
        walk = self.chain.random_walk(length=length)
        observations = self.get_observations(walk)
        out = []
        for i in range(length):
            out.append(ObservedNode(walk[i], observations[i]))
        return out


cold = ChainNode("cold")
hot = ChainNode("hot")
chain = MarkovChain([
    Edge(cold, cold, 0.5),
    Edge(cold, hot, 0.5),
    Edge(hot, cold, 0.4),
    Edge(hot, hot, 0.6),
 ])
one = ObservationState("one")
two = ObservationState("two")
three = ObservationState("three")
hmm = HMM(chain, [
             ObservationEdge(cold, one, 0.5),
             ObservationEdge(cold, two, 0.4),
             ObservationEdge(cold, three, 0.1),
             ObservationEdge(hot, one, 0.2),
             ObservationEdge(hot, two, 0.4),
             ObservationEdge(hot, three, 0.4),
          ])
