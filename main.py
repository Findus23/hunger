import parser
import json

a = parser.fladerei

print(json.dumps(a.get_menus(), indent=2))
print(a.name)
