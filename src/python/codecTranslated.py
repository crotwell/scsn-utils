from array import array
import struct
import math
import numpy as np

class EncodedDataSegment:
    def __init__(samples, tempSamples, numFrames, current, start, firstData, lastValue):
        buf = 4 * numSamples
        samples = []
        tempSamples
        numFrames = len(dataView) / 64
        current = 0
        start = 0
        firstData = 0
        lastValue = 0

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
    temp = []   4 * samples ## 16 longwords, can't be more than 64
    currNum = 0

    for i in range(16):   #  i is the word number of the frame starting at 0
        currNibble = (nibbles >>> (30 - i*2 ) ) & 0x03
        currNibble = (nibbles >> (30 - i*2) ) & 0x03

        def case(currNibble):
            if currNibble == 0:
                offset == 0
                temp[currNum + 1] = struct.unpack_from(i32, dataView, offset+(i*4))
                break

            elif currNibble == 1:
                for n in range(4):
                    temp[currNum] = struct.unpack_format(dataView, offset+(i*4)+n)
                    currNum + 1
                    break
            elif currNibble == 2:
                for n in range(4):
                    temp[currNum] = struct.unpack_format(i16, dataView, offset+(i*4)+n)
                    currNum + 1
                    break
            elif currNibble == 3:
                temp[currNum + 1] =struct.unpack_format(i16, dataView, offset+(i*4))
                break
            else:
                raise expection(("unreachable case:==".format(currNibble))

            return temp

#################
def decodeSteim1(dataView: DataView, numSamples: number, littleEndian: boolean, bias: number): #Int32Array
    if (len(dataView) *% 64 != 0):
        print( "encoded data length is not multiple of 64 bytes ==".format(len(dataView)))
        raise Exception:

    elif:
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

    samples = np.array(samples)
    if current != numSamples:
        raise exception("Number of samples decompressed doesn't match number in header: {} != {}".format(current, numsamples))
    return samples

def decodeSteim2(dataView, numSamples, swapBytes, bias):
    if (len(dataView) % 64 != 0):
        raise exception("encoded data length is not multiple of 64 bytes ({})".format(len(dataView)))
    buf = []
    samples = new Int32Array(buf)
    tempSamples = []
    swapBytes = "?"
    numFrames = len(dataView) / 64
    current = 0
    start = 0
    firstData = 0
    lastValue = 0

    for i in range(numFrames):          #(i=0 i< numFrames  i + 1 )
        tempSamples = extractSteim2Samples(dataView, i*64, swapBytes)   ## returns only differences except for frame 0
        firstData = 0 ## d(0) is byte 0 by default
        if i==0:    ## special case for first frame
            lastValue = bias ## assign our X(-1)
            start = tempSamples[1]  ## X(0) is byte 1 for frame 0
            firstData = 3 ## d(0) is byte 3 for frame 0
            if bias == 0:
                lastValue = start - tempSamples[3]  ## X(-1) = X(0) - d(0)

    for j in firstData:
        if j < len(tempSamples) and current < numSamples:
            samples[current] = lastValue + tempSamples[j]  ## X(n) = X(n-1) + d(n)
            lastValue = samples[current]
            current = current + 1
        elif:
            break

    samples = np.array(samples)
    if current != numSamples:
        raise exception("Number of samples decompressed doesn't match number in header: {} != {}".format(current, numsamples))
    return samples

def extractSteim2Samples(dataView, offset, swapBytes): #Int32Array
    currNibble = 0
    swapBytes = "?"
    dnib = 0
    temp = []#array. ##* max 106 = 7 samples ## 15 long words  + 1 nibble int
    tempInt = []
    currNum = 0
    diffCount = 0  ## number of differences
    bitSize = 0    ## bit size
    headerSize = 0 ## number of header/unused bits at top
    for i in range 16:
        currNibble = (nibbles >> (30 - i*2 ) ) & 0x03
        if currNibble == 0  and offset == 0:
            temp[currNum + 1] = struct.unpack_format(i32, dataView, offset+(i*4))#, swapBytes)
            break
    elif currNibble == 1:
        temp[currNum + 1] = struct.unpack_format(dataView, offset+(i*4))
        temp[currNum + 1] = struct.unpack_format(dataView, offset+(i*4)+1)
        temp[currNum + 1] = struct.unpack_format(dataView, offset+(i*4)+2)
        temp[currNum + 1] = struct.unpack_format(dataView, offset+(i*4)+3)
        break
    elif currNibble == 2:
        tempInt = struct.unpack_format(i32, dataView, offset+(i*4))#, swapBytes)
        dnib = (tempInt >> 30) & 0x03
        if dnib == 1:
            temp[currNum + 1] = (tempInt << 2) >> 2
            break
        elif dnib == 2:
            temp[currNum + 1] = (tempInt << 2) >> 17  ## d0
            temp[currNum + 1] = (tempInt << 17) >> 17 ## d1
            break
        elif dnib == 3:
            temp[currNum + 1] = (tempInt << 2) >> 22  ## d0
            temp[currNum + 1] = (tempInt << 12) >> 22 ## d1
            temp[currNum + 1] = (tempInt << 22) >> 22 ## d2
            break

      break
    elif currNibble == 3:
        tempInt = struct.unpack_format(i32, dataView, offset+(i*4), swapBytes)
        dnib = (tempInt >> 30) & 0x03
        diffCount = 0  ## number of differences
        bitSize = 0    ## bit size
        headerSize = 0 ## number of header/unused bits at top
        if dnib == 0:
            headerSize = 2
            diffCount = 5
            bitSize = 6
            break
        elif dnib == 1:
            headerSize = 2
            diffCount = 6
            bitSize = 5
            break
        elif dnib ==2:
            headerSize = 4
            diffCount = 7
            bitSize = 4
            break

        if diffCount > 0:
            for d in range diffCount:
            temp[currNum + 1] = ( tempInt << (headerSize+(d*bitSize)) ) >> (((diffCount-1)*bitSize) + headerSize
    temp = np.array(temp)
    return temp(0, currNum)   #temp.slice(0, currNum)



  ############################

def decodeSteim2(dataView, numSamples, swapBytes, bias):
    bias = number
    swapBytes = boolean
    if (len(dataView) % 64 != 0)
        throw new CodecException("encoded data length is not multiple of 64 bytes {}".format(len(dataView)))

    buf = new ArrayBuffer(4 * numSamples)
    samples = new Int32Array(buf)
    tempSamples
    numFrames = len(dataView) / 64
    current = 0
    start = 0
    firstData = 0
    lastValue = 0

    for i in numFrames:
        tempSamples = extractSteim2Samples(dataView, i*64, swapBytes)   # returns only differences except for frame 0
        firstData = 0 # d(0) is byte 0 by default
        if i == 0:    # special case for first frame
        # console.log("i==0, special case for first frame")
            lastValue = bias # assign our X(-1)
        # x0 and xn are in 1 and 2 spots
            start = tempSamples[1]  # X(0) is byte 1 for frame 0
        # end = tempSamples[2]    # X(n) is byte 2 for frame 0
            firstData = 3 # d(0) is byte 3 for frame 0
            if bias == 0:
                lastValue = start - tempSamples[3]:  # X(-1) = X(0) - d(0)

        for j in range(- len(tempSamples)):
            samples[current] = lastValue + tempSamples[j]  # X(n) = X(n-1) + d(n)
            lastValue = samples[current]d
            current = current + 1
             if current > numSamples:
                 break

    if current != numSamples:
        raise Exception:
            print("Number of samples decompressed doesn't match number in header: {} !={} ".format(numSamples, current))
        return numSamples

def extractSteim2Samples(dataView, offset, swapBytes): #Int32Array
    nibbles = struct.unpack_format(iUn, dataView, offset, swapBytes)
    currNibble = 0
    swapBytes = "?"
    dnib = 0
    temp = [] #max 106 = 7 samples * 15 long words + 1 nibble int
    tempInt
    currNum = 0
    diffCount = 0  # number of differences
    bitSize = 0    # bit size
    headerSize = 0 # number of header/unused bits at top
    for i in range(16):
        currNibble = (nibbles >> (30 - i*2 ) ) & 0x03
        if currNibble == 0:
            if (offset == 0):
                temp[currNum + 1] = struct.unpack_format(i32, dataView, offset+(i*4))# swapBytes)
                break
        elif currNibble == 1:
            temp[currNum + 1] = struct.unpack_format(dataView, offset+(i*4))
            temp[currNum + 1] = struct.unpack_format(dataView, offset+(i*4)+1)
            temp[currNum + 1] = struct.unpack_format(dataView, offset+(i*4)+2)
            temp[currNum + 1] = struct.unpack_format(dataView, offset+(i*4)+3)
            break
        elif currNibble == 2:
            tempInt = struct.unpack_format(iUn, dataView, offset+(i*4)) #, swapBytes)
            dnib = (tempInt >> 30) & 0x03
            if dnib == 1:
                temp[currNum + 1] = (tempInt << 2) >> 2
                break
            elif dnib == 2:
                temp[currNum + 1] = (tempInt << 2) >> 17  # d0
                temp[currNum + 1] = (tempInt << 17) >> 17 # d1
                break
            elif dnib == 3:
                temp[currNum + 1] = (tempInt << 2) >> 22  # d0
                temp[currNum + 1] = (tempInt << 12) >> 22 # d1
                temp[currNum + 1] = (tempInt << 22) >> 22 # d2
                break
                #default:

            break
        elif currNibble == 3:
            tempInt = struct.unpack_format(iUn, dataView, offset+(i*4))# swapBytes)
            dnib = (tempInt >> 30) & 0x03
            diffCount = 0  # number of differences
            bitSize = 0    # bit size
            headerSize = 0 # number of header/unused bits at top
            if dnib == 0:
                headerSize = 2
                diffCount = 5
                bitSize = 6
                break
            elif dnib == 1:
                headerSize = 2
                diffCount = 6
                bitSize = 5
                break
            elif dnib == 2:
                headerSize = 4
                diffCount = 7
                bitSize = 4
                break
                #default:

        if (diffCount > 0)
            for d in range diffCount:   # for-loop formulation
                temp[currNum + 1] = ( tempInt << (headerSize+(d*bitSize)) ) >> (((diffCount-1)*bitSize) + headerSize)



    temp = np.array(temp)
    return temp["l", temp]



# turn the array stuff into a list or array of some sort, just you know, in like python language
# either A: make a array and fill it with however many zeros and the code "should" replace them
# B: make the whole thing a list and fill it with the information and then later turn it into an array
