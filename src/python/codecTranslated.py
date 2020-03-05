from array import array
import struct
import math
import numpy as np

class EncodedDataSegment:
    def __init__(self, tempSamples, buf,  numFrames, samples=[],
                 current=0,start=0, firstData=0,lastValue=0):
        self.buf=buf=4*numSamples
        self.samples=samples=[]
        self.tempSamples=tempSamples
        self.numFrames=numFrames=len(dataView)/64
        self.current=current=0
        self.start=start=0
        self.firstData=firstData=0
        self.lastValue=lastValue=0

def extractSteim1Samples(dataView, offset,  littleEndian, swapBytes):# Array<number>
    if littleEndian:
        i32 = "<i"
        i16 = "<h"
        iUn = "<I"
    else:
       i32= ">i"
       i16 = ">h"
       iUn = "<I"
    nibbles = struct.unpack_from(i32, dataView, offset)
    currNibble = 0
    swapBytes = "?"
    temp = 4 * samples ## 16 longwords, can't be more than 64
    currNum = 0
    for i in range(16):   #  i is the word number of the frame starting at 0
        currNibble = (nibbles >> (30 - i*2 ) ) & 0x03
        currNibble = (nibbles >> (30 - i*2) ) & 0x03
        if (currNibble == 0):
            offset == 0
            temp[currNum + 1] = struct.unpack_from(i32, dataView, offset+(i*4))
            return temp
            #break
        elif (currNibble == 1):
            for n in range(4):
                temp[currNum] = struct.unpack_from(dataView, offset+(i*4)+n)
                currNum = currNum + 1
            return temp
            #    break
        elif (currNibble == 2):
            for n in range(4):
                temp[currNum] = struct.unpack_from(i16, dataView, offset+(i*4)+n)
                currNum = currNum + 1
            return temp
            #break
        elif (currNibble == 3):
           temp[currNum + 1] = struct.unpack_from(i16, dataView, offset+(i*4))
           return temp
           break
        else:
            #raise Expection(("unreachable case:=={}".format(currNibble))
            break
        #return temp

#################
def decodeSteim1(temp, numSamples, littleEndian, bias): #Int32Array
    if ((len(temp) * 64) != 0):
        raise Exception( "encoded data length is not multiple of 64 bytes == {}".format(len(dataView)))
    else:
        buf = 4 * numSamples
        samples = array.array("l" , buf)
        tempSamples= []
        numFrames = len(dataView)* 6
        current = 0
        start = 0
        firstData = 0
        lastValue = 0
     #-i, j

    for i in range(numFrames):
        tempSamples = extractSteim1Samples(dataView, i*64, littleEndian)   # returns only differences except for frame 0
        firstData = 0 # d(0) is byte 0 by default
        if i == 0:    # special case for first frame
            lastValue = bias # assign our X(-1)
            start = tempSamples[1]  # X(0) is byte 1 for frame 0
            firstData = 3 # d(0) is byte 3 for frame 0
        if (bias == 0):
            lastValue = start - tempSamples[3]  # X(-1) = X(0) - d(0)

    #for (j = firstData, j < len(tempSample) and current < numSamples):
    for j in range(firstData - len(tempSample)):
        samples[current] = lastValue + tempSamples[j]  # X(n) = X(n-1) + d(n)
        lastValue = samples[current]
        current = current + 1
        if current > numSamples:
            break

    samples = array.array(samples)
    if current != numSamples:
        raise Exception("Number of samples decompressed doesn't match number in header: {} != {}".format(current, numsamples))
    return samples

def decodeSteim2(temp, numSamples, swapBytes, bias):
    if ((len(temp) % 64) != 0):
        raise Exception("encoded data length is not multiple of 64 bytes ({})".format(len(temp)))
    else:
        buf = []
        samples = [buf]
        #tempSamples = []
        swapBytes ="?"
        numFrames = int( len(temp) / 64)
        current = 0
        start = 0
        firstData = 0
        lastValue = 0
        for i in range(numFrames):          #(i=0 i< numFrames  i + 1 )
            tempSamples = extractSteim2Samples('?', temp, i*64)   ## returns only differences except for frame 0
            firstData = 0 ## d(0) is byte 0 by default
            if i==0:    ## special case for first frame
                lastValue = bias ## assign our X(-1)
                print(tempSamples[0:4])
                start = tempSamples[0]  ## X(0) is byte 1 for frame 0
                firstData = 3 ## d(0) is byte 3 for frame 0
                if bias == 0:
                    lastValue = start - tempSamples[3]  ## X(-1) = X(0) - d(0)

        for j in range(firstData):
            if j < len(tempSamples) and current < numSamples:
                samples[current] = lastValue + tempSamples[j]  ## X(n) = X(n-1) + d(n)
                lastValue = samples[current]
                current = current + 1
            else:
                break

        samples = array.array(samples)
        if current != numSamples:
            raise Exception("Number of samples decompressed doesn't match number in header: {} != {}".format(current, numsamples))
        return samples

