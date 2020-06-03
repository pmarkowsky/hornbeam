import pysmt

from ..hornbeam_pb2 import Policy, Statement, Condition
from ..translator import AWSTranslator

def test_translator():
    # create a policy
    policy = Policy()

    # create
    statement = Statement()
    statement.effect = Statement.Effect.ALLOW
    statement.principal = "test"
    statement.action = "getAction"
    statement.resource = "arn:CABBOOM"

    condition = Condition()
    condition.op_name = "StringEquals"
    condition.key_name = "aws:sourceVpc"
    condition.value = "vpc-111bbb222"

    statement.conditions.append(condition)
    policy.statements.append(statement)

    trans = AWSTranslator()
    eqs = trans.translate(policy)
    print(eqs)
