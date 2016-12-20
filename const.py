
""" This document provides a guideline for the class creators and class invokers
for a set of default and allowed values. This is only for demonstration purposes
only, and may change from time to time. """

# Allowed language types, on most OJs
language_types = [
    'C', # Enforce ISO C99 dialect
    'C++', # Enforce ISO C++03 dialect
    'C++11', # Enforce ISO C++11 dialect
    'C#', # Mono 3.12.1.0
    'Go', # Go 1.7.3
    'Haskell', # GHC 7.8.3
    'Java', # JDK 1.8.0_112
    'Pascal', # Free Pascal 2.6.4
    'Perl', # Perl 5.20.1
    'PHP', # PHP 7.0.12
    'Python', # By default be Python 3
    'Python2', # Python 2.7.12, CPython
    'Python3', # Python 3.5.2, CPython
    'Ruby', # Ruby 2.0.0
]

# Allowed problem description languages
document_types = [
    'Markdown', # GitHub Flavoured Markdown, without line-end breaks, with MathJax.
    'LaTeX', # Unicode-enabled LaTeX without additional macros
    'HTML5', # Standard HTML5 document, must be checked by class author for intactness
    'HTML', # Unmodified HTML document (from online websites, mostly)
]

# Allowed image formats, in order to be embedded
image_types = [
    'SVG', # Scalable Vector Graphics
    'PNG', # Portable Network Graphics
]

# A sample JSON file for class developers.
default_json = {
    'metadata': {
        'engine': 'Codeforces',
        'id': 'Problemset.746A',
        # 'id': 'Contest.746.A',
        # 'id': 'Gym.101026.A',
        'date_created': '2016-11-19T08:00:00+08:00' # Comply to ISO-8601 standards
        'tags': {
            'title': 'Codeforces Round #386 (Div. 2) - A. Compote',
            'time_limit': 1.0, # In seconds
            'memory_limit': 268435456, # In bytes
        },
    },
    'problem': {
        # GitHub flavoured Markdown, without line-end breaks. Support MathJax extensions.
        'Markdown': [
            'description': '# Lorem Ipsum\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
            'input': 'The **first line** contains the positive integer $a (1 \\leq a \\leq 1000)$ - the number of lemons Nikolay has.',
            'output': 'Print *the maximum* total number of lemons, apples and pears from which Nikolay can cook the compote.',
            'note': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        ],
        # Must be compilable with XeLaTeX or LuaLaTeX, and must be Unicode-compatible.
        'LaTeX': [
            'description': '\\subsection{Lorem Ipsum}\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
            'input': 'The \\textbf{first line} contains the positive integer $a (1 \\leq a \\leq 1000)$ - the number of lemons Nikolay has.',
            'output': 'Print \\textit{the maximum} total number of lemons, apples and pears from which Nikolay can cook the compote.',
            'note': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        ],
        # Use MathJax extension for math displays
        'HTML5': [
            'description': '<h2>Lorem Ipsum</h2><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>',
            'input': '<p>The <b>first line</b> contains the positive integer <span class="math inline">a (1 \\leq a \\leq 1000)</span> - the number of lemons Nikolay has. </p>',
            'output': '<p>Print <i>the maximum</i> total number of lemons, apples and pears from which Nikolay can cook the compote.</p>',
            'note': '<p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>',
        ],
        # Directly stripped off the entire context from online judge. If was
        # converted from LaTeX or Markdown, this can be the same as HTML5, but
        # a combined one.
        'HTML': '<h2>Description</h2>\n<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>\n\n<h2>Input</h2>\n<p>The <b>first line</b> contains the positive integer <span class="tex-span"><i>a</i></span> (<span class="tex-span">1 ≤ <i>a</i> ≤ 1000</span>) — the number of lemons Nikolay has. </p>\n\n<h2>Output</h2>\n<p>Print <i>the maximum</i> total number of lemons, apples and pears from which Nikolay can cook the compote.</p>\n\n<h2>Note</h2>\n<p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>',
    },
    'sample_data': [
        {
            'input': '2\n5\n7\n',
            'output': '7\n',
        },
        {
            'input': '4\n7\n13\n',
            'output': '21\n',
        },
    ],
    'objects': [
        {
            'name': 'd08c64de.png', # Takes the first 8 digits of the hash and append lower-case extension
            'hash': 'd08c64dea518d884b6148c1d506ab7fb12e31e9a1599714a9c7fe5645ccbc0b5', # SHA2-256 algorithm.
            'data': b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\xcd\x00\x00\x00\xfa\x08\x06\x00\x00\x00\xc3M\x1c\xbc\x00\x00\x00\x01sRGB\x00',
        },
    ],
}
