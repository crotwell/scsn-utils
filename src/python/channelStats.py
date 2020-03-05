import simpleDali
import simpleMiniseed
import asyncio
import logging
import signal
import sys
import json
import math
import websockets
from datetime import datetime, timedelta
from array import array

#logging.basicConfig(level=logging.DEBUG)


host = "129.252.35.36"
port = 6384
# port = 15006 ##for MSEED data
#host = "129.252.35.20"
#host = "127.0.0.1"
#port = 6382
uri = "ws://www.seis.sc.edu/dragracews/datalink"

programname="triggerListen"
username="dragrace"
processid=0
architecture="python"

keepGoing = True


def handleSignal(sigNum, stackFrame):
    print("############ handleSignal {} ############".format(sigNum))
    global keepGoing
    if keepGoing:
        keepGoing = False
    else:
        sys.exit(0)
signal.signal(signal.SIGINT, handleSignal)
signal.signal(signal.SIGTERM, handleSignal)

async def connection(loop):
    try:
        dali = simpleDali.WebSocketDataLink(uri)
        await dali.parseResponse()
    except Exception:
        dali = simpleDali.SocketDataLink(host, port)
    dali.verbose = True
    serverId = await dali.id(programname, username, processid, architecture)
    print("Resp: {}".format(serverId))
    serverInfo = await dali.info("STATUS")
    print("Info: {} ".format(serverInfo.message))
    print("File directory?")
    channelLoc = input()
    if channelLoc == '0':
        r = await dali.match("XX.XB08.00.HN./MSEED")
    else:
        r = await dali.match(channelLoc)

    begintime = datetime.utcnow() - timedelta(seconds=2)
    r = await dali.positionAfter(begintime)
    if r.type.startswith("ERROR"):
        print("positionAfter() Resonse {}, ringserver might not know about these packets?".format(r))
    else:
        print("positionAfter() Resonse m={}".format(r.message))
    r = await dali.stream()
    sys.stdout.flush()
    while(keepGoing):
        peakPacket = await dali.parseResponse()
        if not peakPacket.type == "PACKET":
            print("parseResponse not a PACKET {} ".format(peakPacket))
        else:
            peakInfo={}
            devationValues = []
            squares = []
            peakInfo= simpleMiniseed.unpackMiniseedRecord(peakPacket.data).data
            channelX = simpleMiniseed.unpackMiniseedHeader(peakPacket.data).channel
            timestamp = simpleMiniseed.unpackMiniseedRecord(peakPacket.data).starttime()
            average = sum(peakInfo) / len(peakInfo)
            for x in range(len(peakInfo)):
                squares.append(peakInfo[x]**2)
                rms = math.sqrt(sum(squares) / len(peakInfo))
            for x in range(len(peakInfo)):
                devationValues.append( (peakInfo[x] - average) ** 2)
            devation = math.sqrt(sum(devationValues) / (len(peakInfo) - 1))

            print('-========== Channel {} ==========-'.format(channelX))
            print('standard dev = {}'.format(devation))
            print('rms = {}'.format(rms))
            print('max value = {}'.format(max(peakInfo)))
            print('min value = {}'.format(min(peakInfo)))
            print('average = {}'.format(average))
            print('timestamp = {}'.format(timestamp))

            peakInfo={}
        sys.stdout.flush()
    dali.close()


loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(connection(loop))
loop.close()

# doto:
# min value, max value, rms value of each channel
# make sure the data stream is actually decompressed
# buffer the data to take a sample every 10 seconds
#### change how the data is printed so that you only print packets that arrive at the same time X(t)=Y(t)=Z(t)
