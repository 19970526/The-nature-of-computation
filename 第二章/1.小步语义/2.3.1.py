class Number:
    '''数字类'''

    def __init__(self, value):
        self.value = value

    @property
    def reducible(self):
        return False

    def __str__(self):
        return '<{}>'.format(self.value)


class Add:
    '''加法类'''

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            Add(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            Add(self.left, self.right.reduce(environment))
        else:
            Number(self.left.value + self.right.value)

    def __str__(self):
        return '<{} + {}>'.format(self.left, self.right)


class Multiply:
    '''乘法类'''

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            Multiply(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            Multiply(self.left, self.right.reduce(environment))
        else:
            Number(self.left.value * self.right.value)

    def __str__(self):
        return '<{} * {}>'.format(self.left, self.right)


class Machine:
    '''虚拟机'''

    def __init__(self, expression, environment):
        self.environment = environment
        self.expression = expression

    @property
    def run(self):
        while self.expression.reducible:
            print(self.expression)
            self.expression = self.expression.reduce(self.environment)

        print(self.expression.value)


class Boolean:
    '''布尔值类'''

    def __init__(self, value):
        self.value = value

    @property
    def reducible(self):
        return False

    def __str__(self):
        return '<{}>'.format(self.value)


class LessThan:
    '''小于运算'''

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            LessThan(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            LessThan(self.left, self.right.reduce(environment))
        else:
            Boolean(self.left.value < self.right.value)

    def __str__(self):
        return '<{} < {}>'.format(self.left, self.right)


class Variable:
    '''变量类'''

    def __init__(self, name):
        self.name = name

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        return environment[self.name]

    def __str__(self):
        return '<{}>'.format(self.name)


class DoNothing:
    '''语句'''

    def __str__(self):
        return '<do-nothing>'

    def __eq__(self, other_statement):
        return other_statement == DoNothing()

    @property
    def reducible(self):
        return False


class Assign:
    '''赋值类'''

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return '<{} = {}>'.format(self.name, self.expression)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.expression.reducible:
            return [Assign(self.name, self.expression.reduce(environment)), environment]
        else:
            return [DoNothing(), environment.update({self.name: self.expression})]


class If:
    '''条件'''

    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return '<if ({0}) {{1}} else {{2}}>'.format(self.condition, self.consequence, self.alternative)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.condition.reducible:
            return [If(self.condition.reduce(environment), self.consequence, self.alternative), environment]
        else:
            if self.condition == Boolean(True):
                return [self.consequence, environment]
            elif self.condition == Boolean(False):
                return [self.alternative, environment]


class Sequence:
    '''序列'''

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return '<{} ; {}>'.format(self.first, self.second)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.first == DoNothing():
            return [self.second, environment]
        else:
            reduce_first, reduce_environment = self.first.redece(environment)
            return [Sequence(reduce_first, self.second), reduce_environment]


class While:
    '''while循环'''

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return '<while ({0}) {{1}}>'.format(self.condition, self.body)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        return [If(self.condition, Sequence(self.body, 'while ({0}) {{1}}'.format(self.condition, self.body)),
                   DoNothing()), environment]
