def register(linter):
    pass


def load_configuration(linter):
    linter.config.ignore += ("bin",)
