import yaml

import parser


def test_answer():
    with open("../reference.yaml", 'r') as stream:
        reference = yaml.load(stream)

    for p in [parser.fladerei, parser.zuppa, parser.aai]:
        comparison = reference[p.name]
        assert comparison == p.get_menus()
