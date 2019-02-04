class Number:

    def __init__(self, value):
        self.value = value

    def to_py(self):
        return 'lambda e: {}'.format(self.value)


class Boolean:

    def __init__(self, value):
        self.value = value

    def to_py(self):
        return 'lambda e: {}'.format(self.value)


class Variable:

    def __init__(self, name):
        self.name = name

    def to_py(self):
        return 'lambda e: {e{}}'.format(self.name)


class Add:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_py(self):
        return 'lambda e: eval({0}.to_py())(e) + eval({1}.to_py())(e)'.format(self.left, self.right)


class Multiply:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_py(self):
        return 'lambda e: eval({0}.to_py())(e) * eval({1}.to_py())(e)'.format(self.left, self.right)


class LessThan:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_py(self):
        return 'lambda e: eval({0}.to_py())(e) < eval({1}.to_py())(e)'.format(self.left, self.right)


class Assign:

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def to_py(self):
        return 'lambda e: e.update({0}:{1}.to_py()(e))'.format(self.name, self.expression)


class DoNothing:

    def to_py(self):
        return 'lambda e: e'


class If:

    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def to_py(self):
        return 'lambda e: if eval({}.to_py())(e):   eval({}.to_py())(e):'.format(self.condition,
                                                                                 self.consequence)\
               + 'else:   eval({}.to_py())(e)'.format(self.alternative)


class Sequence:

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def to_py(self):
        return 'lambda e: eval({0}.to_py())(eval({1}.to_py())(e))'.format(self.second, self.first)


class While:

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def to_py(self):
        return 'lambda e:' + 'while eval({}.to_py())(e):'.format(self.condition)\
               + 'e = eval({}.to_py())(e)'.format(self.body) + 'e'
