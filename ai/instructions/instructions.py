import os


DIR = os.path.dirname(__file__)


def load_instruction_set(*mds):
  instructions = []
  for md in mds:
    instructions.append(load_instructions(md))
  return '\n'.join(instructions)


def load_instructions(md):
  with open(os.path.join(DIR, md)) as f:
    return f.read()