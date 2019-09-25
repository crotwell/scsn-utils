import simpleDali
import simpleMiniseed
import asyncio
import logging
import signal
import sys
import json
import math
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

async def doTest(loop):
    dali = simpleDali.SocketDataLink(host, port)                                # creates datalink through a regular socket
    #dali = simpleDali.WebSocketDataLink(uri)                                   # creates datalink throguh a websocket (not working)
    dali.verbose = True                                                         # "yes send me debug codes"
    serverId = await dali.id(programname, username, processid, architecture)    # send the server your iD and wait for the server to respond with its iD
    print("Resp: {}".format(serverId))                                          # print the server iD
    serverInfo = await dali.info("STATUS")                                      # request a message from the server, specifically the server status
    print("Info: {} ".format(serverInfo.message))                               # take the response from the server and print the server's status
    #serverInfo = yield from dali.info("STREAMS")                               # if the data stream is active request the status and header information about the stream
    #print("Info: {} ".format(serverInfo.message))                              # print the data stream information
    r = await dali.match("XX.XB08.00.HN./MSEED")        ##                      # requests all data with MAXACC somewhere in the name
    #print("match() Resonse {}".format(r))                                      # prints the match response, does not work normally as they are encoded files

    begintime = datetime.utcnow() - timedelta(seconds=2)                        # stores the start time of the program
    r = await dali.positionAfter(begintime)                                     # asks for any information from the server stored after the start time of the program
    if r.type.startswith("ERROR"):                                                                    # if the requested packet match returns an error do this
        print("positionAfter() Resonse {}, ringserver might not know about these packets?".format(r))   #{print the error time, error message from server and "ringserver might not know about these packets?"}
    else:
        print("positionAfter() Resonse m={}".format(r.message))
    r = await dali.stream()
    sys.stdout.flush()
    while(keepGoing):
        peakPacket = await dali.parseResponse()                                 #dali.parseResponse reads the packet's data string and interpertates it
        if not peakPacket.type == "PACKET":                                     #if the data is not actually in a packet format and thus dali.parseResponse cannot read it, follow this
            # might get an OK very first after stream
            print("parseResponse not a PACKET {} ".format(peakPacket))          # print this data is not a packet and the name of the resquested packet
        else:
            peakInfo={}
            devationValues = []
            squares = []                                                         #writes the "peakInfo" varible
            peakInfo=simpleMiniseed.unpackMiniseedRecord(peakPacket.data).data
            channelX = simpleMiniseed.unpackMiniseedHeader(peakPacket.data).channel                                                     #prints the raw peakpacket data
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

            #print(channelX)
            #print(peakInfo)
            #print("{} acceleration is {:7.5f} at {}".format(peakInfo["station"],peakInfo["accel"],peakInfo["time"]))    #prints the formated data

            peakInfo={}
        sys.stdout.flush()                                                      #flushes the data every loop

    dali.close()


loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(doTest(loop))
loop.close()

# doto:
# min value, max value, rms value of each channel
# make sure the data stream is actually decompressed
# buffer the data to take a sample every 10 seconds
#### change how the data is printed so that you only print packets that arrive at the same time X(t)=Y(t)=Z(t)
