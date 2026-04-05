#Defines how data is structured when sent between the sender and receiver

#Packet Structure: [START][MSG_TYPE][DEVICE_ID][PACKET_ID][DATA][CHECKSUM][END]
def create_packet(msg_type, device_id, packet_id, data):
    checksum = (msg_type + device_id + packet_id + data) % 256
    return bytearray([126, msg_type, device_id, packet_id, data, checksum, 127])


def validate_packet(packet):
    if len(packet) != 7:
        return {"valid": False, "error": "Invalid length"}
    if packet[0] != 126 or packet[6] !=127 : 
        return {"valid": False, "error": "Invalid start/end"}
    msg_type = packet[1]
    device_id = packet[2]
    packet_id = packet[3]
    data = packet[4]
    checksum = packet[5]

    checksum_calculated = (msg_type + device_id + packet_id + data) % 256
    return {"valid": checksum == checksum_calculated, "error": "Checksum mismatch" if checksum != checksum_calculated else None}


def parse_packet(packet):
    packet_validation = validate_packet(packet)
    if not packet_validation["valid"]:
        return packet_validation
    msg_type = packet[1]
    device_id = packet[2]
    packet_id = packet[3]
    data = packet[4]
    return {"valid": True, "error": None, "msg_type": msg_type, "device_id": device_id, "packet_id": packet_id, "data": data}