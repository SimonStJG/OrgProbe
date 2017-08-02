
import os
import sys
import argparse
import ConfigParser

REQUIRED = [
  "PROBE_UUID","PROBE_SECRET","AMQP_USER","AMQP_PASSWD"
  ]

DEFAULTS = {
  'API_HOST': 'api.blocked.org.uk',
  'API_PORT': '443',
  'API_HTTPS': 'True'
  }

env = os.environ

parser = argparse.ArgumentParser(description="Script to write OrgProbe config file")
parser.add_argument('--output','-o', help="Path to output file")
parser.add_argument('--template','-t', help="Path to template file",
    default=os.path.join(os.path.dirname(sys.argv[0]), 'config.ini.tmpl'),
    )
args = parser.parse_args()

missing = []
for req in REQUIRED:
    if req not in env:
        missing.append(req)

if missing:
    print "Missing environment: " + ",".join(missing)
    sys.exit(1)

cfg = ConfigParser.ConfigParser()
cfg.read([args.template])

cfg.set('api','host', env.get('API_HOST', DEFAULTS['API_HOST']))
cfg.set('api','port', env.get('API_PORT', DEFAULTS['API_PORT']))
cfg.set('api','https', env.get('API_HTTPS', DEFAULTS['API_HTTPS']))

cfg.set('amqp','host', env.get('API_HOST', DEFAULTS['API_HOST']))

cfg.set('amqp','userid', env['AMQP_USER'])
cfg.set('amqp','passwd', env['AMQP_PASSWD'])

cfg.set('public','uuid', env['PROBE_UUID'])
cfg.set('public','secret', env['PROBE_SECRET'])

if 'PROBE_QUEUE' in env:
    cfg.set('public','queue',env['PROBE_QUEUE'])
if 'PROBE_NETWORK' in env:
    cfg.set('public','network', env['PROBE_NETWORK'])

with open(args.output,'w') as fp:
    cfg.write(fp)

