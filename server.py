import re
import curio_http
from json import loads
from functools import lru_cache
from curio import run, tcp_server, subprocess, open_connection

KNOWN_PACKAGES = {}

async def get_downloads(package_name):
  print('package is ', package_name)
  if package_name in KNOWN_PACKAGES:
    return KNOWN_PACKAGES[package_name]
  async with curio_http.ClientSession() as session:
    response = await session.get('https://pypi.python.org/pypi/{}/json'.format(package_name))
    if response.status_code != 200:
      return 0
    content = await response.json()
  downloads = 0
  for version, variants in content['releases'].items():
    for variant in variants:
      downloads += variant['downloads']
  KNOWN_PACKAGES[package_name] = downloads
  return downloads

async def echo_client(client, addr):
  while True:
    data = await client.recv(100000)
    if not data:
      break
    download_count = await get_downloads(loads(data.decode())[1].strip())
    await client.sendall(bytes(str(download_count) + '\n', 'utf-8'))
  print('Connection closed')

if __name__ == '__main__':
  run(tcp_server('', 25000, echo_client))
