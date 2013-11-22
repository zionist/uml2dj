class Model:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.fields = []
        # for pk links to another object
        self.pks = []
