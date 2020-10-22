#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Encode and decode afproto frames. For more information on the protocol see
https://github.com/greghaynes/Afproto/
"""

import crc16
import struct

START_BYTE = 0x7B
ESC_BYTE = 0x7E
END_BYTE = 0x7D
LINEFEED_BYTE = 0x0D
CARRIAGE_RET_BYTE = 0x0A


def print_iter(tag, data):
    return  # -----------------------------------------------> DISABLED <----
    # print("\n%s: " % tag,end=" ")
    # for x in data:
    #    print(str(hex(x)) + " ", end =" ")
    # print("")


def unescape_data(data):
    '''
    Takes in a string and returns the unescaped data
    '''

    print_iter("IZ UNESKPEJPA: ", data)

    ret = bytearray()
    prev_escape = False
    for char_ in data:
        if not prev_escape:
            if char_ == ESC_BYTE:
                # print("ESC")
                prev_escape = True
            else:
                # print("%s" % hex(char_))
                ret.append(char_)
        else:
            # print("%s" % hex(char_^20))
            ret.append(char_ ^ 0x20)
            prev_escape = False

    if prev_escape:
        raise ValueError('Invalid data, ends in escape byte')

    return ret


def escape_data(data):
    """ Takes in a string and returns an escaped version of the string

    :param data:
    :return:
    """


    print_iter("IZ ESKEJPANJA: ", data)

    ret = bytearray()
    for char_ in data:
        if char_ in (START_BYTE, ESC_BYTE, END_BYTE, LINEFEED_BYTE, CARRIAGE_RET_BYTE):
            ret.append(ESC_BYTE)
            # print(hex(ESC_BYTE))
            if ((char_ ^ 0x20) in (START_BYTE, ESC_BYTE, END_BYTE, LINEFEED_BYTE, CARRIAGE_RET_BYTE)):
                print("%s JAKO VELIKI PROBLEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" % hex(char_ ^ 0x20))
            ret.append(char_ ^ 0x20)
            # print(hex(char_^0x20))
        else:
            ret.append(char_)
            # print(hex(char_))
    return ret


def afproto_get_data(raw_frame):
    """ Returns a tuple of (data, extra_data). The data is data which was decoded
    from the passed frame, the extra_data is data that was not considered for
    parsing (and should probably be sent in a subsequent call).
    If no valid frame was found, data is None
    extra will always be a string (empty string if all data was considered).

    :param raw_frame:
    :return:
    """

    start_ndx = raw_frame.find(START_BYTE)
    if start_ndx == -1:
        return (None, '')

    end_ndx = raw_frame.find(END_BYTE, start_ndx + 1)
    if end_ndx == -1:
        return (None, raw_frame[start_ndx:])

    contents = unescape_data(raw_frame[start_ndx + 1:end_ndx])
    data = contents[:-2]
    message_id = contents[:1]

    print_iter("UNESKEJPANO: ", data)

    # print("\n############ PORUKA TIPA %s #################\n" % (str(hex(message_id[0]))))

    # sent_crc = (contents[-1] << 8)+contents[-2]

    # print((contents[-1] << 8)+contents[-2])
    # print("--------------------")

    calc_crc1 = crc16.crc16_buff(data) & 0x00FF
    calc_crc2 = (crc16.crc16_buff(data) & 0xFF00) >> 8

    sent_crc1 = contents[-2]
    sent_crc2 = contents[-1]

    # print("XXXXX> ", hex(calc_crc1), hex(calc_crc2))
    # print("YYYYY> ", hex(sent_crc1), hex(sent_crc2))

    #    print("SENT CRC: ",hex(int.from_bytes(sent_crc1, byteorder='little')),hex(int.from_bytes(sent_crc2, byteorder='little')))
    #   print("CALC CRC: ", int.from_bytes(calc_crc1, byteorder='little'), int.from_bytes(calc_crc2, byteorder='little'))

    if (sent_crc1, sent_crc2) != (calc_crc1, calc_crc2):
        print('invalid crc ')
        return (None, raw_frame[end_ndx + 1:])

    return (data, raw_frame[end_ndx + 1:])


def afproto_frame_data(message_id, data):
    '''
    Returns a raw frame which contains the supplied data
    '''

    data = bytes([message_id]) + data

    print_iter("IZ FREJMANJA: ", data)

    # print_iter("DBG1",data)

    ret = bytearray()
    ret.append(START_BYTE)

    crc1 = bytes([(crc16.crc16_buff(data) & 0x00FF)])
    crc2 = bytes([((crc16.crc16_buff(data) & 0xFF00) >> 8)])

    # print("CRC FOR FRAME DATA: ", crc16.crc16_buff(data))

    data = data + crc1 + crc2

    esc_data = escape_data(data)

    # print_iter("DBG2",esc_data)

    # print("TYPE: %s" % type(esc_data))

    for d in esc_data:
        ret.append(d)

    ret.append(END_BYTE)
    return ret

# def main():
#    'Main method'
# resp = afproto_get_data(afproto_frame_data('XtestY') + afproto_frame_data('XothertestY'))
#    resp = afproto_get_data(afproto_frame_data('XtestY'))
#    print(resp, afproto_get_data(resp[1]))


# if __name__ == '__main__':
#    main()
