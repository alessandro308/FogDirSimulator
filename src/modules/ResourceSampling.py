import pymongo as pm
import time, json
from scipy.stats import truncnorm 
import SECRETS as config
import Database as db

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(   (low - mean) / sd, 
                        (upp - mean) / sd, 
                        loc=mean, scale=sd
                    )

def sampleCPU(devid, time=0):
    """
        Sampling considering only the distribution variables
    """
    device = db.getDevice(devid)
    mean = device["distributions"]["CPU"][time]["mean"]
    deviation = device["distributions"]["CPU"][time]["deviation"]
    maxCPU = device["totalCPU"]
    return get_truncated_normal(mean=mean, sd=deviation, low=0, upp=maxCPU).rvs()

def sampleMEM(devid, time=0):
    """
        Sampling considering only the distribution variables
    """
    device = db.getDevice(devid)
    print device
    mean = device["distributions"]["MEM"][time]["mean"]
    deviation = device["distributions"]["MEM"][time]["deviation"]
    maxCPU = device["totalMEM"]
    return get_truncated_normal(mean=mean, sd=deviation, low=0, upp=maxCPU).rvs()

def sampleFreeCPU(devid, time=0):
    """
        Sampling considering the distribution and the used cpu by myapps
    """
    sampled = sampleCPU(devid, time)
    dev = db.getDevice(devid)
    return dev["usedCPU"] + sampled

def sampleFreeMEM(devid, time=0):
    """
        Sampling considering the distribution and the used mem by myapps
    """
    sampled = sampleMEM(devid, time)
    dev = db.getDevice(devid)
    return dev["usedMEM"] + sampled

def sampleMyAppStatus(devid, requestedCPU, requestedMEM, time=0):
    dev = db.getDevice(devid)
    sampledFreeCPU = sampleFreeCPU(devid, time)
    sampledFreeMEM = sampleFreeMEM(devid, time)
    # Computing the freeCPU as total-(sampled - myapp_itself) since myapp cpu is included in the "usedCPU from sampleFreeCPU"
    freeCPU = dev["totalCPU"] - (sampledFreeCPU - requestedCPU)
    freeMEM = dev["totalMEM"] - (sampledFreeMEM - requestedMEM)
    return {"hasCPU": freeCPU > requestedCPU, 
            "hasMEM": freeMEM > requestedMEM}