from __future__ import annotations

from src.AST import insert, concatAST


class Parser:
    # This function should:
    # -> Classify input as either character(or string) or operator
    # -> Convert special inputs like [0-9] to their correct form
    # -> Convert escaped characters
    # You can use Character and Operator defined in Regex.py
    @staticmethod
    def preprocess(regex: str) -> list:
        pass

    # This function should construct a prenex expression out of a normal one.
    @staticmethod
    def toPrenex(s: str) -> str:
        if s == "eps":
            return s
        elif s == "[0-9]":
            return "UNION UNION UNION UNION UNION UNION UNION UNION UNION 0 1 2 3 4 5 6 7 8 9"
        elif s == "[a-z]":
            return "UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION " \
                   "UNION UNION UNION UNION UNION UNION UNION UNION a b c d e f g h i j k l m n o p r s t u v w x y z"
        elif s == "[A-Z]":
            return "UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION " \
                   "UNION UNION UNION UNION UNION UNION UNION UNION A B C D E F G H I J K L M N O P R S T U V W X Y Z"
        else:
            stack = []
            stack[:0] = s
            tree = insert(stack)
            return concatAST(tree)
