class Number:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '<{}>'.format(self.value)

    def evaluate(self, environment):
        return self


class Boolean:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '<{}>'.format(self.value)

    def evaluate(self, environment):
        return self


class Add:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '<{} + {}>'.format(self.left, self.right)

    def evaluate(self, environment):
        return Number(self.left.evaluate(environment).value +
                      self.right.evaluate(environment).value)


class Variable:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<{}>'.format(self.name)

    def evaluate(self, environment):
        return environment[self.name]


class Multiply:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '{} * [}'.format(self.left, self.right)

    def evaluate(self, environment):
        return Number(self.left.evaluate(environment).value *
                      self.right.evaluate(environment).value)


class LessThan:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '<{} < {}>'.format(self.left, self.right)

    def evaluate(self, environment):
        return Boolean(self.left.evaluate(environment).value <
                       self.right.evaluate(environment).value)


class Assign:

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return '<{} = {}>'.format(self.name, self.expression)

    def evaluate(self, environment):
        return environment.update({self.name: self.expression.evaluate(environment)})


class DoNothing:

    def __str__(self):
        return '<do-nothing>'

    def evaluate(self, environment):
        return environment


class If:

    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return 'If ({0}) {{1}} else {{2}}'.format(self.condition, self.consequence, self.alternative)

    def evaluate(self, environment):
        if self.condition.evaluate(environment) == Boolean(True):
            return self.consequence.evaluate(environment)
        elif self.condition.evaluate(environment) == Boolean(False):
            return self.alternative.evaluate(environment)


class Sequence:

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return '<{}; {}>'.format(self.first, self.second)

    def evaluate(self, environment):
        return self.second.evaluate(self.first.evaluate(environment))


class While:

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return '<while ({0}) {{1}}>'.format(self.condition, self.body)

    def evaluate(self, environment):
        if self.condition.evaluate(environment) == Boolean(True):
            return self.evaluate(self.body.evaluate(environment))
        elif self.condition.evaluate(environment) == Boolean(False):
            return environment