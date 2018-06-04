
def lint(f):
  from yamllint.config import YamlLintConfig
  from yamllint.linter import run

  return run(f, YamlLintConfig('extends: default'))

def spellcheck(f):
  from enchant import DictWithPWL

  d = DictWithPWL("en_US", "maps/custom.words")

  for w in [i.lower().strip() for i in sys.stdin.readlines() ]:
    print("{0}\t{1}".format(d.check(w), w))

