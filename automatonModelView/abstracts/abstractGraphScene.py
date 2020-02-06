from abc import abstractmethod

from PySide2.QtCore import QPointF, Signal, Slot
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsView, QGraphicsSceneMouseEvent

from automatonModelView.abstracts.abstractGeneral import AbstractGeneralGraphScene_Meta, AbstractGeneralGraphSceneClass


class AbstractStateGraphScene(AbstractGeneralGraphSceneClass):
    __metaclass__ = AbstractGeneralGraphScene_Meta

    signalStateEditing = Signal(object)
    signalTransitionEditing = Signal(dict)
    signalTransitionAddition = Signal(dict)
    signalSymbolDataRemoved = Signal()

    def __init__(self, parent):
        super(AbstractStateGraphScene, self).__init__(parent)
        self._stateIdToNodeDict = {}
        self.view = QGraphicsView()
        self.view.setScene(self)
        self.view.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        self.setSceneRect(0, 0, 800, 600)

    @abstractmethod
    @Slot(dict)
    def addNode(self, state):
        pass

    def setupNode(self, node):
        seqNumber = len(self._stateIdToNodeDict)
        node.setPos(QPointF(10 + (40 * (seqNumber % 5)), 45 + (40 * ((seqNumber / 5) % 7))))
        self.addItem(node)
        self.clearSelection()

    def updateNodeLabels(self):
        nodes = list(self._stateIdToNodeDict.values())
        for node in nodes:
            node.setLabel(nodes.index(node))

    def findNodeIndex(self, stateId):
        nodes = list(self._stateIdToNodeDict.values())
        node = self._stateIdToNodeDict[stateId]
        return nodes.index(node)

    @Slot(dict)
    def updateNodeFromInfo(self, info):
        node = self._stateIdToNodeDict[info['stateId']]
        if info['isAcceptable'] != node.isAcceptable:
            node.toggleFinalNodeBorder()
            self.update()

    @Slot(object)
    def updateCurrentState(self, newStateId):
        nodes = list(self._stateIdToNodeDict.values())
        for node in nodes:
            if node.isCurrent:
                node.toggleCurrentState()
        newCurrent = self._stateIdToNodeDict[newStateId]
        newCurrent.toggleCurrentState()

    @abstractmethod
    @Slot(dict)
    def addEdge(self, edgeInfo):
        pass

    def isItemNode(self, graphicsItem):
        return graphicsItem in self._stateIdToNodeDict.values()

    @abstractmethod
    def selectedNode(self):
        pass

    def findStateId(self, targetNode):
        for stateId, node in self._stateIdToNodeDict.items():
            if node is targetNode:
                return stateId

    @abstractmethod
    def selectedEdge(self):
        pass

    @abstractmethod
    def selectedTwoNodes(self):
        pass

    @Slot(str)
    def deleteForStateId(self, stateId):
        node = self._stateIdToNodeDict[stateId]
        edges = node.getEdges()
        if len(edges) > 0:
            for edge in edges:
                self.removeItem(edge)
            del edges[:]

        del self._stateIdToNodeDict[stateId]
        self.removeItem(node)
        self.updateNodeLabels()

    @Slot(object)
    def deleteTransitionsForInput(self, input):
        toDelete = []
        for stateId in self._stateIdToNodeDict:
            node = self._stateIdToNodeDict[stateId]
            edgesForInput = node.getEdgesForInput(input)
            toDelete.extend(edgesForInput)
        if len(toDelete) > 0:
            for edge in toDelete:
                self.removeItem(edge)
            del toDelete[:]
        self.signalSymbolDataRemoved.emit()

    @Slot(dict)
    def deleteStateTransitionForInput(self, transitionInfo):
        node = self._stateIdToNodeDict[transitionInfo.fromStateId]
        edgesForInput = node.getEdgesFromSelf(transitionInfo.onInput)
        for edge in edgesForInput:
            self.removeItem(edge)
        del edgesForInput[:]

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        selectedNodes = self.selectedTwoNodes()

        if selectedNodes is not None:
            self.signalTransitionAddition.emit({'fromState': self.findStateId(selectedNodes['fromNode']),
                                                'toState': self.findStateId(selectedNodes['toNode']), 'input': None})
            self.clearSelection()
        super(AbstractStateGraphScene, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        selectedNode = self.selectedNode()
        selectedEdge = self.selectedEdge()

        if selectedNode is not None:
            stateId = self.findStateId(selectedNode)
            self.signalStateEditing.emit(stateId)
            self.clearSelection()
        elif selectedEdge is not None:
            transitionInfo = {'input': selectedEdge.input()}
            transitionInfo['fromState'] = self.findStateId(selectedEdge.fromNode)
            transitionInfo['toState'] = self.findStateId(selectedEdge.toNode)
            self.signalTransitionEditing.emit(transitionInfo)
            self.clearSelection()
        super(AbstractStateGraphScene, self).mouseDoubleClickEvent(event)
