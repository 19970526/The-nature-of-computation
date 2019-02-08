class FARule:

    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state

    def applies_to(self, state, character):
        return self.state == state and self.character == character

    def follow(self):
        return self.next_state

    def inspect(self):
        return '<FARule {} --{} --> {}>'.format(self.state.inspect,
                                                self.character, self.next_state.inspect)


class NFARulebook:

    def __init__(self, rules):
        self.rules = rules

    def next_states(self, states, character):
        lis1 = []
        for state in states:
            lis1 += list(map(self.follow_rules_for, state, character))
        return set(lis1)

    def follow_rules_for(self, state, character):
        lis2 = []
        for rule in self.rules:
            lis2 += list(map(rule.follow(), self.rules_for(state, character)))
        return lis2

    def rules_for(self, state, character):
        lis3 = []
        for rule in self.rules:
            if rule.applies_to(state, character):
                lis3 += rule
        return lis3

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)
        if more_states.issubset(states):
            return states
        else:
            self.follow_free_moves(states + more_states)


class NFA:

    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return any(self.current_states & self.accept_states)

    def read_character(self, character):
        self.current_states = self.rulebook.next_states(self.current_states, character)
        return self.current_states

    def read_string(self, string):
        for character in string:
            self.read_character(character)

    def current_states(self):
        self.rulebook.follow_free_moves(super)


class NFADesign:

    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepts(self, string):
        self.to_nfa().read_string(string)
        return self.to_nfa().accepting()

    def to_nfa(self):
        return NFA(set(self.start_state), self.accept_states, self.rulebook)
