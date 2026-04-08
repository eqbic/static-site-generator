from curses import termattrs

from blocktype import BlockType
from utils import markdown_to_html_node


class TestBlockType:
    def test_heading_1(self):
        text = "# This is a heading"
        assert BlockType.from_block(text) == BlockType.HEADING

    def test_heading_2(self):
        text = "## This is a heading"
        assert BlockType.from_block(text) == BlockType.HEADING

    def test_heading_3(self):
        text = "### This is a heading"
        assert BlockType.from_block(text) == BlockType.HEADING

    def test_heading_4(self):
        text = "#### This is a heading"
        assert BlockType.from_block(text) == BlockType.HEADING

    def test_heading_5(self):
        text = "##### This is a heading"
        assert BlockType.from_block(text) == BlockType.HEADING

    def test_heading_6(self):
        text = "###### This is a heading"
        assert BlockType.from_block(text) == BlockType.HEADING

    def test_heading_too_much(self):
        text = "####### This is a heading"
        assert BlockType.from_block(text) == BlockType.PARAGRAPH

    def test_heading_invalid(self):
        text = "#This is not a heading"
        assert BlockType.from_block(text) == BlockType.PARAGRAPH

    def test_paragraph(self):
        text = "This is not a heading"
        assert BlockType.from_block(text) == BlockType.PARAGRAPH

    def test_code(self):
        text = """```
        print('hello')
        def test():
            return false
        ```"""
        assert BlockType.from_block(text) == BlockType.CODE

    def test_quote_spaceless(self):
        text = ">this is a quote"
        assert BlockType.from_block(text) == BlockType.QUOTE

    def test_quote_space(self):
        text = "> this is also a quote"
        assert BlockType.from_block(text) == BlockType.QUOTE

    def test_quote_multi_line(self):
        text = """> quiote
> another line
> line"""
        assert BlockType.from_block(text) == BlockType.QUOTE

    def test_unordered_list(self):
        text = """- first
- second sdf sdf a
- third"""
        assert BlockType.from_block(text) == BlockType.UNORDERED_LIST

    def test_ordered_list(self):
        text = """1. first entry
2. second entry
3. third entry"""
        assert BlockType.from_block(text) == BlockType.ORDERED_LIST

    def test_ordered_list_invalid(self):
        text = """1. first
3. third"""
        assert BlockType.from_block(text) == BlockType.PARAGRAPH


def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    assert html == "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",



def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    assert html == "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