def extractSteim2Samples(swapBytes, temp, offset): #Int32Array
    nibbles = struct.unpack_from(swapBytes, temp, offset)
    if swapBytes:
        i32 = "<i"
        i16 = "<h"
        iUn = "<I"
    else:
       i32= ">i"
       i16 = ">h"
       iUn = "<I"
    nibbles = struct.unpack_from(i32, temp, offset)
    currNibble = 0
    swapBytes = "?"
    dnib = 0
    tempSamples = [0] * 106 #max 106 = 7 samples * 15 long words + 1 nibble int
    tempInt = []
    currNum = 0
    diffCount = 0  # number of differences
    bitSize = 0    # bit size
    headerSize = 0 # number of header/unused bits at top
    for i in range(16):
        currNibble = nibbles[0] >> (30 - i*2)
        currNibble = currNibble & 0x03
        if currNibble == 0:
            if (offset == 0):
                tempSamples[currNum + 1] = struct.unpack_from(i32, temp, offset+(i*4))[0]
                currNum = currNum + 1
        elif currNibble == 1:
            tempSamples[currNum + 1] = struct.unpack_from('b', temp, offset+(i*4))
            tempSamples[currNum + 2] = struct.unpack_from('b', temp, offset+(i*4)+1)
            tempSamples[currNum + 3] = struct.unpack_from('b', temp, offset+(i*4)+2)
            tempSamples[currNum + 4] = struct.unpack_from('b', temp, offset+(i*4)+3)
            currNum += 4
        elif currNibble == 2:
            tempInt = struct.unpack_from(i32, temp, offset+(i*4)) #, swapBytes)
            dnib = (tempInt >> 30) & 0x03
            if dnib == 1:
                temp[currNum + 1] = (tempInt << 2) >> 2
            elif dnib == 2:
                tempSamples[currNum + 1] = (tempInt << 2) >> 17  # d0
                tempSamples[currNum + 2] = (tempInt << 17) >> 17 # d1
            elif dnib == 3:
                tempSamples[currNum++] = (tempInt << 2) >> 22  # d0
                tempSamples[currNum++] = (tempInt << 12) >> 22 # d1
                tempSamples[currNum++] = (tempInt << 22) >> 22 # d2
                print('default')

        elif currNibble == 3:
            tempInt = struct.unpack_from(i32, temp, offset+(i*4))# swapBytes)
            dnib = (tempInt >> 30) & 0x03
            diffCount = 0  # number of differences
            bitSize = 0    # bit size
            headerSize = 0 # number of header/unused bits at top
            if dnib == 0:
                headerSize = 2
                diffCount = 5
                bitSize = 6
            elif dnib == 1:
                headerSize = 2
                diffCount = 6
                bitSize = 5
            elif dnib == 2:
                headerSize = 4
                diffCount = 7
                bitSize = 4
            else:
                print('Default')
            for i in range(diffCount - 1):
                if i == 0:
                    shiftForward = headerSize
                    shiftBack = headerSize + bitSize
                else:
                    shiftForward = headerSize + (1+i)*bitSize
                    shiftBack = shiftForward + bitSize
                tempSamples[currNum+i] = (tempInt << (headerSize+(1+i)*bitSize) >> (shiftForward + shiftBack)

        if (diffCount > 0):
            for d in range(diffCount):   # for-loop formulation
                tempSamples[currNum + 1] = ( tempInt << (headerSize+(d*bitSize)) ) >> (((diffCount-1)*bitSize) + headerSize)



    #samples = tempInt
    return tempSamples[0:currNum]



# turn the array stuff into a list or array of some sort, just you know, in like python language
# either A: make a array and fill it with however many zeros and the code "should" replace them
# B: make the whole thing a list and fill it with the information and then later turn it into an array
