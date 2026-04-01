from bitstring import BitStream, ConstBitStream, pack

VERSION = 1


def oc1_encode(
    osc1_type: int,
    osc1_offset: float,
    osc1_amplitude: float,
    osc2_type: int,
    osc2_offset: float,
    osc2_amplitude: float,
    osc3_type: int,
    osc3_offset: float,
    osc3_amplitude: float
) -> bytes:
    oc = 1
    bs = BitStream()

    bs += pack('uint8', VERSION)
    bs += pack('uint8', oc)

    bs += pack('uint32', osc1_type)
    bs += pack('float32', osc1_offset)
    bs += pack('float32', osc1_amplitude)
    bs += pack('uint32', osc2_type)
    bs += pack('float32', osc2_offset)
    bs += pack('float32', osc2_amplitude)
    bs += pack('uint32', osc3_type)
    bs += pack('float32', osc3_offset)
    bs += pack('float32', osc3_amplitude)

    return bs.tobytes()


def oc1_decode(bs: ConstBitStream) -> dict:
    rs = {}

    rs['osc1_type'] = bs.read('uint32')
    rs['osc1_offset'] = bs.read('float32')
    rs['osc1_amplitude'] = bs.read('float32')
    rs['osc2_type'] = bs.read('uint32')
    rs['osc2_offset'] = bs.read('float32')
    rs['osc2_amplitude'] = bs.read('float32')
    rs['osc3_type'] = bs.read('uint32')
    rs['osc3_offset'] = bs.read('float32')
    rs['osc3_amplitude'] = bs.read('float32')

    return rs


def oc2_encode(key: int) -> bytes:
    oc = 2
    bs = BitStream()

    bs += pack('uint8', VERSION)
    bs += pack('uint8', oc)

    bs += pack('uint32', key)

    return bs.tobytes()


def oc2_decode(bs: ConstBitStream) -> dict:
    rs = {}

    rs['key'] = bs.read('uint32')

    return rs


def oc3_encode(key: int) -> bytes:
    oc = 3
    bs = BitStream()

    bs += pack('uint8', VERSION)
    bs += pack('uint8', oc)

    bs += pack('uint32', key)

    return bs.tobytes()


def oc3_decode(bs: ConstBitStream) -> dict:
    rs = {}

    rs['key'] = bs.read('uint32')

    return rs


def oc4_encode() -> bytes:
    oc = 4
    bs = BitStream()

    bs += pack('uint8', VERSION)
    bs += pack('uint8', oc)

    return bs.tobytes()


def oc4_decode(bs: ConstBitStream) -> dict:
    return {}
