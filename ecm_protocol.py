import struct

# This file will contain the core protocol definition for communicating with Buell ECMs.

# Real-time data map for the BUEGB ECM family.
# Format: 'VarName': (offset, size, scale, translate)
BUEGB_RT_MAP = {
    'SOH': (0, 1, 1.0, 0.0),
    'Source': (1, 1, 1.0, 0.0),
    'Destination': (2, 1, 1.0, 0.0),
    'Len': (3, 1, 1.0, 0.0),
    'EOH': (4, 1, 1.0, 0.0),
    'SOT': (5, 1, 1.0, 0.0),
    'ACK': (6, 1, 1.0, 0.0),
    'KConfig_LD': (7, 1, 1.0, 0.0),
    'MS_10': (8, 1, 0.01, 0.0),
    'Seconds': (9, 2, 1.0, 0.0),
    'RPM': (11, 2, 1.0, 0.0),
    'Adv1': (13, 2, 0.0025, 0.0),
    'Adv2': (15, 2, 0.0025, 0.0),
    'TabFuel1_Raw': (17, 2, 1.0, 0.0),
    'TabFuel1': (17, 2, 0.026666, 0.0),
    'TabFuel2_Raw': (19, 2, 1.0, 0.0),
    'TabFuel2': (19, 2, 0.026666, 0.0),
    'Fuel1': (21, 2, 0.00133, 0.0),
    'Fuel2': (23, 2, 0.00133, 0.0),
    'TPD': (25, 2, 0.1, 0.0),
    'RLoad': (27, 1, 1.0, 0.0),
    'TPP': (27, 1, 0.392157, 0.0),
    'Bat': (28, 2, 0.01, 0.0),
    'TE': (30, 2, 0.1, -40.0),
    'TE_F': (30, 2, 0.18, -40.0),
    'TA': (32, 2, 0.1, -40.0),
    'TA_F': (32, 2, 0.18, -40.0),
    'AO2': (34, 2, 1.0, 0.0),
    'O2': (34, 2, 0.004887585, 0.0),
    'CrBat': (36, 2, 0.00133, 0.0),
    'CrTE': (38, 2, 0.1, 0.0),
    'CrTA': (40, 2, 0.1, 0.0),
    'CrAcc': (42, 2, 0.1, 0.0),
    'CrDec': (44, 2, 0.1, 0.0),
    'CrWOT': (46, 2, 0.1, 0.0),
    'CrIdle': (48, 2, 0.1, 0.0),
    'CrOL': (50, 2, 0.1, 0.0),
    'LFuel_LD': (52, 2, 0.1, 0.0),
    'FBFuel': (54, 2, 0.1, 0.0),
    'Flags0': (56, 1, 1.0, 0.0),
    'Flags1': (57, 1, 1.0, 0.0),
    'Flags2': (58, 1, 1.0, 0.0),
    'Flags3': (59, 1, 1.0, 0.0),
    'Flags4': (60, 1, 1.0, 0.0),
    'Flags5': (61, 1, 1.0, 0.0),
    'Flags6': (62, 1, 1.0, 0.0),
    'Unknown-63': (63, 2, 1.0, 0.0),
    'ABaro': (63, 1, 1.0, 0.0),
    'ABAS': (65, 2, 1.0, 0.0),
    'ABAS_V': (65, 2, 0.004887585, 0.0),
    'CDiag0': (67, 1, 1.0, 0.0),
    'CDiag1': (68, 1, 1.0, 0.0),
    'CDiag2': (69, 1, 1.0, 0.0),
    'CDiag3': (70, 1, 1.0, 0.0),
    'RDiag0': (71, 1, 1.0, 0.0),
    'RDiag1': (72, 1, 1.0, 0.0),
    'RDiag2': (73, 1, 1.0, 0.0),
    'RDiag3': (74, 1, 1.0, 0.0),
    'HDiag0_LD': (75, 1, 1.0, 0.0),
    'HDiag1_LD': (76, 1, 1.0, 0.0),
    'HDiag2_LD': (77, 1, 1.0, 0.0),
    'HDiag3_LD': (78, 1, 1.0, 0.0),
    'Unknown-79': (79, 1, 1.0, 0.0),
    'Unknown-80': (80, 1, 1.0, 0.0),
    'Unknown-81': (81, 1, 1.0, 0.0),
    'Unknown-82': (82, 1, 1.0, 0.0),
    'RC': (83, 1, 1.0, 0.0),
    'DOut': (84, 1, 1.0, 0.0),
    'DIn': (85, 1, 1.0, 0.0),
    'ACoil1': (86, 1, 1.0, 0.0),
    'ACoil2': (87, 1, 1.0, 0.0),
    'AInj1': (88, 1, 1.0, 0.0),
    'AInj2': (89, 1, 1.0, 0.0),
    'ATPS': (90, 2, 1.0, 0.0),
    'ATPS_V': (90, 2, 0.004887585, 0.0),
    'ABat': (92, 2, 1.0, 0.0),
    'ATE': (94, 1, 1.0, 0.0),
    'ATE_V': (94, 1, 0.019607843, 0.0),
    'ATA': (95, 1, 1.0, 0.0),
    'ATA_V': (95, 1, 0.019607843, 0.0),
    'AFP': (96, 1, 1.0, 0.0),
    'ACF': (97, 1, 1.0, 0.0),
    'Fan_Duty': (98, 1, 1.0, 0.0),
    'VSS_Count': (99, 1, 1.0, 0.0),
    'VS_RPM_Ratio': (100, 1, 1.0, 0.0),
    'CDiag4': (101, 1, 1.0, 0.0),
    'RDiag4': (102, 1, 1.0, 0.0),
    'HDiag4_LD': (103, 1, 1.0, 0.0),
    'EOT': (105, 1, 1.0, 0.0),
    'CHKSM': (106, 1, 1.0, 0.0),
}

def _bytes_to_int(byte_data):
    """Converts a byte array to an integer."""
    if len(byte_data) == 1:
        return byte_data[0]
    elif len(byte_data) == 2:
        return struct.unpack('>H', byte_data)[0]  # Big-endian, 2 bytes
    else:
        return int.from_bytes(byte_data, 'big')

class ECM:
    """Handles the logic for communicating with the Buell ECM."""
    def __init__(self, ecm_map):
        self.ecm_map = ecm_map

    def parse_realtime_data(self, raw_data):
        """Parses a raw real-time data packet into a dictionary of values."""
        parsed_data = {}
        for var_name, (offset, size, scale, translate) in self.ecm_map.items():
            if offset + size > len(raw_data):
                continue # Skip if data packet is too short for this variable

            # Extract the raw byte value from the packet
            raw_value_bytes = raw_data[offset:offset + size]
            raw_int_value = _bytes_to_int(raw_value_bytes)

            # Apply the formula: RealValue = (RawValue * scale) + translate
            real_value = (raw_int_value * scale) + translate
            parsed_data[var_name] = real_value

        return parsed_data
