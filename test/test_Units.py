import cfunits as cf
import math
import os
import unittest

class UnitsTest(unittest.TestCase):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'test_file.nc')
    chunk_sizes = (17, 34, 300, 100000)[::-1]

    def test_Units___eq__(self):
        self.assertTrue(cf.Units('')==cf.Units(''))
        self.assertTrue(cf.Units('18')==cf.Units('18'))
        self.assertTrue(cf.Units('1')==cf.Units('1'))
        self.assertTrue(cf.Units('m')==cf.Units('m'))
        self.assertTrue(cf.Units('m')==cf.Units('metres'))
        self.assertTrue(cf.Units('m')==cf.Units('meTRES'))

        self.assertTrue(cf.Units('days since 2000-1-1')==cf.Units('d since 2000-1-1 0:0'))
        self.assertTrue(cf.Units('days since 2000-1-1')!=cf.Units('h since 1234-1-1 0:0'))
        
        self.assertTrue(cf.Units('days since 2000-1-1')==cf.Units('d since 2000-1-1 0:0', calendar='gregorian'))
        self.assertTrue(cf.Units('days since 2000-1-1')==cf.Units('d since 2000-1-1 0:0', calendar='standard'))
        
        self.assertTrue(cf.Units(calendar='noleap')==cf.Units(calendar='noleap'))
        self.assertTrue(cf.Units(calendar='noleap')==cf.Units(calendar='365_day'))
        self.assertTrue(cf.Units(calendar='nOLEAP')==cf.Units(calendar='365_dAY'))
        
        self.assertTrue(cf.Units('days since 2000-1-1', calendar='all_leap')==cf.Units('d since 2000-1-1 0:0', calendar='366_day'))
        self.assertTrue(cf.Units('days since 2000-1-1', calendar='all_leap')!=cf.Units('h since 2000-1-1 0:0', calendar='366_day'))    
    #--- End: def
        
    def test_Units_equivalent(self):
        self.assertTrue(cf.Units('').equivalent(cf.Units('')))
        self.assertTrue(cf.Units('').equivalent(cf.Units('1')))
        self.assertTrue(cf.Units('').equivalent(cf.Units('18')))
        self.assertTrue(cf.Units('18').equivalent(cf.Units('1')))
        self.assertTrue(cf.Units('18').equivalent(cf.Units('18')))
        self.assertTrue(cf.Units('1)').equivalent(cf.Units('1')))

        self.assertTrue(cf.Units('m').equivalent(cf.Units('m')))
        self.assertTrue(cf.Units('meter').equivalent(cf.Units('km')))
        self.assertTrue(cf.Units('metre').equivalent(cf.Units('mile')))

        self.assertTrue(cf.Units('s').equivalent(cf.Units('h')))
        self.assertTrue(cf.Units('s').equivalent(cf.Units('day')))
        self.assertTrue(cf.Units('second').equivalent(cf.Units('month')) )   

        self.assertTrue(cf.Units(calendar='noleap').equivalent(cf.Units(calendar='noleap')))
        self.assertTrue(cf.Units(calendar='noleap').equivalent(cf.Units(calendar='365_day')))
        self.assertTrue(cf.Units(calendar='nOLEAP').equivalent(cf.Units(calendar='365_dAY')))

        self.assertTrue(cf.Units('days since 2000-1-1').equivalent(cf.Units('d since 2000-1-1 0:0')))
        self.assertTrue(cf.Units('days since 2000-1-1').equivalent(cf.Units('h since 1234-1-1 0:0')))
        self.assertTrue(cf.Units('days since 2000-1-1').equivalent(cf.Units('d since 2000-1-1 0:0', calendar='gregorian')))
        self.assertTrue(cf.Units('days since 2000-1-1').equivalent(cf.Units('h since 1234-1-1 0:0', calendar='standard')))

        self.assertTrue(cf.Units('days since 2000-1-1', calendar='all_leap').equivalent(cf.Units('d since 2000-1-1 0:0', calendar='366_day')))
        self.assertTrue(cf.Units('days since 2000-1-1', calendar='all_leap').equivalent(cf.Units('h since 1234-1-1 0:0', calendar='366_day')))    
    #--- End: def 

    def test_Units_BINARY_AND_UNARY_OPERATORS(self):
        self.assertTrue((cf.Units('m')*2)    ==cf.Units('2m'))
        self.assertTrue((cf.Units('m')/2)    ==cf.Units('0.5m'))
        self.assertTrue((cf.Units('m')//2)   ==cf.Units('0.5m'))
        self.assertTrue((cf.Units('m')+2)    ==cf.Units('m @ -2'))
        self.assertTrue((cf.Units('m')-2)    ==cf.Units('m @ 2'))
        self.assertTrue((cf.Units('m')**2)   ==cf.Units('m2'))
        self.assertTrue((cf.Units('m')**-2)  ==cf.Units('m-2'))
        self.assertTrue((cf.Units('m2')**0.5)==cf.Units('m'))
    
        u = cf.Units('m')
        v = u
        u *= 2
        self.assertTrue(u==cf.Units('2m'))
        self.assertTrue(u!=v)
        u = cf.Units('m')
        v = u
        u /= 2
        self.assertTrue(u==cf.Units('0.5m'))
        self.assertTrue(u!=v)
        u = cf.Units('m')
        v = u
        u //= 2
        self.assertTrue(u==cf.Units('0.5m'))
        self.assertTrue(u!=v)
        u = cf.Units('m')
        v = u
        u += 2
        self.assertTrue(u==cf.Units('m @ -2'))
        self.assertTrue(u!=v)
        u = cf.Units('m')
        v = u
        u -= 2
        self.assertTrue(u==cf.Units('m @ 2'))
        self.assertTrue(u!=v)
        u = cf.Units('m')
        v = u
        u **= 2
        self.assertTrue(u==cf.Units('m2'))
        self.assertTrue(u!=v)
    
        self.assertTrue((2*cf.Units('m')) ==cf.Units('2m'))
        self.assertTrue((2/cf.Units('m')) ==cf.Units('2 m-1'))
        self.assertTrue((2//cf.Units('m'))==cf.Units('2 m-1'))
        self.assertTrue((2+cf.Units('m')) ==cf.Units('m @ -2'))
        self.assertTrue((2-cf.Units('m')) ==cf.Units('-1 m @ -2'))
    
        self.assertTrue((cf.Units('m')*cf.Units('2m')) ==cf.Units('2 m2'))
        self.assertTrue((cf.Units('m')/cf.Units('2m')) ==cf.Units('0.5'))
        self.assertTrue((cf.Units('m')//cf.Units('2m'))==cf.Units('0.5'))
    
        u = cf.Units('m')
        v = u
        u *= u
        self.assertTrue(u==cf.Units('m2'))
        self.assertTrue(u!=v)
        u = cf.Units('m')
        v = u
        u /= u
        self.assertTrue(u==cf.Units('1'))
        self.assertTrue(u!=v)
        u = cf.Units('m')
        v = u
        u //= u
        self.assertTrue(u==cf.Units('1'))
        self.assertTrue(u!=v)
    
        self.assertTrue(cf.Units('m').log(10)    ==cf.Units('lg(re 1 m)'))
        self.assertTrue(cf.Units('m').log(2)     ==cf.Units('lb(re 1 m)'))
        self.assertTrue(cf.Units('m').log(math.e)==cf.Units('ln(re 1 m)'))
        self.assertTrue(cf.Units('m').log(1.5)   ==cf.Units('2.46630346237643 ln(re 1 m)'))    
    #--- End: def

#--- End: class

if __name__ == '__main__':
    print 'cfunits-python version:', cf.__version__
    print 'cfunits-python path:'   , os.path.abspath(cf.__file__)
    print ''
    unittest.main(verbosity=2)

