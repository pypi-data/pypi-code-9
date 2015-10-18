import mistune


class GenerateMarkdown:
    def __init__(self, input):
        self.input = input
        self.m = mistune.Markdown()

    @property
    def output(self):
        return self.m(self.input)
