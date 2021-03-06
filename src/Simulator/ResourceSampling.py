import pymongo as pm
import time, json
import SECRETS as config
import Database as db
import random as rnd
import traceback

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    sample = rnd.gauss(mean, sd)
    while (sample > upp or sample < low):
        sample = rnd.gauss(mean, sd)
    return sample
    
def sampleCPU(devid, time_int=0):
    """
        Sampling considering only the distribution variables
    """
    device = db.getDevice(devid)
    mean = device["distributions"]["CPU"][time_int]["mean"]
    deviation = device["distributions"]["CPU"][time_int]["deviation"]
    maxCPU = device["totalCPU"]
    return get_truncated_normal(mean=mean, sd=deviation, low=0, upp=maxCPU)

def sampleMEM(devid, time_int=0):
    """
        Sampling considering only the distribution variables
    """
    device = db.getDevice(devid)
    mean = device["distributions"]["MEM"][time_int]["mean"]
    deviation = device["distributions"]["MEM"][time_int]["deviation"]
    maxMEM = device["totalMEM"]
    return get_truncated_normal(mean=mean, sd=deviation, low=0, upp=maxMEM)

def sampleBusyCPU(devid, time=0):
    """
        Sampling considering the distribution and the used cpu by myapps
    """
    sampled = sampleCPU(devid, time)
    dev = db.getDevice(devid)
    return sampled - dev["usedCPU"] 

def sampleBusyMEM(devid, time=0):
    """
        Sampling considering the distribution and the used mem by myapps
    """
    sampled = sampleMEM(devid, time)
    dev = db.getDevice(devid)
    return sampled - dev["usedMEM"] 

def sampleMyAppStatus(devid, requestedCPU, requestedMEM, time_int=0):
    dev = db.getDevice(devid)
    sampledBusyCPU = sampleBusyCPU(devid, time_int)
    sampledBusyMEM = sampleBusyMEM(devid, time_int)
    # Computing the freeCPU as total-(sampled - myapp_itself) since myapp cpu is included in the "usedCPU from sampleFreeCPU"
    freeCPU = dev["totalCPU"] - (sampledBusyCPU - requestedCPU)
    freeMEM = dev["totalMEM"] - (sampledBusyMEM - requestedMEM)
    return {"hasCPU": freeCPU > requestedCPU, 
            "hasMEM": freeMEM > requestedMEM}
