# Copyright (c) 2008 David Aguilar
from PyQt4.QtCore import pyqtProperty
from PyQt4.QtCore import QVariant
def TERMINAL(pattern):
    """
    Denotes that a pattern is the final pattern that should
    be matched.  If this pattern matches no other formats
    will be applied, even if they would have matched.
    """
    return '__TERMINAL__:%s' % pattern

# Cache the results of re.compile so that we don't keep
# rebuilding the same regexes whenever stylesheets change
_RGX_CACHE = {}

default_colors = {}
def _install_default_colors():
    def color(c, a=255):
        qc = QColor(c)
        qc.setAlpha(a)
        return qc
    default_colors.update({
        'color_add':            color(Qt.green, 128),
        'color_remove':         color(Qt.red,   128),
        'color_begin':          color(Qt.darkCyan),
        'color_header':         color(Qt.darkYellow),
        'color_stat_add':       color(QColor(32, 255, 32)),
        'color_stat_info':      color(QColor(32, 32, 255)),
        'color_stat_remove':    color(QColor(255, 32, 32)),
        'color_emphasis':       color(Qt.black),
        'color_info':           color(Qt.blue),
        'color_date':           color(Qt.darkCyan),
    })
_install_default_colors()
class GenericSyntaxHighligher(QSyntaxHighlighter):
    def __init__(self, doc, *args, **kwargs):
        for attr, val in default_colors.items():
            setattr(self, attr, val)
        self.init(doc, *args, **kwargs)
        self.reset()

    def init(self, *args, **kwargs):
        pass
    def reset(self):
        self._rules = []
        self.generate_rules()

    def generate_rules(self):
        pass
            terminal = rule.startswith(TERMINAL(''))
                rule = rule[len(TERMINAL('')):]
            if rule in _RGX_CACHE:
                regex = _RGX_CACHE[rule]
            else:
                regex = re.compile(rule)
                _RGX_CACHE[rule] = regex
            self._rules.append((regex, formats, terminal,))
        for regex, fmts, terminal in self._rules:
                if terminal:
                    return matched
    def set_colors(self, colordict):
        for attr, val in colordict.items():
            setattr(self, attr, val)
class DiffSyntaxHighlighter(GenericSyntaxHighligher):
    def init(self, doc, whitespace=True):
        self.whitespace = whitespace
        GenericSyntaxHighligher.init(self, doc)
    def generate_rules(self):
        diff_begin = self.mkformat(self.color_begin, bold=True)
        diff_head = self.mkformat(self.color_header)
        diff_add = self.mkformat(bg=self.color_add)
        diff_remove = self.mkformat(bg=self.color_remove)
        diffstat_info = self.mkformat(self.color_stat_info, bold=True)
        diffstat_add = self.mkformat(self.color_stat_add, bold=True)
        diffstat_remove = self.mkformat(self.color_stat_remove, bold=True)
        if self.whitespace:
        diff_bgn_rgx = TERMINAL('^@@|^\+\+\+|^---')
        diff_hd1_rgx = TERMINAL('^diff --git')
        diff_hd2_rgx = TERMINAL('^index \S+\.\.\S+')
        diff_hd3_rgx = TERMINAL('^new file mode')
        diff_add_rgx = TERMINAL('^\+')
        diff_rmv_rgx = TERMINAL('^-')
                          diff_sts_rgx,     (None, diffstat_info,
                          diff_sum_rgx,     (diffstat_info,
        if self.whitespace:
    def generate_rules(self):
        info = self.mkformat(self.color_info, bold=True)
        emphasis = self.mkformat(self.color_emphasis, bold=True)
        date = self.mkformat(self.color_date, bold=True)

        info_rgx = '^([^:]+:)(.*)$'
        date_rgx = TERMINAL('^\w{3}\W+\w{3}\W+\d+\W+[:0-9]+\W+\d{4}$')

        self.create_rules(date_rgx, date,
                          info_rgx, (info, emphasis))

# This is used as a mixin to generate property callbacks
def accessors(attr):
    private_attr = '_'+attr
    def getter(self):
        if private_attr in self.__dict__:
            return self.__dict__[private_attr]
        else:
            return None
    def setter(self, value):
        self.__dict__[private_attr] = value
        self.reset_syntax()
    return (getter, setter)

def install_theme_properties(cls):
    # Diff GUI colors -- this is controllable via the style sheet
    for name in default_colors:
        setattr(cls, name, pyqtProperty('QColor', *accessors(name)))

def set_theme_properties(widget):
    for name, color in default_colors.items():
        widget.setProperty(name, QVariant(color))
            self.syntax = DiffSyntaxHighlighter(self.output_text.document())
