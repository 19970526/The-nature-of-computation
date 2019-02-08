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


class DFARulebook:

    def __init__(self, rules):
        self.rules = rules

    def next_state(self, state, character):
        return self.rule_for(state, character).follow()

    def rule_for(self, state, character):
        for rule in self.rules:
            if rule.applies_to(state, character):
                return rule
            break


class DFA:

    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return self.accept_states in self.current_state

    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)
        return self.current_state

    def read_string(self, string):
        for character in string:
            self.read_character(character)


class DFADesign:

    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accepts(self, string):
        self.to_dfa().read_string(string)
        return self.to_dfa().accepting()

