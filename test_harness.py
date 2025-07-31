from ecm_protocol import ECM, BUEGB_RT_MAP
import struct

# This script serves as a test harness to verify the ECM data parsing logic.

# --- Create a realistic, sample data packet (107 bytes) ---
# This simulates a real response from the ECM.
# We will set some key values:
# - RPM (offset 11, size 2): 1200
# - Engine Temp (offset 30, size 2): 90 C (Raw value = (90 + 40) / 0.1 = 1300)
# - Throttle Pos (offset 27, size 1): 5% (Raw value = 5 / 0.392157 = 12.75 -> 13)

sample_data = bytearray(107)

# Set RPM to 1200
sample_data[11:13] = struct.pack('>H', 1200)

# Set Engine Temp to 90 C
sample_data[30:32] = struct.pack('>H', 1300)

# Set Throttle Position to 5%
sample_data[27] = 13

# --- Test the Parser ---
def main():
    """Main function to run the test."""
    print("--- Running ECM Protocol Test Harness ---")

    # 1. Instantiate the ECM class with our data map
    ecm = ECM(BUEGB_RT_MAP)

    # 2. Parse the sample data packet
    parsed_data = ecm.parse_realtime_data(sample_data)

    print("\n--- Successfully Parsed Data ---")

    # 3. Print key values to verify correctness
    print(f"RPM: {parsed_data.get('RPM'):.0f}")
    print(f"Engine Temp (C): {parsed_data.get('TE'):.1f}")
    print(f"Throttle Pos (%): {parsed_data.get('TPP'):.1f}")
    print(f"Battery (V): {parsed_data.get('Bat'):.2f}")

    print("\n--- Test Harness Complete ---")

if __name__ == "__main__":
    main()
