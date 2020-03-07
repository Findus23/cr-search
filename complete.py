import readline

from models import Phrase


class SimpleCompleter:

    def __init__(self):
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                phrases = Phrase.select().where((Phrase.until_episode == 9) & (Phrase.text % ("%" + text + "%")))
                self.matches = [p.text for p in phrases]
                # self.matches = [s
                #                 for s in self.options
                #                 if s and s.startswith(text)]
        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def input_loop():
    line = ''
    while line != 'stop':
        line = input('Prompt ("stop" to quit): ')
        print('Dispatch %s' % line)


phrases = Phrase.select().where((Phrase.until_episode == 9) & (Phrase.text % ("%" + "test" + "%")))

print([p.text for p in phrases])

# Register our completer function
readline.set_completer(SimpleCompleter().complete)

# Use the tab key for completion
readline.parse_and_bind('tab: complete')

# Prompt the user for text
input_loop()
