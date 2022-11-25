class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data


def containUnion(stack):
    for ele in stack:
        if ele == "|":
            return True
    return False


def parenthesisBehindUnion(stack: list):
    positionUnion = len(stack) - 1
    positionParenthesis = len(stack) - 1
    found = False
    while found is False and positionParenthesis >= 0:
        if stack[positionParenthesis] == ")":
            found = True
        positionParenthesis = positionParenthesis - 1
    found = False
    while found is False and positionUnion >= 0:
        if stack[positionUnion] == "|":
            found = True
        positionUnion = positionUnion - 1
    if positionUnion > positionParenthesis:
        return True
    return False


def parenthesisAfterUnion(stack: list):
    positionUnion = 0
    positionParenthesis = 0
    found = False
    while found is False and positionParenthesis <= len(stack) - 1:
        if stack[positionParenthesis] == "(":
            found = True
        positionParenthesis = positionParenthesis + 1
    found = False
    while found is False and positionUnion <= len(stack) - 1:
        if stack[positionUnion] == "|":
            found = True
        positionUnion = positionUnion + 1
    if positionUnion < positionParenthesis:
        return True
    return False


def findRightOperandOfUnion(stack: list):
    rightOperand = []
    while True:
        temp = stack.pop()
        if temp == "|":
            return rightOperand
        rightOperand.insert(0, temp)


def findLeftOperandOfUnion(stack: list):
    leftOperand = []
    while True:
        temp = stack.pop(0)
        if temp == "|":
            return leftOperand
        leftOperand.insert(0, temp)


def detectParenthesis(stack):
    count = 0
    tempStack = []
    stack.pop()
    while count != -1:
        temp = stack.pop()
        if temp == ')':
            count = count + 1
        elif temp == '(':
            count = count - 1
        tempStack.insert(0, temp)
    return tempStack


def insert(stack: list) -> Node:
    if len(stack) == 1:
        return Node(stack[0])
    else:
        if containUnion(stack) is True:
            if stack[-2] == "|":
                node = Node("UNION")
                node.right = insert(stack.pop())
                stack.pop()
                node.left = insert(stack)
                return node
            elif parenthesisBehindUnion(stack) is True:
                node = Node("UNION")
                node.right = insert(findRightOperandOfUnion(stack))
                node.left = insert(stack)
                return node
            elif parenthesisAfterUnion(stack) is True:
                node = Node("UNION")
                node.left = insert(findLeftOperandOfUnion(stack))
                node.right = insert(stack)
                return node
            elif stack[-1] == ")":
                operandsInsideParenthesis = detectParenthesis(stack)
                if len(stack) != 0:
                    if stack[-1] == "|":
                        node = Node("UNION")
                        operandsInsideParenthesis.pop(0)
                        node.right = insert(operandsInsideParenthesis)
                        stack.pop()
                        node.left = insert(stack)
                        return node
                    else:
                        node = Node("CONCAT")
                        operandsInsideParenthesis.pop(0)
                        node.right = insert(operandsInsideParenthesis)
                        node.left = insert(stack)
                        return node
                else:
                    operandsInsideParenthesis.pop(0)
                    return insert(operandsInsideParenthesis)
            elif stack[-1] == "*":
                if len(stack) == 2:
                    node = Node("STAR")
                    stack.pop()
                    node.left = insert(stack)
                    return node
                elif stack[-2] == ")":
                    # print(stack)
                    star = Node("STAR")
                    stack.pop()
                    operandsInsideParenthesis = detectParenthesis(stack)
                    operandsInsideParenthesis.pop(0)
                    star.left = insert(operandsInsideParenthesis)
                    if len(stack) != 0:
                        if stack[-1] == "|":
                            node = Node("UNION")
                            stack.pop()
                            node.right = star
                            node.left = insert(stack)
                            return node
                        else:
                            node = Node("CONCAT")
                            node.right = star
                            node.left = insert(stack)
                            return node
                    else:
                        return star
            else:
                node = Node("CONCAT")
                node.right = insert(stack.pop())
                node.left = insert(stack)
                return node
        elif containUnion(stack) is False:
            if stack[1] == "*":
                star = Node("STAR")
                star.left = insert(stack[0])
                stack.pop(0)
                stack.pop(0)
                if len(stack) == 0:
                    return star
                else:
                    node = Node("CONCAT")
                    node.left = star
                    node.right = insert(stack)
                    return node
            else:
                node = Node("CONCAT")
                node.left = insert([stack.pop(0)])
                node.right = insert(stack)
                return node
        elif stack[-1] == "*":
            if len(stack) == 2 or stack[-2] == ")":
                node = Node("STAR")
                stack.pop()
                node.left = insert(stack)
                return node
            else:
                if stack[-3] == "|":
                    node = Node("UNION")
                    star = []
                    star.insert(0, stack.pop())
                    star.insert(0, stack.pop())
                    stack.pop()
                    node.right = insert(star)
                    node.left = insert(stack)
                    return node
                else:
                    node = Node("CONCAT")
                    star = []
                    star.insert(0, stack.pop())
                    star.insert(0, stack.pop())
                    node.right = insert(star)
                    node.left = insert(stack)
                    return node
        elif stack[-1] == ")":
            operandsInsideParenthesis = detectParenthesis(stack)
            if len(stack) != 0:
                if stack[-1] == "|":
                    node = Node("UNION")
                    operandsInsideParenthesis.pop(0)
                    node.right = insert(operandsInsideParenthesis)
                    stack.pop()
                    node.left = insert(stack)
                    return node
                else:
                    node = Node("CONCAT")
                    operandsInsideParenthesis.pop(0)
                    node.right = insert(operandsInsideParenthesis)
                    node.left = insert(stack)
                    return node
            else:
                operandsInsideParenthesis.pop(0)
                return insert(operandsInsideParenthesis)
        else:
            node = Node("CONCAT")
            node.right = insert(stack.pop())
            node.left = insert(stack)
            return node


def printInorder(root):
    if root:
        printInorder(root.left)
        print(root.data)
        printInorder(root.right)


def concatAST(tree: Node):
    if tree:
        leftOperand = concatAST(tree.left)
        rightOperand = concatAST(tree.right)
        if len(leftOperand) == 0 and len(rightOperand) == 0:
            return tree.data
        elif len(leftOperand) != 0 and len(rightOperand) == 0:
            return tree.data + " " + leftOperand
        else:
            return tree.data + " " + leftOperand + " " + rightOperand
    else:
        return ""
