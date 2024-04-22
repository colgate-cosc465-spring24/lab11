import dash_client
import time
import unittest

class TestFetch(unittest.TestCase):
    def test_fetch_content(self):
        data = dash_client.fetch("http://riker.cs.colgate.edu/dash/bbb_", "test", 13, 500)
        self.assertEqual(data, b"This is a test.\n")
    
    def test_fetch_404(self):
        data = dash_client.fetch("http://riker.cs.colgate.edu/dash/bbb_", "test", 99, 500)
        self.assertEqual(data, None)

    def test_fetch_delay(self):
        start = time.time()
        data = dash_client.fetch("http://riker.cs.colgate.edu/dash/bbb_", "test", 250, 1)
        end = time.time()
        self.assertGreaterEqual(end - start, 2)

if __name__ == '__main__':
    unittest.main()
