# HTML

The primary output of a static site generatir is HTML (HyperText Markup Language), because HTML es all you need to render a web page in a browser.

HTML is a simple markup language that's good at structuring content. It's just a way to format text, images, links, and other media so that a web browser can render it as a GUI.

Here's an example of a simplre HTML file that represents a blog post with a title (the part in the browser tab), a heading, and two paragraphs of text:

```html
<html>
  <head>
    <title>Why Frontend Development Sucks</title>
  </head>

  <body>
    <h1>Front-end Development is the Worst</h1>
    <p>
      Look, front-end development is for script kiddies and soydevs who can't
      handle the real programming. I mean, it's just a bunch of divs and spans,
      right? And css??? It's like, "Oh, I want this to be red, but not thaaaaat
      red." What a joke.
    </p>
    <p>
      Real programmers code, not silly markup languages. They code on Arch
      Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code.
      They use C, not HTML. Come to the
      <a href="https://www.boot.dev">backend</a>, where the real programming
      happens.
    </p>
  </body>
</html>
```

HTML is a tree-like structure where each tag can contain other tags, and the whole thing is enclosed in a n outermos <html> tag. Let's break down the structure of this HTML file:

- `<html>` is the root element of the document.
- `<head>` contains metada about the document. Anything in the `<head>` is not rendered visibly in the browser window
  - `<title>` is the title of the document, which is displayed in the browser tab
- `<body>` contains the content of the document, which is what is rendered in the browser window.
  - `<h1>` is a top-level heading.
  - `<p>` is a pragraph of text.
  - `<a>` is a hyperlink. The `href` attribute is the URL the link points to. Attributes are key-value pairs that provide additional information about an element, like `href="https://www.boot.dev"`

All HTML tags are enclosed in angle brackets, and most have an opening tag (e.g `<p>`) and a closing tag (e.g `</p>`). Anything between the opnening and closing tags is the content of the tag, which is sometimes just text, and sometimes more nested tags.

# Python

Creating a simple server with python

```python
import argparse
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler


class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()


def run(
    server_class=HTTPServer,
    handler_class=CORSHTTPRequestHandler,
    port=8000,
    directory=None,
):
    # Change the current working directory if directory is specified
    if directory:
        os.chdir(directory)

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving HTTP on http://localhost:{port} from directory '{directory}'...")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Server with CORS")
    parser.add_argument(
        "--dir", type=str, help="Directory to serve files from", default="."
    )
    parser.add_argument("--port", type=int, help="Port to serve HTTP on", default=8888)
    args = parser.parse_args()

    run(port=args.port, directory=args.dir)
```

# CSS (Cascading Style Sheets)

Is another not-really-a-programming-language that's good at styling components. It's a way to dress up your HTML with colors, fonts, responsive layouts, animations, etc.

CSS is a set of styling rules that target different HTML elements. For example, we can say we want all of our primary headings to be red:

```css
h1 {
  color: red;
}
```

Or maybe we want the max-width of our paragraphs to be 50% of the screen width:

```css
p {
    max-width: 50%:
}
```

# MARKDOWN

Writings markdown is a less-verbose markup language designed for ease of writing. The trouble is, web browsers don't understand Markdown, They only understand HTML and CSS. So, the #1 job of a statice site generator is to convert Markdown into HTML

So, instead of a super-verbose HTML list:

```html
<ul>
  <li>I really</li>
  <li>hate writing</li>
  <li>in raw html</li>
</ul>
```

We can write a Markdown list:

- I really
- hate writing
- in raw HTML

Our static site generator will take a directory of Markdown files (one for each web page), and a simple HTML and CSS template, and output a browser-ready bundle of HTML and CSS files.

MARKDOWN |-> STATIC SITE GENERATOR |-> HTML
TEMPLATE |-> STATIC SITE GENERATOR |-> CSS

# CHEAT SHEET

Cover the basics of MARKDOWN

## Headings

```html
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
```

```markdown
# Heading 1

## Heading 2

### Heading 3
```

## Paragraphs

```html
<p>This is a paragraph of text.</p>
```

```markdown
This is a paragraph of text.
```

## Bold

```html
<p>This is a <b>bold</b> word.</p>
```

