from asynctcp import AsyncTCPCallbackServer

if __name__ == '__main__':
    async def callback(data):
        return bytes('1234\n', 'utf-8')
    AsyncTCPCallbackServer(callback = callback, host='0.0.0.0').run()
