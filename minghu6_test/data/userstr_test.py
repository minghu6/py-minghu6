from minghu6.data.userstr import *


def test_custom_str():
    cs = CustomStr("aaa ")
    cs2 = cs.strip()
    assert cs2 == CustomStr("aaa")
    cs2.extra_attrs["status"] = "Y"

    assert isinstance(cs2, CustomStr)
    assert cs2 != CustomStr("aaa")
    assert cs2.extra_attrs["status"] == "Y"


def test_custom_bytes():
    cb = CustomBytes(b"aaa ")
    cbytes2 = cb.strip()
    assert cbytes2 == CustomBytes(b"aaa")
    cbytes2.extra_attrs["status"] = "Y"

    assert isinstance(cbytes2, CustomBytes)
    assert cbytes2 != CustomBytes(b"aaa")
    assert cbytes2.extra_attrs["status"] == "Y"


def test_custom_bytes_str():
    cs = CustomStr("aaa")
    cb = cs.encode()
    assert isinstance(cb, CustomBytes)
    assert isinstance(cb, bytes)
    assert not isinstance(cb, str)

    cs.extra_attrs["status"] = "Yes"
    assert cs.encode().extra_attrs["status"] == "Yes"

    cb2 = CustomBytes(b"bb")
    cb2.extra_attrs["status"] = "N"
    cs2 = cb2.decode()
    assert isinstance(cs2, str)
    assert isinstance(cs2, CustomStr)
    assert cs2.extra_attrs["status"] == "N", cs2.extra_attrs