```markdown
This is a **bold** word.
```

## Italics

```html
<p>This is a <i>italic</i> word.</p>
```

```markdown
This is a _italic_ word.
```

## Links

```html
<a href="https://google.com"> Link </a>
```

```markdown
This is a paragraph with a [link](https://google.com).
```

## Rendering Images

```html
<img src="url/of/image.jpg" alt="Description of Image" />
```

```markdown
![alt text for image](url/of/image.jpg)
```

## Unordered Lists

```html
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
</ul>
```

```markdown
- Item 1
- Item 2
- Item 3
```

## Ordered Lists

```html
<ol>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
</ol>
```

```markdown
1. Item 1
2. Item 2
3. Item 3
```

## Quotes

```html
<blockquote>This is a quote.</blockquote>
```

```markdown
> This is a quote
```

## Code

```html
<code>This is code</code>
```

```markdown
---
This is code
---
```

# TextNode

We're going to be parsing Markdown text, and outputting it to HTML, so we need an intermediate representation of the text in our code.JK

When I say "inline" I just mean text that is part of a larger block of text. For us, this includes:

- Normal text
- Bold text
- Italic text
- Code text
- Links
- Images

Everything else we're considering block level, like headings, paragraphs, and bullet lists.

## Block-level content

In CSS, content that participates in block layout is called block-level content.

In a block layout, boxes are laid out one after the other, vertically, beginning at the top of a containing block. Each box's left outer edge touches the left edge of the containing block.
A block-level element always starts on a new line. In horizontal writing modes, like English or Arabic, it occupies the entire horizontal space of its parent element (container) and vertical space equal to the height of its contents, thereby creating a "block".

## Inline-level content

In CSS, content that participates in inline layout is called inline-level content. Most text sequences, replaced elements, and generated content are inline-level by default.

In inline layout, a mixed stream of text, replaced elements, and other inline boxes are laid out by fragmenting them into a stack of line boxes. Within each line box, inline-level boxes are aligned to each other vertically or horizontally, depending on the writing mode. Typically, they are aligned by the baselines of their text. This can be changed with CSS.

Examples:

```html
<p>
  This span is an <span class="highlight">inline-level element</span>; its
  background has been colored to display both the beginning and end of the
  element's influence. Input elements, like <input type="radio" /> and
  <input type="checkbox" />, are also inline-level content.
</p>
```

In this example, the <p> element contains some text. Within that text is a <span> element and two <input> elements, which are inline-level elements. If the <span> is spread across two lines, two line boxes are generated. Because these elements are inline, the paragraph correctly renders as a single paragraph of unbroken text flow.kl

## TextNode Tests

