import unittest

class ToolsTestCase(unittest.TestCase):

    def test_get_domain_name(self):
        from .tools import get_domain_name
        cases = [('https://example.com/tags', 'example.com'), 
                ( 'mysite.org', 'mysite.org')]
        for url, domain in cases:
            self.assertEqual( get_domain_name(url), domain)

    def test_get_protocol(self):
        from .tools import get_protocol
        url = "https://example.com"
        self.assertEqual('https:', get_protocol(url))

    def test_get_base_url(self):
        from .tools import get_base_url
        url = "https://example.com/page/other"
        self.assertEqual("https://example.com", 
                            get_base_url(url))

    def test_drop_comments_and_fragments(self):
        from .tools import drop_comments_and_fragments
        url="https://example.com/page/?thing=2"
        self.assertEqual(drop_comments_and_fragments(url), "https://example.com/page/")

if __name__ == "__main__":
    unittest.main()
