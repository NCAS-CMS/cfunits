import faulthandler
import math
import os
import unittest

import numpy

faulthandler.enable()  # to debug seg faults and timeouts

import cfunits
from cfunits import Units


class UnitsTest(unittest.TestCase):
    """Tests the `Units` class."""

    def test_Units___eq__(self):
        """Tests the `___eq__` operator on `Units`."""
        self.assertEqual(Units(""), Units(""))
        self.assertEqual(Units("18"), Units("18"))
        self.assertEqual(Units("1"), Units("1"))
        self.assertEqual(Units("m"), Units("m"))
        self.assertEqual(Units("m"), Units("metres"))
        self.assertEqual(Units("m"), Units("meTRES"))

        self.assertEqual(
            Units("days since 2000-1-1"), Units("d since 2000-1-1 0:0")
        )
        self.assertNotEqual(
            Units("days since 2000-1-1"), Units("h since 1234-1-1 0:0")
        )

        self.assertEqual(
            Units("days since 2000-1-1"),
            Units("d since 2000-1-1 0:0", calendar="gregorian"),
        )
        self.assertEqual(
            Units("days since 2000-1-1"),
            Units("d since 2000-1-1 0:0", calendar="standard"),
        )

        self.assertEqual(Units(calendar="noleap"), Units(calendar="noleap"))
        self.assertEqual(Units(calendar="noleap"), Units(calendar="365_day"))
        self.assertEqual(Units(calendar="nOLEAP"), Units(calendar="365_dAY"))

        self.assertEqual(
            Units("days since 2000-1-1", calendar="all_leap"),
            Units("d since 2000-1-1 0:0", calendar="366_day"),
        )
        self.assertNotEqual(
            Units("days since 2000-1-1", calendar="all_leap"),
            Units("h since 2000-1-1 0:0", calendar="366_day"),
        )

        self.assertNotEqual(Units(1), Units(1))
        self.assertNotEqual(Units(1), Units(2))
        self.assertNotEqual(Units(1), Units())
        self.assertNotEqual(Units(1), Units(""))
        self.assertNotEqual(Units(1), Units(" "))
        self.assertNotEqual(Units(1), Units("metre"))

    def test_Units_equivalent(self):
        """Tests the `equivalent` method on `Units`."""
        self.assertTrue(Units().equivalent(Units()))
        self.assertTrue(Units(" ").equivalent(Units()))
        self.assertTrue(Units("").equivalent(Units()))
        self.assertTrue(Units().equivalent(Units("")))
        self.assertTrue(Units().equivalent(Units(" ")))
        self.assertTrue(Units("").equivalent(Units("")))
        self.assertTrue(Units("").equivalent(Units(" ")))
        self.assertTrue(Units("").equivalent(Units("1")))
        self.assertTrue(Units("").equivalent(Units("18")))
        self.assertTrue(Units("18").equivalent(Units("1")))
        self.assertTrue(Units("18").equivalent(Units("18")))
        self.assertTrue(Units("1)").equivalent(Units("1")))

        self.assertTrue(Units("m").equivalent(Units("m")))
        self.assertTrue(Units("meter").equivalent(Units("km")))
        self.assertTrue(Units("metre").equivalent(Units("mile")))

        self.assertTrue(Units("s").equivalent(Units("h")))
        self.assertTrue(Units("s").equivalent(Units("day")))
        self.assertTrue(Units("second").equivalent(Units("month")))

        self.assertTrue(
            Units(calendar="noleap").equivalent(Units(calendar="noleap"))
        )
        self.assertTrue(
            Units(calendar="noleap").equivalent(Units(calendar="365_day"))
        )
        self.assertTrue(
            Units(calendar="nOLEAP").equivalent(Units(calendar="365_dAY"))
        )

        self.assertTrue(
            Units("days since 2000-1-1").equivalent(
                Units("d since 2000-1-1 0:0")
            )
        )
        self.assertTrue(
            Units("days since 2000-1-1").equivalent(
                Units("h since 1234-1-1 0:0")
            )
        )
        self.assertTrue(
            Units("days since 2000-1-1").equivalent(
                Units("d since 2000-1-1 0:0", calendar="gregorian")
            )
        )
        self.assertTrue(
            Units("days since 2000-1-1").equivalent(
                Units("h since 1234-1-1 0:0", calendar="standard")
            )
        )

        self.assertTrue(
            Units("days since 2000-1-1", calendar="all_leap").equivalent(
                Units("d since 2000-1-1 0:0", calendar="366_day")
            )
        )
        self.assertTrue(
            Units("days since 2000-1-1", calendar="all_leap").equivalent(
                Units("h since 1234-1-1 0:0", calendar="366_day")
            )
        )

        u = Units("days since 2000-02-02", calendar="standard")
        v = Units("months since 2000-02-02", calendar="standard")
        self.assertNotEqual(u, v)

        u = Units("days since 2000-02-02", calendar="standard")
        v = Units("months since 2000-02-02", calendar="gregorian")
        self.assertNotEqual(u, v)

        self.assertFalse(Units(1).equivalent(Units(1)))
        self.assertFalse(Units().equivalent(Units(1)))
        self.assertFalse(Units(2).equivalent(Units(1)))
        self.assertFalse(Units("").equivalent(Units(1)))
        self.assertFalse(Units(" ").equivalent(Units(1)))
        self.assertFalse(Units("1").equivalent(Units(1)))

    def test_Units_conform(self):
        """Tests the `conform` class method on `Units`."""
        self.assertEqual(Units.conform(0.5, Units("km"), Units("m")), 500)

        self.assertEqual(
            Units.conform(360, Units("second"), Units("minute")), 6
        )

        x = Units.conform([360], Units("second"), Units("minute"))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertTrue(numpy.allclose(x, 6))

        x = Units.conform((360, 720), Units("second"), Units("minute"))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertTrue(numpy.allclose(x, [6, 12]))

        x = Units.conform([360.0, 720.0], Units("second"), Units("minute"))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertTrue(numpy.allclose(x, [6, 12]))

        x = Units.conform([[360, 720]], Units("second"), Units("minute"))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertTrue(numpy.allclose(x, [[6, 12]]))

        v = numpy.array([360.0, 720.0], dtype=numpy.dtype("float64"))
        x = Units.conform(v, Units("second"), Units("minute"))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype("float64"))
        self.assertTrue(numpy.allclose(x, [6, 12]), x)

        v = numpy.array([360, 720], dtype=numpy.dtype("int64"))
        x = Units.conform(v, Units("second"), Units("minute"), inplace=True)
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype("float64"))
        self.assertTrue(numpy.allclose(x, [6, 12]))
        self.assertTrue(numpy.allclose(x, v))

        v = numpy.array([360, 720], dtype=numpy.dtype("int32"))
        x = Units.conform(v, Units("second"), Units("minute"), inplace=True)
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype("float32"))
        self.assertTrue(numpy.allclose(x, [6, 12]))
        self.assertTrue(numpy.allclose(x, v))

        for i in range(24):
            v = numpy.array([], dtype=numpy.sctypeDict[i])
            if v.dtype.kind == "i":
                v = numpy.array([60, 120], dtype=numpy.sctypeDict[i])
                check_dtype = v.dtype.str
                x = Units.conform(
                    v, Units("second"), Units("minute"), inplace=True
                )
                self.assertIsInstance(x, numpy.ndarray)
                if check_dtype[-1] in ["1", "2"]:
                    # no inplace converting possible
                    self.assertEqual(x.dtype.itemsize, 4)
                else:
                    self.assertEqual(x.dtype.str, v.dtype.str)
                    self.assertTrue(numpy.allclose(x, v))
                self.assertTrue(numpy.allclose(x, [1, 2]))

        x = Units.conform(35, Units("degrees_C"), Units("degrees_F"))
        self.assertIsInstance(x, float)
        self.assertTrue(numpy.allclose(x, 95))

        x = Units.conform([35], Units("degrees_C"), Units("degrees_F"))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertTrue(numpy.allclose(x, 95))

        x = Units.conform(
            35, Units("degrees_C"), Units("degrees_F"), inplace=True
        )
        self.assertIsInstance(x, float)
        self.assertTrue(numpy.allclose(x, 95))

        x = Units.conform(
            [35], Units("degrees_C"), Units("degrees_F"), inplace=True
        )
        self.assertIsInstance(x, numpy.ndarray)
        self.assertTrue(numpy.allclose(x, 95))

        with self.assertRaises(ValueError):
            Units.conform(1, Units("m"), Units("second"))

    def test_Units_BINARY_AND_UNARY_OPERATORS(self):
        """Tests use of binary and unary operators on `Units`."""
        self.assertEqual(Units("m") * 2, Units("2m"))
        self.assertEqual(Units("m") / 2, Units("0.5m"))
        self.assertEqual(Units("m") // 2, Units("0.5m"))
        self.assertEqual(Units("m") + 2, Units("m @ -2"))
        self.assertEqual(Units("m") - 2, Units("m @ 2"))
        self.assertEqual(Units("m") ** 2, Units("m2"))
        self.assertEqual(Units("m") ** -2, Units("m-2"))
        self.assertEqual(Units("m2") ** 0.5, Units("m"))

        u = Units("m")
        v = u
        u *= 2
        self.assertEqual(u, Units("2m"))
        self.assertNotEqual(u, v)
        u = Units("m")
        v = u
        u /= 2
        self.assertEqual(u, Units("0.5m"))
        self.assertNotEqual(u, v)
        u = Units("m")
        v = u
        u //= 2
        self.assertEqual(u, Units("0.5m"))
        self.assertNotEqual(u, v)
        u = Units("m")
        v = u
        u += 2
        self.assertEqual(u, Units("m @ -2"))
        self.assertNotEqual(u, v)
        u = Units("m")
        v = u
        u -= 2
        self.assertEqual(u, Units("m @ 2"))
        self.assertNotEqual(u, v)
        u = Units("m")
        v = u
        u **= 2
        self.assertEqual(u, Units("m2"))
        self.assertNotEqual(u, v)

        self.assertEqual(2 * Units("m"), Units("2m"))
        self.assertEqual(2 / Units("m"), Units("2 m-1"))
        self.assertEqual(2 // Units("m"), Units("2 m-1"))
        self.assertEqual(2 + Units("m"), Units("m @ -2"))
        self.assertEqual(2 - Units("m"), Units("-1 m @ -2"))

        self.assertEqual(Units("m") * Units("2m"), Units("2 m2"))
        self.assertEqual(Units("m") / Units("2m"), Units("0.5"))
        self.assertEqual(Units("m") // Units("2m"), Units("0.5"))

        u = Units("m")
        v = u
        u *= u
        self.assertEqual(u, Units("m2"))
        self.assertNotEqual(u, v)
        u = Units("m")
        v = u
        u /= u
        self.assertEqual(u, Units("1"))
        self.assertNotEqual(u, v)
        u = Units("m")
        v = u
        u //= u
        self.assertEqual(u, Units("1"))
        self.assertNotEqual(u, v)

        self.assertEqual(Units("m").log(10), Units("lg(re 1 m)"))
        self.assertEqual(Units("m").log(2), Units("lb(re 1 m)"))
        self.assertEqual(Units("m").log(math.e), Units("ln(re 1 m)"))
        self.assertEqual(
            Units("m").log(1.5), Units("2.46630346237643 ln(re 1 m)")
        )

    def test_Units_isvalid(self):
        """Tests the `isvalid` property on `Units`."""
        self.assertTrue(Units("m").isvalid)
        self.assertTrue(Units("days since 2019-01-01").isvalid)
        self.assertTrue(
            Units("days since 2019-01-01", calendar="360_day").isvalid
        )

        self.assertFalse(Units("qwerty").isvalid)
        self.assertFalse(Units(1.0).isvalid)
        self.assertFalse(Units([1.0, "qwerty"]).isvalid)
        self.assertFalse(Units("since 2019-01-01").isvalid)
        self.assertFalse(
            Units("days since 2019-01-01", calendar="qwerty").isvalid
        )
        self.assertFalse(Units("since 2019-01-01", calendar="qwerty").isvalid)

    def test_Units_has_offset(self):
        """Tests the `has_offset` property on `Units`."""
        self.assertFalse(Units("K").has_offset)
        self.assertFalse(Units("K @ 0").has_offset)
        self.assertFalse(Units("Watt").has_offset)
        self.assertFalse(Units("m2.kg.s-3").has_offset)
        self.assertFalse(Units("km").has_offset)
        self.assertFalse(Units("1000 m").has_offset)
        self.assertFalse(Units("(K @ 273.15) m s-1").has_offset)
        self.assertFalse(Units("degC m s-1").has_offset)

        self.assertTrue(Units("K @ 273.15").has_offset)
        self.assertTrue(Units("degC").has_offset)
        self.assertTrue(Units("degF").has_offset)
        self.assertTrue(Units("m2.kg.s-3 @ 3.14").has_offset)

        self.assertEqual(Units("degC m s-1"), Units("K m s-1"))

    def test_Units__hash__(self):
        """Tests the hash value generated by `__hash__` on `Units`."""
        self.assertIsInstance(hash(Units("K")), int)
        self.assertIsInstance(hash(Units("")), int)
        self.assertIsInstance(hash(Units()), int)
        self.assertIsInstance(hash(Units("days since 2000-01-01")), int)
        self.assertIsInstance(
            hash(Units("days since 2000-01-01", calendar="360_day")), int
        )

    def test_Units_formatted(self):
        """Tests the `formatted` method on `Units`."""
        u = Units("W")
        self.assertEqual(u.units, "W")
        self.assertEqual(u.formatted(names=True), "watt")
        self.assertEqual(u.formatted(definition=True), "m2.kg.s-3")
        self.assertEqual(
            u.formatted(names=True, definition=True),
            "meter^2-kilogram-second^-3",
        )
        self.assertEqual(u.formatted(), "W")

        u = Units("tsp")
        self.assertEqual(u.formatted(names=True), "4.928921875e-06 meter^3")
        u = Units("tsp", names=True)
        self.assertEqual(u.units, "4.928921875e-06 meter^3")

        u = Units("m/s", formatted=True)
        self.assertEqual(u.units, "m.s-1")

        u = Units("Watt", formatted=True)
        self.assertEqual(u.units, "W")
        u = Units("Watt", names=True)
        self.assertEqual(u.units, "watt")
        u = Units("Watt", definition=True)
        self.assertEqual(u.units, "m2.kg.s-3")
        u = Units("Watt", names=True, definition=True)
        self.assertEqual(u.units, "meter^2-kilogram-second^-3")

        u = Units("days since 1900-1-1 03:05", names=True)
        self.assertEqual(u.units, "day since 1900-01-01 03:05:00")
        u = Units("days since 1900-1-1 03:05", formatted=True)
        self.assertEqual(u.units, "d since 1900-01-01 03:05:00")
        u = Units("days since 1900-1-1 03:05")
        self.assertEqual(u.formatted(), "d since 1900-01-01 03:05:00")

        u = Units("hours since 2100-1-1", calendar="noleap", names=True)
        self.assertEqual(u.units, "hour since 2100-01-01 00:00:00")
        u = Units("hours since 2100-1-1", calendar="noleap", formatted=True)
        self.assertEqual(u.units, "h since 2100-01-01 00:00:00")
        u = Units("hours since 2100-1-1", calendar="noleap")
        self.assertEqual(u.formatted(), "h since 2100-01-01 00:00:00")


# --- End: class


if __name__ == "__main__":
    print("cfunits version:", cfunits.__version__)
    print("cfunits path:", os.path.abspath(cfunits.__file__))
    print("")
    unittest.main(verbosity=2)
