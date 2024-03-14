import unittest

from nodes.htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_with_props(self):
        node_with_props = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(
            node_with_props.to_html(), "<a href='https://www.google.com'>Click me!</a>"
        )

    def test_leaf_node_without_props(self):
        node_without_props = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(
            node_without_props.to_html(), "<p>This is a paragraph of text.</p>"
        )

    def test_leaf_node_without_tag(self):
        node_without_tag = LeafNode(None, "Text")

        self.assertEqual(node_without_tag.to_html(), "Text")

    def test_leaf_node_without_value(self):
        node_without_tag = LeafNode(None, None)

        with self.assertRaises(ValueError):
            node_without_tag.to_html()

