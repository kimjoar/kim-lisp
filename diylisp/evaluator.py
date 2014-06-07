# -*- coding: utf-8 -*-

from .types import Environment, LispError, Closure
from .ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from .asserts import assert_exp_length, assert_valid_definition, assert_boolean
from .parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""


def evaluate(ast, env):
    if is_boolean(ast):
        return ast
    if is_symbol(ast):
        return env.lookup(ast)
    if is_integer(ast):
        return ast
    if is_list(ast):
        if is_boolean(ast[0]):
            raise LispError("not a function")
        if is_integer(ast[0]):
            raise LispError("not a function")

        if is_closure(ast[0]):
            return evaluate_closure(ast[0], ast[1:], env)
        if ast[0] == "define":
            if len(ast) != 3:
                raise LispError("Wrong number of arguments")
            if not is_symbol(ast[1]):
                raise LispError("non-symbol")
            env.set(ast[1], evaluate(ast[2], env))
            return
        if ast[0] == "lambda":
            if not is_list(ast[1]):
                raise LispError("arguments is not a list")
            if len(ast) != 3:
                raise LispError("number of arguments")
            return Closure(env, ast[1], ast[2])
        if ast[0] == "quote":
            return ast[1]
        if ast[0] == "atom":
            return is_atom(evaluate(ast[1], env))
        if ast[0] == "if":
            res = evaluate(ast[1], env)
            if res:
                return evaluate(ast[2], env)
            else:
                return evaluate(ast[3], env)

        arg1 = evaluate(ast[1], env)
        if len(ast) > 2:
            arg2 = evaluate(ast[2], env)

        if ast[0] == "eq":
            if is_atom(arg1) or is_atom(arg2):
                return arg1 == arg2
            return False
        if ast[0] == "+":
            check_math_args(arg1, arg2)
            return arg1 + arg2
        if ast[0] == "-":
            check_math_args(arg1, arg2)
            return arg1 - arg2
        if ast[0] == "/":
            check_math_args(arg1, arg2)
            return arg1 / arg2
        if ast[0] == "*":
            check_math_args(arg1, arg2)
            return arg1 * arg2
        if ast[0] == "mod":
            check_math_args(arg1, arg2)
            return arg1 % arg2
        if ast[0] == ">":
            check_math_args(arg1, arg2)
            return arg1 > arg2
        if ast[0] == "<":
            check_math_args(arg1, arg2)
            return arg1 < arg2
        if ast[0] == "=":
            check_math_args(arg1, arg2)
            return arg1 == arg2

        if ast[0] == "cons":
            a = [evaluate(ast[1], env)]
            l = evaluate(ast[2], env)
            return a + l

        if ast[0] == "head":
            res = evaluate(ast[1], env);
            if len(res) == 0:
                raise LispError("too few args")
            return res[0]

        if ast[0] == "tail":
            res = evaluate(ast[1], env);
            return res[1:]

        if ast[0] == "empty":
            res = evaluate(ast[1], env);
            return len(res) == 0

        if is_symbol(ast[0]):
            closure = env.lookup(ast[0])
            params = ast[1:];
            if len(closure.params) != len(params):
                raise LispError("wrong number of arguments, expected %s got %s" % (len(closure.params), len(params)))
            return evaluate_closure(closure, params, env)

        if is_list(ast[0]):
            res = evaluate(ast[0], env)
            ast[0] = res
            return evaluate(ast, env)

def check_math_args(arg1, arg2):
    if not is_integer(arg1) or not is_integer(arg2):
        raise LispError("MATH, yo")

def evaluate_closure(closure, params, env):
    evaluated = [evaluate(a, env) for a in params]
    e = Environment(dict(zip(closure.params, evaluated)))
    return evaluate(closure.body, e.extend(closure.env.variables))
