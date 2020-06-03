"""
translator.py: translates a hornbeam policies to smt formulae

This file contains all of the classes to translate various policies 
languages to SMT formulae. Each translator provides a translate method.
"""
import hornbeam_pb2

from pysmt.shortcuts import Symbol, LE, GE, Int, String, StrLength, StrContains, StrConcat, StrReplace, And, Equals, Plus, Solver, Not
from pysmt.typing import BOOL, INT, STRING

class AWSTranslator(object):
    def __init__(self):
        self.symbols = {}
        self.condition_operators = {
            "StringEquals": self.strEq,
        }
        self.condition_vars = {}

    def getSymbolByName(self, name):
        return self.symbols.get(name, None)

    def assignSymbol(self, name, sym):
        self.symbols[name] = sym

    def strEq(self, key, value):
        """
        strEq encodes a string equivalency constraint on a key.
        if a symbol for a given key doesn't exists strEq will create the
        variable

        Args:
          key: a string name (e.g. aws:sourceVpc)
          value: a string constant

        Returns:
          a pysmt expression.
        """
        sym = self.getSymbolByName(key)

        if not sym:
            sym = Symbol(key, STRING)
            self.assignSymbol(key, sym)

        return sym.Equals(String(value))

    def encodeStringConstraint(self, var, str_constraint):
        """
        Encode a string constraint against a string variable.

        Args:
          var: a pysmt.Symbol of type string
          str_constraint: a constant string (e.g. foo or arn:*)

        Returns:
          a pysmt Expression 
        """
        # check to see if we have wild cards
        if "*" not in str_constraint and "?" not in str_constraint:
            return var.Equals(String(str_constraint))
        else:
            raise NotImplemented("No support for RegExp and wildcards")

    def encodeCondition(self, cond):
        """
        Encode a Condition into smt formulae
        """
        key_var_name = cond.key_name + "_exists"
        existsVar = self.condition_vars.get(key_var_name, None)

        if not existsVar:
            existsVar = Symbol(key_var_name, BOOL)
            self.condition_vars[key_var_name] = existsVar

        encoder = self.condition_operators.get(cond.op_name, None)
        if not encoder:
            raise NotImplemented("Unsupported condition " + cond.op_name)

        constraints = encoder(cond.key_name, cond.value)

        return And(existsVar, constraints)

    def translate(self, policy):
        """
        args:
          policy: a hornbeam_pb2.Policy object

        returns:
          a pysmt.Expr
        """
        principal = Symbol("principal", STRING)
        action = Symbol("action", STRING)
        resource = Symbol("string", STRING)

        allow_statements = None
        deny_statements = None

        for statement in policy.statements:
            # Create constraints on principal, action, and resource
            stmt_constraints = self.encodeStringConstraint(principal, 
                statement.principal)
            stmt_constraints = And(stmt_constraints, self.encodeStringConstraint(action, 
                statement.action))
            stmt_constraints = And(stmt_constraints, self.encodeStringConstraint(resource, 
                statement.resource))

            # encode the conditions
            for cond in statement.conditions:
                cond_constraints = self.encodeCondition(cond)
                stmt_constraints = And(stmt_constraints, cond_constraints)

            if statement.effect == hornbeam_pb2.Statement.Effect.ALLOW:
                if not allow_statements:
                    allow_statements = stmt_constraints
                else:
                    allow_statements = Or(allow_statements, stmt_contraints)
            else:
                if not deny_statements:
                    deny_statements = stmt_constraints
                else:
                    deny_statements = Or(deny_statements, stmt_contraints)

            # if we don't have any allow statements set them to true
            if allow_statements is None:
                allow_statements = Symbol("allow_all", BOOL)

            # if we don't have any deny statements set them to false
            if deny_statements is None:
                deny_statements = Symbol("deny_all", BOOL)

            return And(allow_statements, Not(deny_statements))
