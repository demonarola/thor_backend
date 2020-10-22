#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import traceback
import ujson
import datetime

# LOAD TRACEBACK FUNCT.
from traceback import format_exc

# LOAD TWISTED DEPENDENCIES
from txpostgres import txpostgres
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

# LOAD PROTOBUF DEPENDENCIES
import google.protobuf

import NVLGPSStatus_pb2
import NVLThrottleControl_pb2

# FROM CONFIG IMPORT DB CONNECTION CONF
from web_backend.config import dsn, DEBUG

from web_backend.backend_services.nvl_tracker_service.afproto import *
from web_backend.backend_services.nvl_tracker_service.nvltracker_server_specification import *

# CREATE TX POSTGRES CONNECTION
conn = txpostgres.ConnectionPool(None, min=3, **dsn)
d = conn.start()


# LOCATION web_backend/tests/nvl_tracker_service
# Protocol Implementation

# This is just about the simplest possible protocol
# DEBUG = True


class Echo(Protocol):
    data_rx = 0
    mode = 0
    COUNTER = 0
    HW_MOD_ID = None
    ITER_LOOP = 0
    DEFAULT_THROTTLE = 100
    COLLISION_AVOIDANCE_STATE = False
    COLLISION_AVOIDANCE_THROTTLE = 25
    MINIMAL_DISTANCE = 60
    small_loop_counter = 0
    temp_message_counter = 0
    LAST_THROTTLE_VALUE = 0
    # Check if connection is just opened.
    # On first connection send state to the device 
    FIRST_CONTACT = True

    def connectionMade(self):
        """ On connectionMade start callbacks that will trigger
        functions written bellow to run periodically.

        :return:
        """
        # ... your code
        # cancel connection in 2 minutes
        # reactor.callLater(10, self.transport.loseConnection)"
        if DEBUG:
            print('CONNECTION MADE')
        reactor.callLater(2, self.pool_commands)
        reactor.callLater(0.8, self.pool_check_collision_avoidance_state)
        reactor.callLater(0.8, self.pool_check_throttle_value)

    def set_collision_avoidance_system_state(self, data):
        """ On polygon intersection trigger action.

        :param data:
        :return:
        """

        # TODO: REMOVE IN PRODUCTION
        if DEBUG:
            print('========== set_collision_avoidance_system_state ==========\n')
            print(data)

        if len(data) > 0:
            # THIS IS A FILTER THAT RETURNS ONLY DATA ON WHICH POINT AND POLYGON IS INTERSECTED.
            # EXAMPLE DATA : [(False, 51), (True, 45)]
            # WE ONLY NEED TO PROCESS INTERSECTED DATA
            print(data)
            self.COLLISION_AVOIDANCE_STATE = True
        else:
            self.COLLISION_AVOIDANCE_STATE = False

    def trigger_action_on_intersect_detect(self, data):
        """ On polygon intersection trigger creation of command

        :param data:
        :return:
        """
        print('========== INTERSECTED ACTION COMMAND CREATION ==========\n')
        print(data)
        if len(data) > 0:
            for action in data:
                intersect_detect = conn.runQuery(
                    create_hw_command_element_on_intersect_query, (action[3], action[2], action[1], self.HW_MOD_ID,))

    def process_saved_hw_module_user_pos(self, data):
        """ On inserted point check if point intersects with
        element (Polygon / Circle). Geo data of polygons is located in table public.user_hw_action_collection
        and it is materialized view that is updated on location/action change.
        :param data:
        :return:
        """
        # TODO: REMOVE IN PRODUCTION
        if DEBUG:
            print('process_saved_hw_module_user_pos')
            print(data)

        if len(data) > 0:
            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print('THIS IS DATA IN process_saved_hw_module_user_pos: {}'.format(data))
                pos_id = data[0][0]
                intersect_detect = conn.runQuery(query_intersect, (pos_id,))
                intersect_detect.addCallback(self.trigger_action_on_intersect_detect)

    def process_device_initial_state(self, data):
        if DEBUG:
            print('process_device_initial_state')
            print(data)

        if len(data) > 0:
            field_value = data[0][0]
            throttle_control = NVLThrottleControl_pb2.NVLThrottleControl()
            throttle_control.disable_start_stop = True if field_value in ['true', '1', 1, 1.0, b'true', 'True', b'True'] else False
            throttle_control.ack_message_serial = False

            ser_obj = throttle_control.SerializeToString()
            ser_frame = afproto_frame_data(0xce, ser_obj)

            self.transport.write(ser_frame)

    def create_user_command_element(self, data):
        """ On detected value create command

        :param data:
        :return:
        """
        # TODO: REMOVE IN PRODUCTION
        if DEBUG:
            print('create_user_command_element')
            print(data)

        if len(data) > 0 and self.HW_MOD_ID:
            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print('THIS IS DATA IN create_user_command_element: {}'.format(data))
            
            if self.LAST_THROTTLE_VALUE != data[0][0]:
                conn.runQuery(
                    create_hw_command_element_query, (
                        data[0][0],
                        self.HW_MOD_ID
                    ))

                self.LAST_THROTTLE_VALUE = data[0][0]
                # TO REMOVE
                # print("create_user_command_element THROTTLE: {}".format(data[0][0]))
                # print(self.LAST_THROTTLE_VALUE)
                # if data[0][0] != 100:
                #     reactor.stop()

    def get_command_data(self, data):
        """

        :param data:
        :return:
        """

        # TODO: REMOVE IN PRODUCTION
        if DEBUG:
            print('GET_command_data_CALLED')
            print(datetime.datetime.now())

        if len(data) > 0:

            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print('THIS IS DATA: {}'.format(data))
                print(85 * '-')
                print(data)
                print(85 * ':')

            command_id = data[0][0]
            proto_field = data[0][1]
            # field_type = data[0][2]
            field_value = data[0][3]
            ack_message = data[0][4]

            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print(
                    '''
                    COMMAND_ID {}: \n COMMAND_TYPE: {} \n PROTO_FIELD: {} \n
                     FIELD_VALUE: {} \n FIELD_VALUE_TYPE: {} \n ACK_MESSAGE: {} \n ACK_MESSAGE_TYPE: {}'''.format(
                        command_id, type(command_id), proto_field, field_value,
                        type(field_value), ack_message, type(ack_message)))

            throttle_control = NVLThrottleControl_pb2.NVLThrottleControl()
            if proto_field == 'throttle':
                throttle_control.throttle = int(field_value)
            if proto_field == 'disable_start_stop':
                throttle_control.disable_start_stop = True if field_value in ['true', '1', 1, 1.0, b'true', 'True', b'True'] else False
            if proto_field == 'shutdown_vehicle':
                throttle_control.shutdown_vehicle = True if field_value in ['true', '1', 1, 1.0, b'true', 'True', b'True'] else False
            if proto_field == 'sound_buzzer':
                throttle_control.sound_buzzer = True if field_value in ['true', '1', 1, 1.0, b'true', 'True', b'True'] else False

            if ack_message is True:
                throttle_control.ack_message_serial = True  # We request ACK
            throttle_control.message_serial = int(command_id)

            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print('THIS IS THROTTLE MESSAGE SERIAL : {}'.format(throttle_control.message_serial))

            ser_obj = throttle_control.SerializeToString()
            ser_frame = afproto_frame_data(0xce, ser_obj)

            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print('>>>>>>>>>>>>>>>>>>>>COMMAND DATA SEND FRAME <<<<<<<<<<<<<<<<<<<<<')
                print(datetime.datetime.now())
            self.transport.write(ser_frame)
            print(datetime.datetime.now())
            print('>>>>>>>>>>>>>>>>>>>>>>AAAAAAAAAAAAAAAAAAAAA>>>>>>>>>>>>>>>>>>>>>>>>>')

    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        self.data_rx = 1

        try:

            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print('data: {}, type_of_data: {}'.format(data, type(data)))

            # print("--NVLTRK--> ", end =" ")
            # for x in data:
            #    print(str(hex(x)) + " ", end =" ")
            # print("")

            ########################################################
            #
            # /* ----- Transmit message ID ----- */
            # define SP_MSG_TYPE__NVLGPSStatus               0xA
            # define SP_MSG_TYPE__NVLThrottleControl_ACK     0xB
            #
            # /* -----  Receive message ID ----- */
            # define SP_MSG_TYPE__NVLThrottleControl         0xCE
            #
            ########################################################

            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            rawd = afproto_get_data(data)

            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print('RAW DATA: {}'.format(rawd))
            message_id = rawd[0][0]

            # TODO: REMOVE IN PRODUCTION
            if DEBUG:
                print("\n############ PORUKA TIPA %s #################\n" % (str(hex(message_id))))

            if message_id == 0xB:
                if self.HW_MOD_ID is not None:
                    # TODO: REMOVE IN PRODUCTION
                    if DEBUG:
                        print("\n\n\n\n##############>> ACK MESSAGE HAS RECIEVED <<###################\n\n\n\n\n")

                    throttle_control = NVLThrottleControl_pb2.NVLThrottleControl()
                    throttle_control.ParseFromString(rawd[0][1:])
                    # TODO: REMOVE IN PRODUCTION
                    if DEBUG:
                        print((int(throttle_control.message_serial), self.HW_MOD_ID), throttle_control)

                    conn.runQuery(
                        query_change_command_state_for_device, (int(throttle_control.message_serial), self.HW_MOD_ID))

            else:
                # PROCESSING GPS DATA FROM DEVICE.
                gpsstatus = NVLGPSStatus_pb2.NVLGPSStatus()
                gpsstatus.ParseFromString(rawd[0][1:])

                # --------------- REMOVE - FUEL LEVEL DEBUG ------------------------
                print('\n\n\n\n')             
                print(30 * '*')
                print(gpsstatus.fuel_level)
                print(30 * '*')
                print('\n\n\n\n')              
                # --------------- REMOVE - FUEL LEVEL DEBUG ------------------------

                # TODO: REMOVE IN PRODUCTION
                if DEBUG:
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>ZIE KORDINATEN<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                    print(gpsstatus)

                # TEMP COORDINATE LIST USED TO FAKE DATA
                # TODO: REMOVE IN PRODUCTION

                # TODO: REMOVE IN PRODUCTION
                if DEBUG:
                    print('IN COUNTER {}'.format(self.ITER_LOOP % 3))
                dte = '{0:02d}-{1:02d}-{2:02d}'.format(int(gpsstatus.date_day), int(gpsstatus.date_month), int(gpsstatus.date_year))
                record_time = datetime.datetime.strptime(dte,'%d-%M-%y').strftime('%M/%d/%y')
                value_tuple = (
                    gpsstatus.longitude, gpsstatus.latitude,
                    '',
                    ujson.dumps({
                        'message_id': str(message_id),
                        'date': record_time,
                        'time': record_time + ' ' + '{0:02d}:{1:02d}:{2:02d}'.format(int(gpsstatus.time_hours), int(gpsstatus.time_minutes), int(gpsstatus.time_seconds)),
                        'time_microseconds': '{}'.format(str(gpsstatus.time_microseconds)),
                        'gps_active': gpsstatus.gps_active if gpsstatus.gps_active is not None else None,
                        'speed': (
                            '{:.1f}'.format(float(gpsstatus.speed_over_ground_knots)) if gpsstatus.speed_over_ground_knots is not None else None),
                        'magnetic_var': str(
                            gpsstatus.magnetic_variation) if gpsstatus.magnetic_variation is not None else None,
                        'track_angle': gpsstatus.track_angle_degrees if gpsstatus.track_angle_degrees is not None else None,
                        'fuel_level': gpsstatus.fuel_level if gpsstatus.fuel_level is not None else None,
                        'voltage_level': gpsstatus.voltage_level if gpsstatus.voltage_level is not None else None,
                        'vehicle_running': gpsstatus.vehicle_running if gpsstatus.vehicle_running is not None else None

                    }),
                    gpsstatus.tracker_id.decode()
                )

                # TODO: REMOVE IN PRODUCTION
                if DEBUG:
                    print(value_tuple)
                    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

                if gpsstatus.tracker_id is not None:
                    # TODO: REMOVE IN PRODUCTION
                    if DEBUG:
                        print('SETTING HW MODULE ID: {}'.format(gpsstatus.tracker_id.decode()))
                    # TODO: REMOVE: HARDCODED VALUE IN PRODUCTION: PROPER VALUE:
                    #  self.HW_MOD_ID = gpsstatus.tracker_id.decode()
                    self.HW_MOD_ID = gpsstatus.tracker_id.decode()

                    if self.FIRST_CONTACT:
                        self.FIRST_CONTACT = False
                        set_inital_state = conn.runQuery(last_device_lock_state_query, (self.HW_MOD_ID, ))
                        set_inital_state.addCallback(self.process_device_initial_state)

                # TODO: REMOVE QUERY STR DETECT
                # conn.runQuery(query_str_detect, value_tuple)
                # SAVE POSITION IN TO THE HW MODULE USER POSITION TABLE
                hw_mod_user_pos_data = conn.runQuery(
                    create_hw_module_user_position_element_query, value_tuple)
                hw_mod_user_pos_data.addCallback(self.process_saved_hw_module_user_pos)

                # IF COLLISION AVOIDANCE SYSTEM IS ACTIVATED ON HW MODULE SAVE THE LAST POINT IN
                # HW_CAS TABLE
                if self.COLLISION_AVOIDANCE_STATE:
                    conn.runQuery(
                        upsert_collision_avoidance_system_last_point_query, (
                            gpsstatus.longitude, gpsstatus.latitude, datetime.datetime.now(),
                             self.HW_MOD_ID, gpsstatus.longitude, gpsstatus.latitude,
                            datetime.datetime.now()))

        except Exception as recdta_ext:
            print('Exception on nmea read erred with: {}, {}'.format(recdta_ext, format_exc()))

    def pool_commands(self):
        # TODO: REMOVE IN PRODUCTION
        if DEBUG:
            print("========== POOL COMMANDS CALLED! ==========\n")
            print("_________HW__MOD_______ID:{}_{}___________".format(self.HW_MOD_ID, type(self.HW_MOD_ID)))

        if self.HW_MOD_ID is not None:
            command_data = conn.runQuery(query_find_command_for_device, (self.HW_MOD_ID,))
            command_data.addCallback(self.get_command_data)

        reactor.callLater(2, self.pool_commands)

    def pool_check_collision_avoidance_state(self):
        # TODO: REMOVE IN PRODUCTION
        if DEBUG:
            print("========== POOL THROTTLE CONTROL CALLED! ==========\n")
            print("_________HW__MOD_______ID:{}_{}___________".format(self.HW_MOD_ID, type(self.HW_MOD_ID)))

        if self.HW_MOD_ID is not None:
            collision_data = conn.runQuery(check_collision_avoidance_system_query, (self.HW_MOD_ID,))
            collision_data.addCallback(self.set_collision_avoidance_system_state)

        reactor.callLater(0.8, self.pool_check_collision_avoidance_state)

    def pool_check_throttle_value(self):
        if self.HW_MOD_ID is not None:
            print(
                'pool_check_throttle_value: {} {} {} {}'.format(
                    self.COLLISION_AVOIDANCE_THROTTLE,
                    self.COLLISION_AVOIDANCE_STATE, self.HW_MOD_ID, self.MINIMAL_DISTANCE
                )
            )
            throttle_data = conn.runQuery(
                get_throttle_value_for_hw_module_module_id_query, (
                    self.COLLISION_AVOIDANCE_THROTTLE,
                    self.COLLISION_AVOIDANCE_STATE, self.HW_MOD_ID, self.MINIMAL_DISTANCE
                ))
            throttle_data.addCallback(self.create_user_command_element)

        reactor.callLater(0.8, self.pool_check_throttle_value)


def main():
    try:
        f = Factory()
        f.protocol = Echo
        reactor.listenTCP(8009, f)
        reactor.run()
    except Exception as err:
        print(30 * '-')
        print(err)
        traceback.print_exc()
        print(30 * '#')


if __name__ == '__main__':
    main()
