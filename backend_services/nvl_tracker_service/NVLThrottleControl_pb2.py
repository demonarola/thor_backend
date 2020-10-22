# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: NVLThrottleControl.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='NVLThrottleControl.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x18NVLThrottleControl.proto\"\xa6\x01\n\x12NVLThrottleControl\x12\x10\n\x08throttle\x18\x01 \x01(\x05\x12\x1a\n\x12\x64isable_start_stop\x18\x02 \x01(\x08\x12\x18\n\x10shutdown_vehicle\x18\x03 \x01(\x08\x12\x14\n\x0csound_buzzer\x18\x04 \x01(\x08\x12\x1a\n\x12\x61\x63k_message_serial\x18\x05 \x02(\x08\x12\x16\n\x0emessage_serial\x18\x06 \x01(\r')
)




_NVLTHROTTLECONTROL = _descriptor.Descriptor(
  name='NVLThrottleControl',
  full_name='NVLThrottleControl',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='throttle', full_name='NVLThrottleControl.throttle', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disable_start_stop', full_name='NVLThrottleControl.disable_start_stop', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shutdown_vehicle', full_name='NVLThrottleControl.shutdown_vehicle', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sound_buzzer', full_name='NVLThrottleControl.sound_buzzer', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ack_message_serial', full_name='NVLThrottleControl.ack_message_serial', index=4,
      number=5, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message_serial', full_name='NVLThrottleControl.message_serial', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=195,
)

DESCRIPTOR.message_types_by_name['NVLThrottleControl'] = _NVLTHROTTLECONTROL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NVLThrottleControl = _reflection.GeneratedProtocolMessageType('NVLThrottleControl', (_message.Message,), dict(
  DESCRIPTOR = _NVLTHROTTLECONTROL,
  __module__ = 'NVLThrottleControl_pb2'
  # @@protoc_insertion_point(class_scope:NVLThrottleControl)
  ))
_sym_db.RegisterMessage(NVLThrottleControl)


# @@protoc_insertion_point(module_scope)
