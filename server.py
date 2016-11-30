from json import loads
from logging import getLogger
from multiprocessing import current_process
from signal import signal, SIGTERM, SIGINT
from sys import exit

from curio import run, tcp_server
from curio_http import ClientSession


current_process().name = 'impact-python'


# TODO import log.setup and call it
LOG = getLogger(__name__)


KNOWN_PACKAGES = {}


def quit(signal_number, stack_frame):
    exit(0)


async def get_downloads(package_name):
    if package_name in KNOWN_PACKAGES:
        return KNOWN_PACKAGES[package_name]
    async with ClientSession() as session:
        response = await session.get('https://pypi.python.org/pypi/{}/json'.format(package_name))
        if (response.status_code < 200) or (response.status_code >= 300):
            LOG.error('PyPI returned HTTP status code {}'.format(response.status_code))
            return 0
        content = await response.json()
        downloads = 0
        if 'releases' not in content:
            LOG.error('PyPI server response is invalid: missing "releases" key in response')
            return 0
        for version, variants in content['releases'].items():
            for variant in variants:
                downloads += variant['downloads']
                KNOWN_PACKAGES[package_name] = downloads
        return downloads


async def connection_handler(client, addr):
    LOG.debug('New connection with client at {}'.format(addr))
    stream = client.as_stream()
    while True:
        args_as_JSON = await stream.readline()
        if not args_as_JSON:
            break
        download_count = await get_downloads(loads(args_as_JSON.decode())[1].strip())
        LOG.debug('download count is {}'.format(download_count))
        await stream.write(bytes(str(download_count)+'\n', 'utf-8'))
    LOG.debug('Connection closed')


if __name__ == '__main__':
    signal(SIGTERM, quit)
    signal(SIGINT, quit)
    run(tcp_server('', 25000, connection_handler))


