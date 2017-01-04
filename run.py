import os
import json
import errno
import base64
import logging
from multiprocessing import current_process

import rsyslog
from curio_http import ClientSession
from asynctcp import AsyncTcpCallbackServer

current_process().name = os.environ['HOSTNAME']
rsyslog.setup(log_level = os.environ['LOG_LEVEL'])
LOGGER = logging.getLogger(__name__)
logging.getLogger('curio_http').setLevel(logging.WARNING)

async def get_downloads(json_request):
    async with ClientSession() as session:
        url = 'https://pypi.python.org/pypi/{}/json'.format(json_request['module'])
        response = await session.get(url)
        if response.status_code == 404:
            LOGGER.debug('No such package {}'.format(json_request['module']))
            data = { 'impact': 0 }
        elif (response.status_code < 200) or (response.status_code >= 300):
            LOGGER.error('GET of {} returned {}'.format(url, response.status_code))
            data = { 'error': errno.EIO, 'impact': None }
        else:
            content = await response.json()
            downloads = 0
            for version, variants in content['releases'].items():
                for variant in variants:
                    downloads += variant['downloads']
            data = { 'impact': downloads }
            LOGGER.debug('Impact for module {} is {}'.format(json_request['module'], data['impact']))
        return json.dumps(data)

if __name__ == '__main__':
    AsyncTcpCallbackServer('0.0.0.0', 25000, get_downloads, memoized = True).run()
