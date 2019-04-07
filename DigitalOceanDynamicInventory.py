#!/usr/bin/env python

from argparse import ArgumentParser
import json
import requests
from sys import exit

parser = ArgumentParser(description="AWX DO dynamic host inventory")
parser.add_argument(
    '--list',
    default=False,
    dest="list",
    action="store_true",
    help="Produce a JSON consumable grouping of servers for Ansible"
)
args = parser.parse_args()

digitalOceanToken = "X"

if not digitalOceanToken:
    exit("HALT: No digitalOceanToken specified")

if args.list:
  headers = {
    'Authorization': 'Bearer %s' % digitalOceanToken,
    'Content-Type' : 'application/json'
  }
  inventory = {}
  result = requests.get('https://api.digitalocean.com/v2/droplets?tag_name=X', headers=headers)
  results = result.json()
  droplets = results['droplets']

  # Build up final dictionary structure
  inventory['du-deployment'] = {}
  inventory['du-deployment']['hosts'] = []
  inventory['_meta'] = {}
  inventory['_meta']['hostvars'] = {}
  hosts = []
  for host in droplets:
    hostName = host['name']
    hostIp = host['networks']['v4'][0]['ip_address']
    hostTags = host['tags']

    # Build hosts list
    hosts.append(hostIp)

    # Build inventory meta dict
    inventory['_meta']['hostvars'][hostIp] = { 'server_hostname': hostName, 'tags': hostTags, 'ansible_host': hostIp }

  for h in hosts:
      inventory['du-deployment']['hosts'].append(h)

  inv_string = json.dumps(inventory, indent=1, sort_keys=True)
  print(inv_string)
