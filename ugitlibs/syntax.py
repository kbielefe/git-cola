class GenericSyntaxHighligher(QSyntaxHighlighter):
		self.__rules = []

	FINAL_STR = '__FINAL__:'
	def final(self, pattern=''):
		'''Denotes that a pattern is the final pattern that should
		be matched.  If this pattern matches no other formats
		will be applied, even if they would have matched.'''
		return GenericSyntaxHighligher.FINAL_STR + pattern

	def create_rules(self, *rules):
		if len(rules) % 2:
			raise Exception("create_rules requires an even "
					"number of arguments.")
		for idx, rule in enumerate(rules):
			if idx % 2: continue
			formats = rules[idx+1]
			terminal = rule.startswith(self.final())
			if terminal:
				rule = rule[len(self.final()):]
			regex = re.compile(rule)
			self.__rules.append((regex, formats, terminal,))

	def get_formats(self, line):
		matched = []
		for regex, fmts, terminal in self.__rules:
			match = regex.match(line)
			if match:
				matched.append([match, fmts])
				if terminal: return matched
		return matched

	def mkformat(self, fg, bg=None, bold=False):
		format = QTextCharFormat()
		if bold: format.setFontWeight(QFont.Bold)
		format.setForeground(fg)
		if bg: format.setBackground(bg)
		return format
		formats = self.get_formats(ascii)
		if not formats: return
		for match, fmts in formats:
			start = match.start()
			end = match.end()
			groups = match.groups()

			# No groups in the regex, assume this is a single rule
			# that spans the entire line
			if not groups:
				self.setFormat(0, len(ascii), fmts)
				continue

			# Groups exist, rule is a tuple corresponding to group
			for grpidx, group in enumerate(groups):
				# allow None as a no-op format
				length = len(group)
				if fmts[grpidx]:
					self.setFormat(start, start+length,
							fmts[grpidx])
				start += length

class DiffSyntaxHighlighter(GenericSyntaxHighligher):
	def __init__(self, doc,whitespace=True):
		GenericSyntaxHighligher.__init__(self,doc)
		begin = self.mkformat(Qt.darkCyan, bold=True)
		diffhead = self.mkformat(Qt.darkYellow)
		addition = self.mkformat(Qt.darkGreen)
		removal = self.mkformat(Qt.red)
		if whitespace:
			bad_ws = self.mkformat(Qt.black, Qt.red)

		# We specify the whitespace rule last so that it is
		# applied after the diff addition/removal rules.
		# The rules for the header
		self.create_rules(
			self.final('^@@|^\+\+\+|^---'), begin,
			self.final('^diff --git'), diffhead,
			self.final('^index \S+\.\.\S+'), diffhead,
			self.final('^new file mode'), diffhead,
			'^\+', addition,
			'^-', removal,
			)
		if whitespace:
			self.create_rules('(.+)(\s+)$', (None, bad_ws,))

class LogSyntaxHighlighter(GenericSyntaxHighligher):
	def __init__(self, doc):
		GenericSyntaxHighligher.__init__(self,doc)

		dark_cyan = self.mkformat(Qt.darkCyan, bold=True)
		blue = self.mkformat(Qt.blue, bold=True)

		self.create_rules(
			self.final('^\w{3}\W+\w{3}\W+\d+\W+'
					'[:0-9]+\W+\d{4}$'),
			dark_cyan,
			'^([^:]+:)(.*)$',
			(blue, dark_cyan),
			)
		def setupUi(self, dialog):
			dialog.resize(QtCore.QSize(QtCore.QRect(0,0,720,512).size()).expandedTo(dialog.minimumSizeHint()))
			self.vboxlayout = QtGui.QVBoxLayout(dialog)
			self.output_text = QtGui.QTextEdit(dialog)
			self.output_text.setFont(font)
			self.output_text.setAcceptDrops(False)
			self.vboxlayout.addWidget(self.output_text)
			DiffSyntaxHighlighter(self.output_text.document())