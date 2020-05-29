# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import hornbeam_pb2 as hornbeam__pb2


class HornbeamStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ComparePolicies = channel.unary_unary(
                '/Hornbeam/ComparePolicies',
                request_serializer=hornbeam__pb2.ComparePoliciesRequest.SerializeToString,
                response_deserializer=hornbeam__pb2.ComparePolicyResponse.FromString,
                )


class HornbeamServicer(object):
    """Missing associated documentation comment in .proto file"""

    def ComparePolicies(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HornbeamServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ComparePolicies': grpc.unary_unary_rpc_method_handler(
                    servicer.ComparePolicies,
                    request_deserializer=hornbeam__pb2.ComparePoliciesRequest.FromString,
                    response_serializer=hornbeam__pb2.ComparePolicyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Hornbeam', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Hornbeam(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def ComparePolicies(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Hornbeam/ComparePolicies',
            hornbeam__pb2.ComparePoliciesRequest.SerializeToString,
            hornbeam__pb2.ComparePolicyResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
