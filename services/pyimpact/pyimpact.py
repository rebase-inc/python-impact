from asynctcp import AsyncTCPCallbackServer
from curio_http import ClientSession
from logging import getLogger

from rsyslog import setup
    
setup()
LOGGER = getLogger(__name__)

async def get_downloads(package_name):
    async with ClientSession() as session:
        url = 'https://pypi.python.org/pypi/{}/json'.format(package_name)
        response = await session.get(url)
        if (response.status_code < 200) or (response.status_code >= 300):
            LOGGER.error('GET of {} returned {}'.format(url, response.status_code))
            return 0
        content = await response.json()
        if 'releases' not in content:
            LOGGER.error('PyPI server response is invalid: missing "releases" key in response')
            return 0 
        downloads = 0
        for version, variants in content['releases'].items():
            for variant in variants:
                downloads += variant['downloads']
        return downloads 

if __name__ == '__main__':
    AsyncTCPCallbackServer(callback = get_downloads, host = '0.0.0.0').run()
