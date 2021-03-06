# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/request.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/request.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13proto/request.proto\"\xc0\x01\n\x0bTaskRequest\x12\x11\n\tcode_path\x18\x01 \x01(\t\x12\x11\n\tdata_path\x18\x02 \x01(\t\x12\x13\n\x0boutput_path\x18\x03 \x01(\t\x12\x13\n\x0btarget_path\x18\x04 \x01(\t\x12\x0f\n\x07timeout\x18\x05 \x01(\x01\x12!\n\x0c\x63onfig_pairs\x18\x06 \x03(\x0b\x32\x0b.ConfigPair\x12\x19\n\x11number_of_retries\x18\x07 \x01(\x05\x12\x12\n\nrequest_id\x18\x08 \x01(\x05\"(\n\nConfigPair\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x94\x01\n\x0cTaskResponse\x12%\n\x06status\x18\x01 \x01(\x0e\x32\x15.TaskResponse.options\x12\x17\n\x0fnumber_of_files\x18\x02 \x01(\x05\x12\x12\n\ntime_taken\x18\x03 \x01(\x01\"0\n\x07options\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x07\x46\x41ILURE\x10\x01\x12\x0b\n\x07SUCCESS\x10\x02\"\'\n\x11TaskStatusRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\x05\"\xd1\x01\n\x12TaskStatusResponse\x12\x17\n\x0f\x63urrent_task_id\x18\x01 \x01(\x05\x12*\n\x06status\x18\x02 \x01(\x0e\x32\x1a.TaskStatusResponse.Status\x12$\n\rtask_response\x18\x03 \x01(\x0b\x32\r.TaskResponse\"P\n\x06Status\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0c\n\x08\x41\x43\x43\x45PTED\x10\x01\x12\x0c\n\x08REJECTED\x10\x02\x12\r\n\tCOMPLETED\x10\x03\x12\x0e\n\nINVALID_ID\x10\x04\x62\x06proto3'
)



_TASKRESPONSE_OPTIONS = _descriptor.EnumDescriptor(
  name='options',
  full_name='TaskResponse.options',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FAILURE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=361,
  serialized_end=409,
)
_sym_db.RegisterEnumDescriptor(_TASKRESPONSE_OPTIONS)

_TASKSTATUSRESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='TaskStatusResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ACCEPTED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REJECTED', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COMPLETED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_ID', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=582,
  serialized_end=662,
)
_sym_db.RegisterEnumDescriptor(_TASKSTATUSRESPONSE_STATUS)


_TASKREQUEST = _descriptor.Descriptor(
  name='TaskRequest',
  full_name='TaskRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code_path', full_name='TaskRequest.code_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data_path', full_name='TaskRequest.data_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='output_path', full_name='TaskRequest.output_path', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='target_path', full_name='TaskRequest.target_path', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeout', full_name='TaskRequest.timeout', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='config_pairs', full_name='TaskRequest.config_pairs', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='number_of_retries', full_name='TaskRequest.number_of_retries', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_id', full_name='TaskRequest.request_id', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=216,
)


_CONFIGPAIR = _descriptor.Descriptor(
  name='ConfigPair',
  full_name='ConfigPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ConfigPair.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='ConfigPair.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=218,
  serialized_end=258,
)


_TASKRESPONSE = _descriptor.Descriptor(
  name='TaskResponse',
  full_name='TaskResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='TaskResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='number_of_files', full_name='TaskResponse.number_of_files', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time_taken', full_name='TaskResponse.time_taken', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TASKRESPONSE_OPTIONS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=261,
  serialized_end=409,
)


_TASKSTATUSREQUEST = _descriptor.Descriptor(
  name='TaskStatusRequest',
  full_name='TaskStatusRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_id', full_name='TaskStatusRequest.request_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=411,
  serialized_end=450,
)


_TASKSTATUSRESPONSE = _descriptor.Descriptor(
  name='TaskStatusResponse',
  full_name='TaskStatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='current_task_id', full_name='TaskStatusResponse.current_task_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='TaskStatusResponse.status', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_response', full_name='TaskStatusResponse.task_response', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TASKSTATUSRESPONSE_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=453,
  serialized_end=662,
)

_TASKREQUEST.fields_by_name['config_pairs'].message_type = _CONFIGPAIR
_TASKRESPONSE.fields_by_name['status'].enum_type = _TASKRESPONSE_OPTIONS
_TASKRESPONSE_OPTIONS.containing_type = _TASKRESPONSE
_TASKSTATUSRESPONSE.fields_by_name['status'].enum_type = _TASKSTATUSRESPONSE_STATUS
_TASKSTATUSRESPONSE.fields_by_name['task_response'].message_type = _TASKRESPONSE
_TASKSTATUSRESPONSE_STATUS.containing_type = _TASKSTATUSRESPONSE
DESCRIPTOR.message_types_by_name['TaskRequest'] = _TASKREQUEST
DESCRIPTOR.message_types_by_name['ConfigPair'] = _CONFIGPAIR
DESCRIPTOR.message_types_by_name['TaskResponse'] = _TASKRESPONSE
DESCRIPTOR.message_types_by_name['TaskStatusRequest'] = _TASKSTATUSREQUEST
DESCRIPTOR.message_types_by_name['TaskStatusResponse'] = _TASKSTATUSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TaskRequest = _reflection.GeneratedProtocolMessageType('TaskRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKREQUEST,
  '__module__' : 'proto.request_pb2'
  # @@protoc_insertion_point(class_scope:TaskRequest)
  })
_sym_db.RegisterMessage(TaskRequest)

ConfigPair = _reflection.GeneratedProtocolMessageType('ConfigPair', (_message.Message,), {
  'DESCRIPTOR' : _CONFIGPAIR,
  '__module__' : 'proto.request_pb2'
  # @@protoc_insertion_point(class_scope:ConfigPair)
  })
_sym_db.RegisterMessage(ConfigPair)

TaskResponse = _reflection.GeneratedProtocolMessageType('TaskResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKRESPONSE,
  '__module__' : 'proto.request_pb2'
  # @@protoc_insertion_point(class_scope:TaskResponse)
  })
_sym_db.RegisterMessage(TaskResponse)

TaskStatusRequest = _reflection.GeneratedProtocolMessageType('TaskStatusRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKSTATUSREQUEST,
  '__module__' : 'proto.request_pb2'
  # @@protoc_insertion_point(class_scope:TaskStatusRequest)
  })
_sym_db.RegisterMessage(TaskStatusRequest)

TaskStatusResponse = _reflection.GeneratedProtocolMessageType('TaskStatusResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKSTATUSRESPONSE,
  '__module__' : 'proto.request_pb2'
  # @@protoc_insertion_point(class_scope:TaskStatusResponse)
  })
_sym_db.RegisterMessage(TaskStatusResponse)


# @@protoc_insertion_point(module_scope)
