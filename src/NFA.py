from typing import Callable, Generic, TypeVar

S = TypeVar("S")
T = TypeVar("T")


class NFA(Generic[S]):
    nfaMachine = []  # list of list : every list has current state, set of output, set of next states
    state = []  # set of states
    setOfInput = set()

    def makeNFA(self, initialState, stackInput, finalState):
        firstStep = ""
        if len(stackInput) == 1:
            firstStep = stackInput
        else:
            firstStep = stackInput.pop(0)

        if firstStep == "CONCAT":
            finalStateFirst = 0
            finalStateSecond = 0
            theRest = []
            if (stackInput[0] != "UNION" and stackInput[0] != "CONCAT" and stackInput[0] != "STAR") and \
                    (stackInput[1] != "UNION" and stackInput[1] != "CONCAT" and stackInput[1] != "STAR"):
                finalStateFirst, theRest = self.makeNFA(initialState, stackInput.pop(0), finalStateFirst)
                self.nfaMachine.append([finalStateFirst, "eps", finalStateFirst + 1])
                finalStateSecond, theRest = self.makeNFA(finalStateFirst + 1, stackInput.pop(0), finalStateSecond)
                theRest = stackInput
            elif (stackInput[0] != "UNION" and stackInput[0] != "CONCAT" and stackInput[0] != "STAR") and \
                    (stackInput[1] == "UNION" and stackInput[1] == "CONCAT" and stackInput[1] == "STAR"):
                finalStateFirst, theRest = self.makeNFA(initialState, stackInput.pop(0), finalStateFirst)
                self.nfaMachine.append([finalStateFirst, "eps", finalStateFirst + 1])
                finalStateSecond, theRest = self.makeNFA(finalStateFirst + 1, stackInput, finalStateSecond)
            else:
                finalStateFirst, theRest = self.makeNFA(initialState, stackInput, finalStateFirst)
                self.nfaMachine.append([finalStateFirst, "eps", finalStateFirst + 1])
                finalStateSecond, theRest = self.makeNFA(finalStateFirst + 1, theRest, finalStateSecond)
            return finalStateSecond, theRest
        elif firstStep == "UNION":
            finalStateFirst = 0
            finalStateSecond = 0
            theRest = []
            if (stackInput[0] != "UNION" and stackInput[0] != "CONCAT" and stackInput[0] != "STAR") and \
                    (stackInput[1] != "UNION" and stackInput[1] != "CONCAT" and stackInput[1] != "STAR"):
                self.nfaMachine.append([initialState, "eps", initialState + 1])
                finalStateFirst, theRest = self.makeNFA(initialState + 1, stackInput.pop(0), finalStateFirst)
                self.nfaMachine.append([initialState, "eps", finalStateFirst + 1])
                finalStateSecond, theRest = self.makeNFA(finalStateFirst + 1, stackInput.pop(0), finalStateSecond)
                self.nfaMachine.append([finalStateFirst, "eps", finalStateSecond + 1])
                self.nfaMachine.append([finalStateSecond, "eps", finalStateSecond + 1])
                theRest = stackInput
            elif (stackInput[0] != "UNION" and stackInput[0] != "CONCAT" and stackInput[0] != "STAR") and \
                    (stackInput[1] == "UNION" and stackInput[1] == "CONCAT" and stackInput[1] == "STAR"):
                self.nfaMachine.append([initialState, "eps", initialState + 1])
                finalStateFirst, theRest = self.makeNFA(initialState + 1, stackInput.pop(0), finalStateFirst)
                self.nfaMachine.append([initialState, "eps", finalStateFirst + 1])
                finalStateSecond, theRest = self.makeNFA(finalStateFirst + 1, stackInput, finalStateSecond)
                self.nfaMachine.append([finalStateFirst, "eps", finalStateSecond + 1])
                self.nfaMachine.append([finalStateSecond, "eps", finalStateSecond + 1])
            else:
                self.nfaMachine.append([initialState, "eps", initialState + 1])
                finalStateFirst, theRest = self.makeNFA(initialState + 1, stackInput, finalStateFirst)
                self.nfaMachine.append([initialState, "eps", finalStateFirst + 1])
                finalStateSecond, theRest = self.makeNFA(finalStateFirst + 1, theRest, finalStateSecond)
                self.nfaMachine.append([finalStateFirst, "eps", finalStateSecond + 1])
                self.nfaMachine.append([finalStateSecond, "eps", finalStateSecond + 1])
            return finalStateSecond + 1, theRest
        elif firstStep == "STAR":
            finalStateFirst = 0
            theRest = []
            if stackInput[0] != "UNION" and stackInput[0] != "CONCAT":
                self.nfaMachine.append([initialState, "eps", initialState + 1])
                finalStateFirst, theRest = self.makeNFA(initialState + 1, stackInput.pop(0), finalStateFirst)
                self.nfaMachine.append([finalStateFirst, "eps", initialState + 1])
                self.nfaMachine.append([finalStateFirst, "eps", finalStateFirst + 1])
                self.nfaMachine.append([initialState, "eps", finalStateFirst + 1])
                theRest = stackInput
            else:
                self.nfaMachine.append([initialState, "eps", initialState + 1])
                finalStateFirst, theRest = self.makeNFA(initialState + 1, stackInput, finalStateFirst)
                self.nfaMachine.append([finalStateFirst, "eps", initialState + 1])
                self.nfaMachine.append([finalStateFirst, "eps", finalStateFirst + 1])
                self.nfaMachine.append([initialState, "eps", finalStateFirst + 1])
            return finalStateFirst + 1, theRest
        else:
            finalState = initialState + 1
            if type(firstStep) == list:
                self.nfaMachine.append([initialState, firstStep.pop(), finalState])
            else:
                self.nfaMachine.append([initialState, firstStep, finalState])
            return finalState, stackInput

    def runNFA(self, setOfInput, currentState) -> bool:
        if len(setOfInput) == 0:
            if self.isFinal(currentState) is True:
                return True
            else:
                nextStates = self.next(currentState, setOfInput)
                if nextStates.__len__() == 0:
                    return False
                else:
                    for x in nextStates:
                        for state in self.nfaMachine:
                            if state[0] == currentState and state[2] == x:
                                if state[1] == "eps":
                                    if self.isFinal(state[2]) is True:
                                        return True
                                    elif self.runNFA(setOfInput, x) is True:
                                        return True
                                else:
                                    return False
                    return False
        elif len(setOfInput) > 0:
            if self.isFinal(currentState) is True:
                return False
            else:
                nextStates = self.next(currentState, setOfInput[0])
                if nextStates.__len__() == 0:
                    return False
                for x in nextStates:
                    for state in self.nfaMachine:
                        if state[0] == currentState and state[2] == x:
                            if state[1] == setOfInput[0]:
                                tempInput = setOfInput.pop(0)
                                if self.runNFA(setOfInput, x) is True:
                                    return True
                                setOfInput.insert(0, tempInput)
                            elif state[1] == "eps":
                                if self.runNFA(setOfInput, x) is True:
                                    return True
                            else:
                                return False
                return False

    def getSetOfInput(self):
        for x in self.nfaMachine:
            self.setOfInput.add(x[1])

    def checkInputValid(self, value):
        for x in self.setOfInput:
            if x == value:
                return True
        return False

    def map(self, f: Callable[[S], T]) -> 'NFA[T]':
        pass

    def next(self, from_state: S, on_chr: str) -> 'set[S]':
        nextStates = set()
        for x in self.nfaMachine:
            if x[0] == from_state and (x[1] == on_chr or x[1] == "eps"):
                nextStates.add(x[2])
        return nextStates

    def getStates(self) -> 'set[S]':
        returnSet = set()
        for x in self.nfaMachine:
            returnSet.add(x[0])
            returnSet.add(x[2])
        return returnSet

    def accepts(self, str: str) -> bool:
        self.state = list(self.getStates())
        self.getSetOfInput()
        if str == "' '" and len(self.nfaMachine) == 1 and self.nfaMachine[0][1] == " ":
            return True
        elif self.nfaMachine[0][1] == "void":
            return False
        else:
            stack = []
            stack[:0] = str
            for x in stack:
                if self.checkInputValid(x) is False:
                    return False
            return self.runNFA(stack, 0)

    def isFinal(self, state: S) -> bool:
        if state == self.state[len(self.state) - 1]:
            return True
        return False

    @staticmethod
    def fromPrenex(str: str) -> 'NFA[int]':
        nfa = NFA()
        nfa.nfaMachine.clear()
        nfa.setOfInput.clear()
        nfa.state.clear()

        if str == "' '":
            temp = [0, " ", 1]
            nfa.nfaMachine.append(temp)
        elif str == "eps":
            temp = [0, "eps", 0]
            nfa.nfaMachine.append(temp)
        elif str == "void":
            temp = [0, "void", 0]
            nfa.nfaMachine.append(temp)
        else:
            nfa.makeNFA(0, str.split(' '), 1)
        return nfa