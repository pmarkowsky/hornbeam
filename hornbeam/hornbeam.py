# Hornbeam maps policies to SMT formula using PySMT. It then attempts to solve
# the formula using portfolio solving. 

import pysmt

import hornbeam_pb2
import hornbeam_pb2_grpc
import translator

class HornbeamServicer(hornbeam_pb2_grpc.HornbeamServicer):
    """
    RPC endpoint class.
    """
    def __init__(self):
        self.translator = translator.AWSTranslator()

    def ComparePolicies(self, first, second):
        """
        Compare two AWS policies.
        """
        # TODO add preprocessing steps to the translator
        first_smt = self.translator.translate(first)
        second_smt = self.translator.translate(second)

        result = hornbeam_pb2.ComparePolicyResponse()
        result.result = hornbeam_pb2._COMPAREPOLICYRESPONSE_RESULT.unknown

        # check if A -> B
        if is_sat(Implies(first_smt, second_smt)):
            pass
        # if NOT(A->B) and B->A then A is less permissive than B
        elif is_sat(Implies(second_smt, first_smt)):
            result.result = hornbeam_pb2._COMPAREPOLICYRESPONSE_RESULT.less_permissive
        else:
            # incomparable
            result.result = hornbeam_pb2._COMPAREPOLICYRESPONSE_RESULT.incomparable

        return result
