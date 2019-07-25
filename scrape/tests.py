import unittest

class ToolsTestCase(unittest.TestCase):

    def test_get_domain_name(self):
        from .tools import get_domain_name
        cases = [('https://example.com/tags', 'example.com'), 
                ( 'mysite.org', 'mysite.org')]
        for url, domain in cases:
            self.assertEqual( get_domain_name(url), domain)

if __name__ == "__main__":
    unittest.main()