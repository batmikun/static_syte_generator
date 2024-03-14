import unittest

from nodes.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("<p>", "Text", None, {"styles": "color:#FFFFFF"})
        self.assertEqual(
            node.__repr__(),
            "Tag=<p>, Value=Text, Children=None, Props={'styles': 'color:#FFFFFF'}",
        )

    def test_repr_with_children(self):
        node = HTMLNode(
            "<p>",
            "Text",
            [HTMLNode("<a>", "Text", None, {"href": "https://google.com"})],
            {"styles": "color:#FFFFFF"},
        )
        self.assertEqual(
            node.__repr__(),
            "Tag=<p>, Value=Text, Children=[Tag=<a>, Value=Text, Children=None, Props={'href': 'https://google.com'}], Props={'styles': 'color:#FFFFFF'}",
        )

    def test_props_to_html(self):
        node = HTMLNode("<p>", "Text", None, {"styles": "color:#FFFFFF"})
        self.assertEqual(
            node.props_to_html(),
            " styles='color:#FFFFFF'",
        )


if __name__ == "__main__":
    unittest.main()

