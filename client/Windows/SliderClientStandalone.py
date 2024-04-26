# WINDOWS VERSION

import subprocess
import schedule

import os
import time

# the 4 fixed square resolution levels
fixedImgRes = [1376, 2752, 5504, 11008]

# calculate the crop values based on x y positions of where you want the photo to be
# x and y have a max 256
def calculateOnOrigin(monitorResolution, posx, posy, scalefactor):
    
    targetArea = monitorResolution[0] * monitorResolution[1]    
    croppedArea = 0 
    resultFactor = 0
    
    # pick the correct resolution level to grab image
    while croppedArea <= targetArea:
        croppedArea = fixedImgRes[resultFactor] * fixedImgRes[resultFactor]
        #print(croppedArea, targetArea)
        resultFactor += 1
        if resultFactor >= 4:
            break
            
    # lets now convery x & y coords to x, xx, y, yy crops for slider
    locStep = fixedImgRes[resultFactor] / scalefactor # square image, dont need to account for height
    xCenterStep = locStep * posx
    yCenterStep = locStep * posy
    halfx = monitorResolution[0] / 2 
    halfy = monitorResolution[1] / 2

    x = xCenterStep - halfx
    xx = xCenterStep + halfx
    y = yCenterStep - halfy 
    yy = yCenterStep + halfy

    # we need to filter out neg values
    negs = [x, xx, y, yy]
    notneg = []

    for num in negs:
        if num <=0:
            notneg.append(1)
        else:
            notneg.append(int(num))

    return [resultFactor + 1, notneg[0], notneg[2], notneg[1], notneg[3]]


#sliderres =  calculateOnOrigin([1290, 2796], 150, 167, 256) # iphone
#sliderres =  calculateOnOrigin([1920, 1080], 113, 187, 256) # 1080p AU
#sliderres =  calculateOnOrigin([2560, 1440], 113, 187, 256) # 2k AU
sliderres =  calculateOnOrigin([3440, 1440], 113, 187, 256) # ultrawide AU
#sliderres =  calculateOnOrigin([3840, 2160], 113, 187, 256) # 4k AU

# we need to clamp the storm resolution as himawari has a max of 3
sResMax = sliderres[0]
if sliderres[0] > 3:
    sResMax = 3

sliderArgsGeo = [
    "slider-cli.exe",
    "--satellite=himawari",
    "--sector=full-disk",
    "--product=geocolor", # geocolor cira-atmosphere-rgb
    "-i",
    "1",
    "-z",
    f"{sliderres[0]}",
    #"-v", # verbose for debug
    "-f",
    "png",
    #"-b=20231214225000", # timestamp
    f"--crop={sliderres[1]},{sliderres[2]},{sliderres[3]},{sliderres[4]}"
]

sliderArgsRGB = [
    "slider-cli.exe",
    "--satellite=himawari",
    "--sector=full-disk",
    "--product=cira-atmosphere-rgb", # geocolor cira-atmosphere-rgb
    "-i",
    "1",
    "-z",
    f"{sliderres[0]}",
    #"-v", # verbose for debug
    "-f",
    "png",
    #"-b=20231217082000", 
    f"--crop={sliderres[1]},{sliderres[2]},{sliderres[3]},{sliderres[4]}"
]

sliderArgsStorm = [
    "slider-cli.exe",
    "--satellite=himawari",
    "--sector=full-disk",
    "--product=band-16",
    "-i",
    "1",
    "-z",
    f"{sResMax}", # we apply the clamped value here
    #"-v", # verbose for debug
    "-f",
    "png",
    #"-b=20231214225000",
    f"--crop={sliderres[1]},{sliderres[2]},{sliderres[3]},{sliderres[4]}"
]


def mainExec():
    #print(sliderArgsRGB, sliderArgsStorm)
    subprocess.call(sliderArgsRGB)
    print("Gathered latest RGB image")
    subprocess.call(sliderArgsStorm)
    print("Gathered latest Storm Image")
    os.popen("merge.bat")
    print("Merge completed")


mainExec()

