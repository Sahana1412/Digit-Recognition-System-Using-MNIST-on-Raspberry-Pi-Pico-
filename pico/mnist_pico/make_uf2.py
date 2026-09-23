import struct
from pathlib import Path

BIN_FILE = Path("build/mnist_pico.bin")
UF2_FILE = Path("build/mnist_pico.uf2")

# RP2040 UF2 family ID
RP2040_FAMILY_ID = 0xE48BFF56

# RP2040 flash starts at 0x10000000
FLASH_ADDRESS = 0x10000000

# UF2 magic numbers
MAGIC_START0 = 0x0A324655
MAGIC_START1 = 0x9E5D5157
MAGIC_END = 0x0AB16F30

# UF2 format
PAYLOAD_SIZE = 256
UF2_BLOCK_SIZE = 512

# Check input file
if not BIN_FILE.exists():
    print("ERROR: build/mnist_pico.bin was not found.")
    raise SystemExit(1)

data = BIN_FILE.read_bytes()

if len(data) == 0:
    print("ERROR: mnist_pico.bin is empty.")
    raise SystemExit(1)

# Number of UF2 blocks
num_blocks = (len(data) + PAYLOAD_SIZE - 1) // PAYLOAD_SIZE

uf2_blocks = []

for block_number in range(num_blocks):

    # Read 256-byte firmware chunk
    start = block_number * PAYLOAD_SIZE
    chunk = data[start:start + PAYLOAD_SIZE]

    # Pad final chunk to exactly 256 bytes
    if len(chunk) < PAYLOAD_SIZE:
        chunk += b"\x00" * (PAYLOAD_SIZE - len(chunk))

    target_address = FLASH_ADDRESS + start

    # Family ID present
    flags = 0x00002000

    # 32-byte UF2 header
    header = struct.pack(
        "<8I",
        MAGIC_START0,
        MAGIC_START1,
        flags,
        target_address,
        PAYLOAD_SIZE,
        block_number,
        num_blocks,
        RP2040_FAMILY_ID
    )

    # 220 bytes padding:
    # 32 header + 256 payload + 220 padding + 4 magic = 512
    padding = bytes(220)

    block = (
        header
        + chunk
        + padding
        + struct.pack("<I", MAGIC_END)
    )

    # Every UF2 block MUST be exactly 512 bytes
    if len(block) != UF2_BLOCK_SIZE:
        print(
            f"ERROR: Block {block_number} has size "
            f"{len(block)}, expected 512."
        )
        raise SystemExit(1)

    uf2_blocks.append(block)

# Write UF2
UF2_FILE.write_bytes(b"".join(uf2_blocks))

print()
print("======================================")
print("       UF2 CREATED SUCCESSFULLY")
print("======================================")
print(f"Input file : {BIN_FILE}")
print(f"Output file: {UF2_FILE}")
print(f"BIN size   : {len(data)} bytes")
print(f"UF2 size   : {UF2_FILE.stat().st_size} bytes")
print(f"UF2 blocks : {num_blocks}")
print("======================================")