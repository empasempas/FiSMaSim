from PySide2.QtCore import Slot

from automatonModelView.abstracts.abstractGraphScene import AbstractStateGraphScene
from automatonModelView.deterministicFiniteAutomaton.shapes.dfaEdge import DFAEdge
from automatonModelView.deterministicFiniteAutomaton.shapes.dfaNode import DFANode


class DFAGraphScene(AbstractStateGraphScene):
    def __init__(self, parent):
        super(DFAGraphScene, self).__init__(parent)

    def selectedNode(self):
        items = self.selectedItems()
        if len(items) == 1 and isinstance(items[0], DFANode):
            return items[0]

    def selectedEdge(self):
        items = self.selectedItems()
        if len(items) == 1 and isinstance(items[0], DFAEdge):
            return items[0]

    def addNode(self, state):
        node = DFANode(self, state)
        self._stateIdToNodeDict[state.id] = node
        self.setupNode(node)
        self.updateNodeLabels()

    @Slot(dict)
    def addEdge(self, edgeInfo):
        fromNode = self._stateIdToNodeDict[edgeInfo['fromStateId']]
        toNode = self._stateIdToNodeDict[edgeInfo['toStateId']]
        newEdge = DFAEdge(fromNode, toNode, edgeInfo['input'])

        fromNode.addEdge(newEdge)
        toNode.addEdge(newEdge)
        self.addItem(newEdge)
        self.clearSelection()

        fromIndex = self.findNodeIndex(edgeInfo['fromStateId'])
        toIndex = self.findNodeIndex(edgeInfo['toStateId'])
        newEdge.setLabel(fromIndex, toIndex)

    def selectedTwoNodes(self):
        items = self.selectedItems()
        if len(items) == 2 and isinstance(items[0], DFANode) and isinstance(items[1], DFANode):
            return {'fromNode': items[0], 'toNode': items[1]}
