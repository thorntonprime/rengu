from enchant import DictWithPWL
import rengu.verse.yaml

def lint(f):
    from yamllint.config import YamlLintConfig
    from yamllint.linter import run

    return run(f, YamlLintConfig('extends: default'))

def spellcheck(v, d=DictWithPWL("en_US", "maps/custom.words")):

    for w in [i.lower().strip() for i in sys.stdin.readlines() ]:
        print("{0}\t{1}".format(d.check(w), w))

def check(repo, path):
    import os
    os.chdir(repo.RENGU_PATH)

    #yield(path)

    for l in lint(open(path, 'r')):
        yield 'yamllint = ' + str(l)

    #v = rengu.verse.yaml.read_yaml_file(path)
    #yield('spellcheck = ' + path + v.get('Body'))
    
