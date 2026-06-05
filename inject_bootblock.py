import os
import sys

def inject_bootblock(bin_input, adf_output):
    try:
        # Existence validation
        if not os.path.exists(bin_input):
            print(f"Error: The file '{bin_input}' could not be found in the current path.")
            return
            
        with open(bin_input, 'rb') as f:
            datos_bootblock = f.read()
            
        print(f"-> Loading bootblock: {bin_input} ({len(datos_bootblock)} bytes)")

        # Create buffer
        bootblock = bytearray(1024)
        copy_size = min(len(datos_bootblock), 1024)
        bootblock[0:copy_size] = datos_bootblock[0:copy_size]
        
        # Checksum
        bootblock[4:8] = b'\x00\x00\x00\x00'
        checksum = 0
        for i in range(0, 1024, 4):
            val = int.from_bytes(bootblock[i:i+4], byteorder='big')
            checksum += val
            if checksum > 0xffffffff:
                checksum = (checksum & 0xffffffff) + 1
        
        final_checksum = checksum ^ 0xffffffff
        bootblock[4:8] = final_checksum.to_bytes(4, byteorder='big')
        
        # Create ADF
        total_adf_size = 901120 
        with open(adf_output, 'wb') as f:
            f.write(bootblock)
            f.write(b'\x00' * (total_adf_size - 1024))
            
        print(f"-> SUCCESS! Floppy disk generated: {adf_output}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print(f"Error: 2 arguments expected, {len(sys.argv)-1} received .")
        print("Correct use: python inject_bootblock.py <bootblock> <disk.adf>")
    else:
        bootblock_file = sys.argv[1]
        adf_file = sys.argv[2]
        inject_bootblock(bootblock_file, adf_file)