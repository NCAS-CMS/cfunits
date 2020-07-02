import math
import os
import unittest

import numpy

import cfunits
from cfunits import Units


class UnitsTest(unittest.TestCase):
    def test_Units___eq__(self):
        self.assertEqual(Units(''), Units(''))
        self.assertEqual(Units('18'), Units('18'))
        self.assertEqual(Units('1'), Units('1'))
        self.assertEqual(Units('m'), Units('m'))
        self.assertEqual(Units('m'), Units('metres'))
        self.assertEqual(Units('m'), Units('meTRES'))

        self.assertEqual(Units('days since 2000-1-1'),
                         Units('d since 2000-1-1 0:0'))
        self.assertNotEqual(Units('days since 2000-1-1'),
                            Units('h since 1234-1-1 0:0'))
        
        self.assertEqual(Units('days since 2000-1-1'),
                         Units('d since 2000-1-1 0:0', calendar='gregorian'))
        self.assertEqual(Units('days since 2000-1-1'),
                         Units('d since 2000-1-1 0:0', calendar='standard'))
        
        self.assertEqual(Units(calendar='noleap'), Units(calendar='noleap'))
        self.assertEqual(Units(calendar='noleap'), Units(calendar='365_day'))
        self.assertEqual(Units(calendar='nOLEAP'), Units(calendar='365_dAY'))
        
        self.assertEqual(Units('days since 2000-1-1', calendar='all_leap'),
                         Units('d since 2000-1-1 0:0', calendar='366_day'))
        self.assertNotEqual(Units('days since 2000-1-1', calendar='all_leap'),
                            Units('h since 2000-1-1 0:0', calendar='366_day'))
        
    def test_Units_equivalent(self):
        self.assertTrue(Units('').equivalent(Units('')))
        self.assertTrue(Units('').equivalent(Units('1')))
        self.assertTrue(Units('').equivalent(Units('18')))
        self.assertTrue(Units('18').equivalent(Units('1')))
        self.assertTrue(Units('18').equivalent(Units('18')))
        self.assertTrue(Units('1)').equivalent(Units('1')))

        self.assertTrue(Units('m').equivalent(Units('m')))
        self.assertTrue(Units('meter').equivalent(Units('km')))
        self.assertTrue(Units('metre').equivalent(Units('mile')))

        self.assertTrue(Units('s').equivalent(Units('h')))
        self.assertTrue(Units('s').equivalent(Units('day')))
        self.assertTrue(Units('second').equivalent(Units('month')) )   

        self.assertTrue(Units(calendar='noleap').equivalent(Units(calendar='noleap')))
        self.assertTrue(Units(calendar='noleap').equivalent(Units(calendar='365_day')))
        self.assertTrue(Units(calendar='nOLEAP').equivalent(Units(calendar='365_dAY')))

        self.assertTrue(Units('days since 2000-1-1').equivalent(Units('d since 2000-1-1 0:0')))
        self.assertTrue(Units('days since 2000-1-1').equivalent(Units('h since 1234-1-1 0:0')))
        self.assertTrue(Units('days since 2000-1-1').equivalent(Units('d since 2000-1-1 0:0', calendar='gregorian')))
        self.assertTrue(Units('days since 2000-1-1').equivalent(Units('h since 1234-1-1 0:0', calendar='standard')))

        self.assertTrue(Units('days since 2000-1-1', calendar='all_leap').equivalent(Units('d since 2000-1-1 0:0', calendar='366_day')))
        self.assertTrue(Units('days since 2000-1-1', calendar='all_leap').equivalent(Units('h since 1234-1-1 0:0', calendar='366_day')))    

        u = Units('days since 2000-02-02', calendar='standard')
        v = Units('months since 2000-02-02', calendar='standard')
        self.assertNotEqual(u, v)

        u = Units('days since 2000-02-02', calendar='standard')
        v = Units('months since 2000-02-02', calendar='gregorian')
        self.assertNotEqual(u, v)

    def test_Units_conform(self):
        self.assertEqual(Units.conform(0.5, Units('km'), Units('m')), 500)
        
        self.assertEqual(
            Units.conform(360, Units('second'), Units('minute')), 6)

        x = Units.conform([360], Units('second'), Units('minute'))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype('float64'))
        self.assertTrue(numpy.allclose(x, 6))
        
        x = Units.conform((360, 720), Units('second'), Units('minute'))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype('float64'))
        self.assertTrue(numpy.allclose(x, [6, 12]))
        
        x = Units.conform([360.0, 720.0], Units('second'), Units('minute'))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype('float64'))
        self.assertTrue(numpy.allclose(x, [6, 12]))
        
        x = Units.conform([[360, 720]], Units('second'), Units('minute'))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype('float64'))
        self.assertTrue(numpy.allclose(x, [[6, 12]]))

        v = numpy.array([360.0, 720.0])
        x = Units.conform(v, Units('second'), Units('minute'))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype('float64'))
        self.assertTrue(numpy.allclose(x, [6, 12]), x)
        
        v = numpy.array([360, 720])
        x = Units.conform(v, Units('second'), Units('minute'), inplace=True)
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype('float64'))
        self.assertTrue(numpy.allclose(x, [6, 12]))
        self.assertTrue(numpy.allclose(x, v))    
        
        x = Units.conform(35, Units('degrees_C'), Units('degrees_F'))
        self.assertIsInstance(x, float)
        self.assertTrue(numpy.allclose(x, 95))
        
        x = Units.conform([35], Units('degrees_C'), Units('degrees_F'))
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype('float64'))
        self.assertTrue(numpy.allclose(x, 95))
        
        x = Units.conform(35, Units('degrees_C'), Units('degrees_F'),
                          inplace=True)
        self.assertIsInstance(x, float)
        self.assertTrue(numpy.allclose(x, 95))
        
        x = Units.conform([35], Units('degrees_C'), Units('degrees_F'),
                          inplace=True)
        self.assertIsInstance(x, numpy.ndarray)
        self.assertEqual(x.dtype, numpy.dtype('float64'))
        self.assertTrue(numpy.allclose(x, 95))
        
        with self.assertRaises(ValueError):
            Units.conform(1, Units('m'), Units('second'))

    def test_Units_BINARY_AND_UNARY_OPERATORS(self):
        self.assertEqual(Units('m') * 2, Units('2m'))
        self.assertEqual(Units('m') / 2, Units('0.5m'))
        self.assertEqual(Units('m') // 2, Units('0.5m'))
        self.assertEqual(Units('m') + 2, Units('m @ -2'))
        self.assertEqual(Units('m') - 2, Units('m @ 2'))
        self.assertEqual(Units('m') ** 2, Units('m2'))
        self.assertEqual(Units('m') ** -2, Units('m-2'))
        self.assertEqual(Units('m2') ** 0.5, Units('m'))
    
        u = Units('m')
        v = u
        u *= 2
        self.assertEqual(u, Units('2m'))
        self.assertNotEqual(u, v)
        u = Units('m')
        v = u
        u /= 2
        self.assertEqual(u, Units('0.5m'))
        self.assertNotEqual(u, v)
        u = Units('m')
        v = u
        u //= 2
        self.assertEqual(u, Units('0.5m'))
        self.assertNotEqual(u, v)
        u = Units('m')
        v = u
        u += 2
        self.assertEqual(u, Units('m @ -2'))
        self.assertNotEqual(u, v)
        u = Units('m')
        v = u
        u -= 2
        self.assertEqual(u, Units('m @ 2'))
        self.assertNotEqual(u, v)
        u = Units('m')
        v = u
        u **= 2
        self.assertEqual(u, Units('m2'))
        self.assertNotEqual(u, v)
    
        self.assertEqual(2 * Units('m'), Units('2m'))
        self.assertEqual(2 / Units('m'), Units('2 m-1'))
        self.assertEqual(2 // Units('m'),Units('2 m-1'))
        self.assertEqual(2 + Units('m'), Units('m @ -2'))
        self.assertEqual(2 - Units('m'), Units('-1 m @ -2'))
    
        self.assertEqual(Units('m') * Units('2m'), Units('2 m2'))
        self.assertEqual(Units('m') / Units('2m'), Units('0.5'))
        self.assertEqual(Units('m') // Units('2m'), Units('0.5'))
    
        u = Units('m')
        v = u
        u *= u
        self.assertEqual(u, Units('m2'))
        self.assertNotEqual(u, v)
        u = Units('m')
        v = u
        u /= u
        self.assertEqual(u, Units('1'))
        self.assertNotEqual(u, v)
        u = Units('m')
        v = u
        u //= u
        self.assertEqual(u, Units('1'))
        self.assertNotEqual(u, v)
    
        self.assertEqual(Units('m').log(10), Units('lg(re 1 m)'))
        self.assertEqual(Units('m').log(2), Units('lb(re 1 m)'))
        self.assertEqual(Units('m').log(math.e), Units('ln(re 1 m)'))
        self.assertEqual(Units('m').log(1.5),
                         Units('2.46630346237643 ln(re 1 m)'))    

    def test_Units_isvalid(self):
        self.assertTrue(Units('m').isvalid)
        self.assertTrue(Units('days since 2019-01-01').isvalid)
        self.assertTrue(
            Units('days since 2019-01-01', calendar='360_day').isvalid)

        self.assertFalse(Units('qwerty').isvalid)
        self.assertFalse(Units(1.0).isvalid)
        self.assertFalse(Units([1.0, 'qwerty']).isvalid)
        self.assertFalse(Units('since 2019-01-01').isvalid)
        self.assertFalse(
            Units('days since 2019-01-01', calendar='qwerty').isvalid)
        self.assertFalse(
            Units('since 2019-01-01', calendar='qwerty').isvalid)

# --- End: class

        
if __name__ == '__main__':
    print('cfunits version:', cfunits.__version__)
    print('cfunits path:'   , os.path.abspath(cfunits.__file__))
    print('')
    unittest.main(verbosity=2)

