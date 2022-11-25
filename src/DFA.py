from typing import Callable, Generic, TypeVar

from src.NFA import NFA

S = TypeVar("S")
T = TypeVar("T")


class DFA(Generic[S]):
    dfaMachine = []
    nfaMachine = []
    oldStates = []
    updateStates = {}  # old state : old states with eps
    newState = []
    setOfInput = []

    def getSetOfInput(self):
        temp = set()
        for x in self.nfaMachine:
            if x[1] != "eps":
                temp.add(x[1])
        self.setOfInput = list(temp)

    def groupStates(self):
        for state in self.oldStates:
            tempStack = [state]
            stack = [state]
            while len(stack) > 0:
                currentState = stack.pop(0)
                for trans in self.nfaMachine:
                    if trans[0] == currentState and trans[1] == "eps":
                        tempStack.append(trans[2])
                        stack.append(trans[2])
                if len(stack) == 0:
                    break
            tempStack.sort()
            self.updateStates[state] = tempStack

    def getOldStates(self) -> 'set[S]':
        returnSet = set()
        for x in self.nfaMachine:
            returnSet.add(x[0])
            returnSet.add(x[2])
        return returnSet

    def getNewState(self):
        for trans in self.dfaMachine:
            if self.newState.count(trans[0]) == 0:
                self.newState.append(trans[0])
            if self.newState.count(trans[2]) == 0:
                self.newState.append(trans[2])

    def checkInputValid(self, value):
        for x in self.setOfInput:
            if x == value:
                return True
        return False

    def checkAcceptedState(self, state):
        if state[len(state) - 1] == self.oldStates[len(self.oldStates) - 1]:
            return True
        return False

    def runDFA(self, stackOfInput, currentState) -> bool:
        if len(stackOfInput) == 0 and self.checkAcceptedState(currentState) is False:
            return False
        if len(stackOfInput) == 0 and self.checkAcceptedState(currentState) is True:
            return True
        elif len(stackOfInput) > 0:
            inp = stackOfInput.pop(0)
            for trans in self.dfaMachine:
                if trans[0] == currentState and trans[1] == inp:
                    if self.runDFA(stackOfInput, trans[2]) is True:
                        return True
                    stackOfInput.insert(0, inp)
            return False

    def map(self, f: Callable[[S], T]) -> 'DFA[T]':
        pass

    def next(self, from_state: S, on_chr: str) -> S:
        pass

    def getStates(self) -> 'set[S]':
        pass

    def accepts(self, str: str) -> bool:
        if self.dfaMachine[0][1] == "eps" and len(str) == 0:
            return True
        if self.dfaMachine[0][1] == "void":
            return False
        if self.dfaMachine[0][1] == " " and str == " ":
            print("ngon")
            return True
        if self.dfaMachine[0][1] == " " and str == "":
            print("ngon")
            return False
        else:
            stack = []
            stack[:0] = str
            for x in stack:
                if self.checkInputValid(x) is False:
                    return False
            return self.runDFA(stack, self.updateStates[0])

    def isFinal(self, state: S) -> bool:
        pass

    @staticmethod
    def fromPrenex(str: str) -> 'DFA[int]':
        dfa = DFA()
        dfa.dfaMachine.clear()
        dfa.nfaMachine.clear()
        dfa.oldStates.clear()
        dfa.updateStates.clear()
        dfa.setOfInput.clear()
        dfa.newState.clear()

        if str == "eps":
            dfa.dfaMachine.append([0, str, 1])
        elif str == "void":
            dfa.dfaMachine.append([0, str, 1])
        elif str[0] == "'":
            dfa.dfaMachine.append([0, str[1], 1])
        else:
            nfa = NFA.fromPrenex(str)
            dfa.nfaMachine = nfa.nfaMachine
            dfa.oldStates = list(nfa.getStates())
            dfa.groupStates()
            dfa.getSetOfInput()
            storeState = [dfa.updateStates[0]]
            saveState = [dfa.updateStates[0]]
            while len(storeState) > 0:
                tempState = storeState.pop(0)
                for inp in dfa.setOfInput:
                    for state in tempState:
                        for trans in dfa.nfaMachine:
                            if trans[0] == state and trans[1] == inp:
                                dfa.dfaMachine.append([tempState, inp, dfa.updateStates[trans[2]]])
                                if saveState.count(dfa.updateStates[trans[2]]) == 0:
                                    saveState.append(dfa.updateStates[trans[2]])
                                    storeState.insert(0, dfa.updateStates[trans[2]])
            dfa.getNewState()

        return dfa