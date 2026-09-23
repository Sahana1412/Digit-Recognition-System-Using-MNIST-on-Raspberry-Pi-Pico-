import struct
from pathlib import Path

BIN_FILE = Path("pico/mnist_pico/build/mnist_pico.bin")
UF2_FILE = Path("pico/mnist_pico/build/mnist_pico.uf2")

RP2040_FAMILY_ID = 0xE48BFF56
FLASH_ADDRESS = 0x10000000

MAGIC_START0 = 0x0A324655
MAGIC_START1 = 0x9E5D5157
MAGIC_END = 0x0AB16F30

PAYLOAD_SIZE = 256
UF2_BLOCK_SIZE = 512

if not BIN_FILE.exists():
    print("ERROR: mnist_pico.bin was not found.")
    print(f"Expected: {BIN_FILE.resolve()}")
    raise SystemExit(1)

data = BIN_FILE.read_bytes()

if len(data) == 0:
    print("ERROR: mnist_pico.bin is empty.")
    raise SystemExit(1)

num_blocks = (len(data) + PAYLOAD_SIZE - 1) // PAYLOAD_SIZE

uf2_blocks = []

for block_number in range(num_blocks):

    start = block_number * PAYLOAD_SIZE

    chunk = data[start:start + PAYLOAD_SIZE]

    if len(chunk) < PAYLOAD_SIZE:
        chunk += b"\x00" * (PAYLOAD_SIZE - len(chunk))

    target_address = FLASH_ADDRESS + start

    flags = 0x00002000

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

    padding = bytes(220)

    block = (
        header
        + chunk
        + padding
        + struct.pack("<I", MAGIC_END)
    )

    if len(block) != UF2_BLOCK_SIZE:
        print(
            f"ERROR: Block {block_number} has size "
            f"{len(block)}, expected 512."
        )
        raise SystemExit(1)

    uf2_blocks.append(block)

UF2_FILE.write_bytes(b"".join(uf2_blocks))

print()
print("======================================")
print("       UF2 CREATED SUCCESSFULLY")
print("======================================")
print(f"Input file : {BIN_FILE.resolve()}")
print(f"Output file: {UF2_FILE.resolve()}")
print(f"BIN size   : {len(data)} bytes")
print(f"UF2 size   : {UF2_FILE.stat().st_size} bytes")
print(f"UF2 blocks : {num_blocks}")
print("======================================")