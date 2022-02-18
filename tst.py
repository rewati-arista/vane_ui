import pprint
import pyeapi
from showparsers.show_running_config import parse

pp = pprint.PrettyPrinter(indent=4)

node = pyeapi.connect_to('DC1-SPINE1')

running_config = node.get_config()

running_config_dict = {}
parse(running_config_dict, 'show running-config', running_config)

print ('The entire running config dictionary. Features are keys')
pp.pprint(running_config_dict['show running-config'])

print ('The entire running config dictionary. Features are keys')
pp.pprint(running_config_dict['show running-config'].keys())

print ('To get only interface keys')
interfaces = {k: v  for k,v in running_config_dict['show running-config'].items() if k.startswith('interface')}
pp.pprint(interfaces)

print ('To get only user  keys')
users = {k: v  for k,v in running_config_dict['show running-config'].items() if k.startswith('username')}
pp.pprint(users)
