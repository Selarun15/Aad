from partial_container import PartialContainer
from dataclasses import dataclass
from typing import Optional
from remerkleable.basic import uint16, uint32, uint64, uint256
from remerkleable.bitfields import Bitvector
from remerkleable.byte_arrays import ByteList
from remerkleable.complex import Container

@dataclass
class Foo:
    a: uint64
    b: Optional[uint32]
    c: Optional[uint16]
    d: Optional[ByteList[4]]
    e: ByteList[4]

class Wrapper(Container):
    x: PartialContainer[Foo, 32]

# Test serialization
value = Wrapper(
    x=PartialContainer[Foo, 32](a=64, b=None, c=16, d=None, e=ByteList[4]([0x42]))
)
expected_bytes = bytes.fromhex("0400000015000000400000000000000010000e00000042")
assert value.encode_bytes() == expected_bytes

# Test deserialization
assert Wrapper.decode_bytes(expected_bytes) == value

# Test merkleization
class Bar(Container):
    a: uint64
    ph01: uint256
    c: uint16
    ph03: uint256
    e: ByteList[4]
    ph05: uint256
    ph06: uint256
    ph07: uint256
    ph08: uint256
    ph09: uint256
    ph0a: uint256
    ph0b: uint256
    ph0c: uint256
    ph0d: uint256
    ph0e: uint256
    ph0f: uint256
    ph10: uint256
    ph11: uint256
    ph12: uint256
    ph13: uint256
    ph14: uint256
    ph15: uint256
    ph16: uint256
    ph17: uint256
    ph18: uint256
    ph19: uint256
    ph1a: uint256
    ph1b: uint256
    ph1c: uint256
    ph1d: uint256
    ph1e: uint256
    ph1f: uint256

class Baz(Container):
    data: Bar
    active_fields: Bitvector[32]

expected = Baz(
    data=Bar(a=value.x.a, c=value.x.c, e=value.x.e),
    active_fields=Bitvector[32]([True, False, True, False, True] + [False] * 27)
)
assert value.hash_tree_root() == expected.hash_tree_root()
