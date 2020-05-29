import pysmt

import hornbeam_pb2

def test_translator():
    # create a policy
    policy = hornbeam_pb2.Policy()

    # create
    statement = hornbeam_pb2.Statment()
    statement.effect = hornbeam_pb2.Statment.Effect.ALLOW
    statement.principal = "test"
    statement.action = "getAction"
    statement.resource = "arn:CABBOOM"

    condition = hornbeam_pb2.Condition()
    condition.op_name = "StringEquals"
    condition.key_name = "aws:sourceVpc"
    condition.value = "vpc-111bbb222"

    statement.conditions.append(condition)
    policy.statements.append(statement)

    trans = AWSTranslator()
    eqs = trans.translate(policy)
    print(eqs)
