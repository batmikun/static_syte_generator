import unittest

from nodes.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_fail(self):
        node = TextNode("Thi is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Thi is a text node", TextType.BOLD)
        self.assertNotEqual(
            node.__repr__(), f"TextNode(Thi is a text node,{TextType.BOLD.name})"
        )


if __name__ == "__main__":
    unittest.main()

