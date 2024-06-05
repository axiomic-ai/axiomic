
import grpc
import os

from google.protobuf import text_format as text_format_
from google.protobuf.json_format import MessageToJson



def text_parse(proto, text):
    text_format_.Parse(text, proto)
    return proto

def text_dump(proto):
    return text_format_.MessageToString(proto)

text_format = text_dump

def _load_protos(file_path):
    protos, service = grpc.protos_and_services(os.path.join('axiomic/protos', file_path))
    return protos, service

def json_dump(proto):
    return MessageToJson(proto)

axiomic, axiomic_service = _load_protos('axiomic.proto')