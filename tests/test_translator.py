import pysmt

import ..hornbeam as h

def test_translator():
    # create a policy
    policy = h.hornbeam_pb2.Policy()

    # create
    statement = h.hornbeam_pb2.Statment()
    statement.effect = h.hornbeam_pb2.Statment.Effect.ALLOW
    statement.principal = "test"
    statement.action = "getAction"
    statement.resource = "arn:CABBOOM"

    condition = h.hornbeam_pb2.Condition()
    condition.op_name = "StringEquals"
    condition.key_name = "aws:sourceVpc"
    condition.value = "vpc-111bbb222"

    statement.conditions.append(condition)
    policy.statements.append(statement)

    trans = h.AWSTranslator()
    eqs = trans.translate(policy)
    print(eqs)




