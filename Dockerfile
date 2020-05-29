FROM python:3.8.3-alpine3.11
RUN apk add grpc-dev build-base z3-dev py3-z3 linux-headers
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ADD ./proto ./proto
CMD python -m grpc_tools.protoc -I./proto --python_out=/opt/hornbeam --grpc_python_out=/opt/hornbeam ./proto/hornbeam.proto
