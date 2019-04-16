class ParseError(Exception):
    def __init__(self, expected, received):
        template = "Expected {0} and received ({1}, {2})"
        self.strerror = template.format(expected, received[0], received[1])
        self.args = [self.strerror]


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.next()

    def next(self):
        try:
            self.token = next(self.tokens)
        except StopIteration:
            self.token = ("EOF", "")

    def is_eof(self):
        return self.token[0] == "EOF"

    def is_character(self):
        return self.token[0] == "CHARACTER"

    def is_literal(self):
        return self.token[0] == "LITERAL"

    def is_string(self):
        return self.is_character() or self.is_literal()

    def is_comma(self):
        return self.token[0] == "COMMA"

    def is_to(self):
        return self.token[0] == "TO"

    def is_open_bracket(self):
        return self.token[0] == "OPEN_BRACKET"

    def is_close_bracket(self):
        return self.token[0] == "CLOSE_BRACKET"

    def parse_alphabet_member(self):
        character = self.token
        self.next()
        if self.is_to():
            self.next()
            if self.is_character():
                lower = character
                upper = self.token
                self.next()
                return [("RANGE", [lower, upper])]
            else:
                raise ParseError("CHARACTER", self.token)
        else:
            return [character]

    def parse_alphabet(self):
        if self.is_close_bracket():
            self.next()
            return []
        elif self.is_character():
            member = self.parse_alphabet_member()
            if self.is_comma():
                self.next()
            return member + self.parse_alphabet()
        raise ParseError("CLOSE_BRACKET or CHARACTER", self.token)

    def parse(self):
        if self.is_eof():
            return []
        elif self.is_string():
            string = self.token
            self.next()
            return [string] + self.parse()
        elif self.is_open_bracket():
            self.next()
            return [("ALPHABET", self.parse_alphabet())] + self.parse()
        raise ParseError("EOF or STRING or OPEN_BRACKET", self.token)


def parse(tokens):
    parser = Parser(tokens)
    return parser.parse()


ast = parse(
    iter(
        [
            ("LITERAL", "hello"),
            ("OPEN_BRACKET", "["),
            ("CHARACTER", "a"),
            ("COMMA", ","),
            ("CHARACTER", "e"),
            ("COMMA", ","),
            ("CHARACTER", "i"),
            ("COMMA", ","),
            ("CHARACTER", "o"),
            ("COMMA", ","),
            ("CHARACTER", "u"),
            ("TO", "-"),
            ("CHARACTER", "a"),
            ("COMMA", ","),
            ("CHARACTER", "a"),
            ("CLOSE_BRACKET", "]"),
        ]
    )
)

print(ast)
