# -*- coding: utf-8 -*-

import sys, unittest, os, decimal, datetime, gc, time, zlib, json
import cProfile, pstats
import EXASOL
from pprint import pprint as pp

PROFILE_OUTPUT = False
DB_URL = os.environ.get('DB_URL', "ws://localhost:8563")

class EXASOLTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ws = EXASOL.connect(DB_URL, 'sys', 'exasol', autocommit = True, useCompression = True)
        with self.ws.cursor() as c:
            try: c.execute('OPEN SCHEMA test')
            except: c.execute('CREATE SCHEMA test')

    @classmethod
    def tearDownClass(self):
        self.ws.close()
        self.ws = None

class EXASOLSpecialTests(EXASOLTest):
    def test_000_reconnect(self):
        with self.ws.cursor() as c:
            c.columnar_mode = True
            c.execute('''CREATE OR REPLACE PYTHON SCALAR SCRIPT sleep(seconds INT) RETURNS INT AS
import time
def run(c):
    start = time.time()
    time.sleep(c.seconds)
    return int(time.time() - start)    
''')
            c.execute('SELECT sleep(60)')
            print c.fetchall()

class EXASOLDataTypeTests(EXASOLTest):
    def test_000_int(self):


class EXASOLEngineDBTest(EXASOLTest):
    def test_000_open_schema(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = True
            self.assertEqual(c.execute('OPEN SCHEMA test'), 0)
            self.assertEqual(c.execute('SELECT * FROM cat'), 66)
            self.assertTrue(u'ENGINETABLE' in c.fetchall()[0])

    def test_001_fetchall_small(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = True
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > 0 AND INT_INDEX < 10 ORDER BY INT_INDEX'), 9)
            self.assertEqual(c.fetchall()[0], [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_002_fetchall_small_parameters(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = True
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > ? AND INT_INDEX < ? ORDER BY INT_INDEX', 0, 10), 9)
            self.assertEqual(c.fetchall()[0], [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_003_fetchall_big(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = True
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > 0 AND INT_INDEX < 4000 ORDER BY INT_INDEX'), 3999)
            intindex = c.fetchall()[0]
            self.assertEqual(intindex[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.assertEqual(intindex[-9:], [3991, 3992, 3993, 3994, 3995, 3996, 3997, 3998, 3999])

    def test_004_fetchall_big_parameters(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = True
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > ? AND INT_INDEX < ? ORDER BY INT_INDEX', 0, 4000), 3999)
            intindex = c.fetchall()[0]
            self.assertEqual(intindex[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.assertEqual(intindex[-9:], [3991, 3992, 3993, 3994, 3995, 3996, 3997, 3998, 3999])

    def test_005_fetchmany_small(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = True
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > 0 AND INT_INDEX < 10 ORDER BY INT_INDEX'), 9)
            self.assertEqual(c.fetchmany(size = 5)[0], [1, 2, 3, 4, 5])

    def test_006_fetchmany_small_parameters(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = True
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > ? AND INT_INDEX < ? ORDER BY INT_INDEX', 0, 10), 9)
            self.assertEqual(c.fetchmany(size = 5)[0], [1, 2, 3, 4, 5])

    def test_007_fetchmany_big(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = True
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > 0 AND INT_INDEX < 4000 ORDER BY INT_INDEX'), 3999)
            intindex = c.fetchmany(size = 2997)[0]
            self.assertEqual(intindex[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.assertEqual(intindex[-9:], [2989, 2990, 2991, 2992, 2993, 2994, 2995, 2996, 2997])

    def test_008_fetchmany_big_parameters(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = True
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > ? AND INT_INDEX < ? ORDER BY INT_INDEX', 0, 4000), 3999)
            intindex = c.fetchmany(size = 2997)[0]
            self.assertEqual(intindex[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.assertEqual(intindex[-9:], [2989, 2990, 2991, 2992, 2993, 2994, 2995, 2996, 2997])

    def test_009_fetchall_small_rows(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = False
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > 0 AND INT_INDEX < 10 ORDER BY INT_INDEX'), 9)
            data = c.fetchall()
            self.assertEqual(data[0], (1, u'42856.814', u'-26939.136', -5741, 14966, 8, -241360270, 4.827728e-28, 123.456, u'O', None, u'TEST                          ', u'z5uaaoai;HrakuxYr2;Zi.sp', u'LqZbuT0uC4vQ._6cG5uLpZdTZW;dfZ', u'1943-05-23', u'1982-11-01'))
            self.assertEqual(data[-1], (9, u'-0.001', u'-5.385', 4662, -4748, -770164835, 137587790, -802185.79, 23.855287999999998, u'o', u'046144224708798261336938866   ', u'0718052103665962291399302     ', u'ABCDE', u'PohjJC2DXjA9gxQv', u'1980-12-03', u'1972-04-18'))

    def test_010_fetchall_small_parametersl_rows(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = False
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > ? AND INT_INDEX < ? ORDER BY INT_INDEX', 0, 10), 9)
            data = c.fetchall()
            self.assertEqual(data[0], (1, u'42856.814', u'-26939.136', -5741, 14966, 8, -241360270, 4.827728e-28, 123.456, u'O', None, u'TEST                          ', u'z5uaaoai;HrakuxYr2;Zi.sp', u'LqZbuT0uC4vQ._6cG5uLpZdTZW;dfZ', u'1943-05-23', u'1982-11-01'))
            self.assertEqual(data[-1], (9, u'-0.001', u'-5.385', 4662, -4748, -770164835, 137587790, -802185.79, 23.855287999999998, u'o', u'046144224708798261336938866   ', u'0718052103665962291399302     ', u'ABCDE', u'PohjJC2DXjA9gxQv', u'1980-12-03', u'1972-04-18'))

    def test_011_fetchall_bigl_rows(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = False
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > 0 AND INT_INDEX < 4000 ORDER BY INT_INDEX'), 3999)
            intindex = c.fetchall()
            self.assertEqual(intindex[0][:9], (1, u'42856.814', u'-26939.136', -5741, 14966, 8, -241360270, 4.827728e-28, 123.456))
            self.assertEqual(intindex[0][-9:], (4.827728e-28, 123.456, u'O', None, u'TEST                          ', u'z5uaaoai;HrakuxYr2;Zi.sp', u'LqZbuT0uC4vQ._6cG5uLpZdTZW;dfZ', u'1943-05-23', u'1982-11-01'))
            self.assertEqual(intindex[-1][:9], (3999, u'1', u'41376.633', 4166, 5040, 781567016, -529930594, 1.4209716e-23, 8.953642e-34))
            self.assertEqual(intindex[-1][-9:], (1.4209716e-23, 8.953642e-34, u'D', u'77trU,p                       ', u'TEST                          ', u'PTJ_7lDlI9,v7hU3oUjSwuQwN', u'jQMIV2zFP;QkDxprL', u'1942-12-07', u'2000-06-05'))

    def test_012_fetchall_big_parametersl_rows(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = False
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > ? AND INT_INDEX < ? ORDER BY INT_INDEX', 0, 4000), 3999)
            intindex = c.fetchall()
            self.assertEqual(intindex[0][:9], (1, u'42856.814', u'-26939.136', -5741, 14966, 8, -241360270, 4.827728e-28, 123.456))
            self.assertEqual(intindex[0][-9:], (4.827728e-28, 123.456, u'O', None, u'TEST                          ', u'z5uaaoai;HrakuxYr2;Zi.sp', u'LqZbuT0uC4vQ._6cG5uLpZdTZW;dfZ', u'1943-05-23', u'1982-11-01'))
            self.assertEqual(intindex[-1][:9], (3999, u'1', u'41376.633', 4166, 5040, 781567016, -529930594, 1.4209716e-23, 8.953642e-34))
            self.assertEqual(intindex[-1][-9:], (1.4209716e-23, 8.953642e-34, u'D', u'77trU,p                       ', u'TEST                          ', u'PTJ_7lDlI9,v7hU3oUjSwuQwN', u'jQMIV2zFP;QkDxprL', u'1942-12-07', u'2000-06-05'))

    def test_013_fetchmany_smalll_rows(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = False
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > 0 AND INT_INDEX < 10 ORDER BY INT_INDEX'), 9)
            data = c.fetchmany(size = 5)
            self.assertEqual(len(data), 5)
            self.assertEqual(data[0], (1, u'42856.814', u'-26939.136', -5741, 14966, 8, -241360270, 4.827728e-28, 123.456, u'O', None, u'TEST                          ', u'z5uaaoai;HrakuxYr2;Zi.sp', u'LqZbuT0uC4vQ._6cG5uLpZdTZW;dfZ', u'1943-05-23', u'1982-11-01'))
            self.assertEqual(data[-1], (5, u'-44807.806', u'-8.752', 16146, -8, -826950668, None, -357886640000000, 4.810994e+20, u'j', u'pmsB9ayzLfESkw                ', u'br8,yshVLHklywIX9NWfh         ', u'TEST', u'TEST', u'1992-08-05', u'1949-07-12'))

    def test_014_fetchmany_small_parametersl_rows(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = False
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > ? AND INT_INDEX < ? ORDER BY INT_INDEX', 0, 10), 9)
            data = c.fetchmany(size = 5)
            self.assertEqual(len(data), 5)
            self.assertEqual(data[0], (1, u'42856.814', u'-26939.136', -5741, 14966, 8, -241360270, 4.827728e-28, 123.456, u'O', None, u'TEST                          ', u'z5uaaoai;HrakuxYr2;Zi.sp', u'LqZbuT0uC4vQ._6cG5uLpZdTZW;dfZ', u'1943-05-23', u'1982-11-01'))
            self.assertEqual(data[-1], (5, u'-44807.806', u'-8.752', 16146, -8, -826950668, None, -357886640000000, 4.810994e+20, u'j', u'pmsB9ayzLfESkw                ', u'br8,yshVLHklywIX9NWfh         ', u'TEST', u'TEST', u'1992-08-05', u'1949-07-12'))

    def test_015_fetchmany_bigl_rows(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = False
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > 0 AND INT_INDEX < 4000 ORDER BY INT_INDEX'), 3999)
            intindex = c.fetchmany(size = 2997)
            self.assertEqual(intindex[0][:9], (1, u'42856.814', u'-26939.136', -5741, 14966, 8, -241360270, 4.827728e-28, 123.456))
            self.assertEqual(intindex[0][-9:], (4.827728e-28, 123.456, u'O', None, u'TEST                          ', u'z5uaaoai;HrakuxYr2;Zi.sp', u'LqZbuT0uC4vQ._6cG5uLpZdTZW;dfZ', u'1943-05-23', u'1982-11-01'))
            self.assertEqual(intindex[-1][:9], (2997, u'24009.895', u'5.877', 15927, 6056, 241109333, -46335780, 0.017249234000000002, -0.7224116970000001))
            self.assertEqual(intindex[-1][-9:], (0.017249234000000002, -0.7224116970000001, u'q', u'ndNoPjisbFsiLFTjuD1p2ePYO     ', None, u'TEST', u'34491219476324761945', u'1975-08-09', u'1965-08-21'))

    def test_016_fetchmany_big_parametersl_rows(self):
        with self.ws.cursor() as c:
            self.ws.columnar_mode = False
            self.assertEqual(c.execute('SELECT * FROM ENGINETABLE WHERE INT_INDEX > ? AND INT_INDEX < ? ORDER BY INT_INDEX', 0, 4000), 3999)
            intindex = c.fetchmany(size = 2997)
            self.assertEqual(intindex[0][:9], (1, u'42856.814', u'-26939.136', -5741, 14966, 8, -241360270, 4.827728e-28, 123.456))
            self.assertEqual(intindex[0][-9:], (4.827728e-28, 123.456, u'O', None, u'TEST                          ', u'z5uaaoai;HrakuxYr2;Zi.sp', u'LqZbuT0uC4vQ._6cG5uLpZdTZW;dfZ', u'1943-05-23', u'1982-11-01'))
            self.assertEqual(intindex[-1][:9], (2997, u'24009.895', u'5.877', 15927, 6056, 241109333, -46335780, 0.017249234000000002, -0.7224116970000001))
            self.assertEqual(intindex[-1][-9:], (0.017249234000000002, -0.7224116970000001, u'q', u'ndNoPjisbFsiLFTjuD1p2ePYO     ', None, u'TEST', u'34491219476324761945', u'1975-08-09', u'1965-08-21'))


class EXASOLODBCTest(EXASOLTest):
    @classmethod
    def setUpClass(self):
        self.ws = EXASOL.connect(DB_URL, 'sys', 'exasol')
        self.ws.columnar_mode = False
        with self.ws.cursor() as c:
            c.execute('OPEN SCHEMA test')

        import pyodbc
        self.od = pyodbc.connect(DSN='LL')
        c = self.od.cursor()
        c.execute('OPEN SCHEMA test')

    @classmethod
    def tearDownClass(self):
        self.ws.close()
        self.ws = None
        self.od.close()
        self.od = None

    def setUp(self):
        if PROFILE_OUTPUT:
            self.pr = cProfile.Profile()
            self.pr.enable()

    def tearDown(self):
        if PROFILE_OUTPUT:
            self.pr.disable()
            p = pstats.Stats(self.pr)
            print("")
            p.strip_dirs().sort_stats('tottime').print_stats()

    @unittest.skip("disabled")
    def test_000_fetchall_vs_odbc(self):
        c = self.ws.cursor()
        c.execute('SELECT * FROM ENGINETABLE ORDER BY INT_INDEX')
        r1 = c.fetchall()

        c = self.od.cursor()
        c.execute('SELECT * FROM ENGINETABLE ORDER BY INT_INDEX')
        r2 = c.fetchall()

        for w, o in zip(r1, r2):
            for a, b in zip(w, o):
                if type(a) == type(1) and type(b) == type(1.0):
                    a = float(a)
                self.assertEqual(unicode(a), unicode(b))

    @unittest.skip("disabled")
    def test_001_fetchall_perf_vs_odbc(self):
        try:
            c0 = self.ws.cursor(); self.ws.columnar_mode = True
            c1 = self.ws.cursor(); self.ws.columnar_mode = False
            c2 = self.od.cursor()
            
            #query = 'SELECT FLOAT1, FLOAT2, CHAR1, CHAR2, VARCHAR01, VARCHAR02 FROM ENGINETABLEBIG1 WHERE INT_INDEX < 30000 ORDER BY INT_INDEX'
            query = 'SELECT * FROM ENGINETABLEBIG1 WHERE INT_INDEX < 30000 ORDER BY INT_INDEX'
            c0.execute(query); r0 = c0.fetchall(); c0.close(); self.ws.timersreset()

            r1 = r2 = None
            for n in range(5):
                del r1; del r2
                gc.collect(); gc.disable()
                with EXASOL.timer(self.ws, 'exws'): c1.execute(query)
                with EXASOL.timer(self.ws, 'fews'): r1 = c1.fetchall()
                with EXASOL.timer(self.ws, 'exod'): c2.execute(query)
                with EXASOL.timer(self.ws, 'feod'): r2 = c2.fetchall()
                gc.enable(); gc.collect()

            timers = self.ws.timers()
            if PROFILE_OUTPUT:
                print("")
                pp(self.ws.timers())
            self.assertTrue(timers['fews'][0] < timers['feod'][0])
            self.assertTrue(timers['fews'][1] < timers['feod'][1])

            if sys.version_info.major >= 3:
                conv = str
            else: conv = unicode
            for w, o in zip(r1, r2):
                for a, b in zip(w, o):
                    if type(a) == type(1) and type(b) == type(1.0):
                        a = float(a)
                    self.assertEqual(conv(a), conv(b))

        finally:
            gc.enable()

    def test_002_fetchall_perf(self):
        try:
            c1 = self.ws.cursor(); self.ws.columnar_mode = True
            query = 'SELECT * FROM ENGINETABLEBIG1 WHERE INT_INDEX < 200000 ORDER BY INT_INDEX'

            with EXASOL.timer(self.ws, 'exws'): c1.execute(query)
            with EXASOL.timer(self.ws, 'fews'): r1 = c1.fetchall()

            timers = self.ws.timers()
            if PROFILE_OUTPUT:
                print("")
                pp(self.ws.timers())

            self.assertTrue(timers['fews'][0] < 5)
            self.assertTrue(timers['fews'][1] < 1)

        finally:
            gc.enable()

    def test_003_fetch_perf(self):
        try:
            c1 = self.ws.cursor(); self.ws.columnar_mode = True
            query = 'SELECT * FROM ENGINETABLEBIG1'

            with EXASOL.timer(self.ws, 'exws'): c1.execute(query)
            while True:
                with EXASOL.timer(self.ws, 'fews'):
                    r1 = c1.fetchmany(size = 'optimal')
                if r1 is None: break

            timers = self.ws.timers()
            if PROFILE_OUTPUT:
                print("")
                pp(self.ws.timers())

            self.assertTrue(timers['fews'][0] < 35)
            self.assertTrue(timers['fews'][1] < 3)

        finally:
            gc.enable()
        

if __name__ == '__main__':
    unittest.main()