Unit tests are a way to verify that the code you write works as expected. It's often worth it, especially if the logic you're testing is particularly complex while simultaneously easy to test (e.g it doesn't rely on external stuff like files on disk)

# HTMLNode

Next, we're going to need a way to represent HTML nodes. A "TextNode" is sort of an intermediate representation between Markdown and HTML, and is specif to inline markup. The HTMLNose class will represent a "node" in HTML document tree (like a <p> tag and its contents, or an <a> tag ans its contents) and is purpose-built to render itself as HTML.

# LeafNode

Now we need to actually render some HTML strings. A LeafNode is a type of HTMLMode that represents a single HTML tag with no children. For example, a single <p> tag with some text inside of it

```html
<p>This is a paragraph of text.</p>
```

We call it a "leaf" node because its a "leaf" in the tree of HTML nodes. It's a node with no children.

# Extract Links

A regular expression or "regex" for short, is a programming-language-agnostic way of searching for patterns in text.
In Python, we can use the `re` module to work with regex. The `re` module has a `findall` function that will return a list of all the matchets in a string.

```python
import re

text = "I'm a little teapot, short and stout. Here is my handle, here is my spout."
matches = re.findall(r"teapot", text)
print(matches) # ['teapot']
```

`r"teapot"` is a regex pattern. The `r` at the beginning of the string just tells Python to treat the string as a "raw" `string`, which means we don't have to escape backslashes. The pattern teapot will just match any exact occurrence of the word "teapot" in the string.

Regez can also match more complex patterns. For example, it can find emails:

```python
text = "My email is lane@example.com and my friend's email is hunter@example.com"
matches = re.findall(r"\w+@\w+\.\w+", text)
print(matches) # ['lane@example.com', 'hunter@example.com']
```

- `.` Matches a single character of any single character, except the end of a line. The below regex matches shrt, short and any character between sh and rt `sh.rt`
- `^` Matches a term if the term appears at the beginning of a paragraph or a line. The below regex maches a paragraph or a line that starts with Apple `^Apple`
- `^ inside a bracket` The below regex matches any characters but a,b,c,d,e `[^a-e]`
- `$` Matches a term if the term appears at the end of a paragraph or line. The below regext matches a paragraph or a line that ends with bye `bye$`
- `[]` Matches any single character from withn the bracketed list. The below regex matches bad, bed, bcd, brd amd bod `b[aecro]d`
- `-` Represents a range of letters or numbers, often used inside a square bracket. The below regex matches kam, kbm, kcm, k2m, k3m, k4m abd k5m `k[a-c2-5]m`
- `()` Groups one or more regular expressions. The below regex matches codexpedia.com, codexpedia.net and codexpedia.or `codexpedia\.(com|net|org)`
- `{n}` Matches exactly n times of the preceding character. The below regular expression matches 4 digits string, and only four digits string because there is ^ at the beginninga nd $ at the end of the regex. `^[\d]{4}$`
- `{n,m}` Curly brackets with 2 numbers inside it, matches minimum and maximum number of times of the preceding character. The below regular expression matches google, gooogle and goooogle. `go{2,4}gle`
- `{n,}` Curly brackets with a number and a comma, matches minimum number of times the preceding character. For example, the below regex matches google, gooogle, gooooogle, goooooogle, …. `go{2,}gle`
- `|` Matches either the regular expression preceding it or the regular expression following it. The below regex matches the fomart dates of MM/DD/YYYY, MM.DD.YYYY and MM-DD-YYYY `^(0[1-9]|1[012])[-/.](0[1-9]|[12][0-9]|3[01])[-/.][0`
- `?` Matches 1 or 0 character in front of the question mark. The below regular expression matches apple and apples `apples?`
- `*` Matches 0 or more characters in front of the asterisk. The below regular expression mathces cl, col, cool, cooool, cooooooool, ... `co*l`
- `+` Matches 1 or more characters in front of the plus. The below regular expression matches col, coool, cooooool, ... `co+l`
- `!` Do not matches the next character or regular expression. The below regular expression matches the characher q if the charachter after q is not a digit, it will matches the q in those strings of abdqk, quit, qeig, but not q2kd, sdkq8d. `q(?![0-9])`
- `\` Backslash, turns off the special meaning of the next character. The below regex treats the period as a normal character and it matches a.b only. `a\.b`
- `\b` Backslash and b, matches a word boundary. For example, “\bwater” finds “watergun” but not “cleanwater” whereas “water\b” finds “cleanwater” but not “watergun”.
- `\n` Backslash and n, represents a line break.
- `\t` Backslash and t, represents a tab.
- `\w` Backslash and w, it is equivalent to `[a-zA-Z0-9_]`, matches alphanumeric character or underscore. Conversely, Capital \W will match non-alphnumeric character and not underscore.
- `\d` Backslash and d, matches digits 0 to 9, equivalent to `[0-9]` or `[:digit]`
- `[:alpha:]` or `[A-Za-z]` represents an alphabetic character.
- `[:digit:]` or `[0-9]` or `[\d]` represents a digit.
- `[:alnum:]` or `[A-Za-z0-9]` represents an alphanumeric character.

Examples:

This regex matches email addresses:

- `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b`

This regex matches websites links ending with sites of .com, .org, .edu, .gov and .us:

- `https?://(www\.)?[A-Za-z0-9]+\.(com|org|edu|gov|us)/?.\*`

This regex matches social security numbers.

- `^[0-9]{3}-[0-9]{2}-[0-9]{4}$`

So, `\w+@\w+\.\w+` says "match one or more alphanumeric characters, followed by an @, followed by one or more alphanumeric characters, followed by a . and one or more alphanumeric characters."

I love [regexr](https://regexr.com/) for interactive regex testing, it breaks down each part of the pattern and explains what it does.
