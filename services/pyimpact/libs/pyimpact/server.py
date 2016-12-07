from asynctcp import AsyncTCPCallbackServer

# def get_downloads(data):
#   package_name = loads(data.decode())[1].strip()
#   async with ClientSession() as session:
#     response = await session.get(PYPI_URL.format(package_name))
    
#     if not (200 <= response.status_code < 300):
#       LOGGER.error('PyPI returned HTTP status code {}'.format(response.status_code))
#       return 0

#     content = await response.json()
#     if 'releases' not in content:
#       LOGGER.error('PyPI returned HTTP status code {}'.format(response.status_code))
#       return 0
#     else:
#       for version, variants in content['releases'].items():
#         for variant in variants:
#           downloads += variant['downloads']
#           KNOWN_PACKAGES[package_name] = downloads
#       return downloads


#     content = await response.json()
#     downloads = 0
#     if 'releases' not in content:
#       LOG.error('PyPI server response is invalid: missing "releases" key in response')
#       return 0
#     for version, variants in content['releases'].items():
#       for variant in variants:
#         downloads += variant['downloads']
#         KNOWN_PACKAGES[package_name] = downloads



# async def get_downloads(package_name):
#     if package_name in KNOWN_PACKAGES:
#         return KNOWN_PACKAGES[package_name]
#     async with ClientSession() as session:
#         response = await session.get('https://pypi.python.org/pypi/{}/json'.format(package_name))
#         if (response.status_code < 200) or (response.status_code >= 300):
#             LOG.error('PyPI returned HTTP status code {}'.format(response.status_code))
#             return 0
#         content = await response.json()
#         downloads = 0
#         if 'releases' not in content:
#             LOG.error('PyPI server response is invalid: missing "releases" key in response')
#             return 0
#         for version, variants in content['releases'].items():
#             for variant in variants:
#                 downloads += variant['downloads']
#                 KNOWN_PACKAGES[package_name] = downloads
#         return downloads


# async def connection_handler(client, addr):
#     LOG.debug('New connection with client at {}'.format(addr))
#     stream = client.as_stream()
#     while True:
#         args_as_JSON = await stream.readline()
#         if not args_as_JSON:
#             break
#         download_count = await get_downloads(loads(args_as_JSON.decode())[1].strip())
#         LOG.debug('download count is {}'.format(download_count))
#         await stream.write(bytes(str(download_count)+'\n', 'utf-8'))
#     LOG.debug('Connection closed')


if __name__ == '__main__':
    print(dir(AsyncTCPCallbackServer))


