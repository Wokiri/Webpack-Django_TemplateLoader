import os

headTag = '<head>'
djangoStatic = '{% load static %}'

forLINKstart = 'href="'

forSRCstart = 'src="'

data = ''

indexFile = os.path.join(os.getcwd(), 'prod', 'index.html')

if os.path.isfile(indexFile):
    oldIndex = open(indexFile, 'rt') #read the index file
    data = oldIndex.read() #read index contents to string
    oldIndex.close()
    
# Adds djangoStatic load
data = data.replace(headTag, headTag + djangoStatic)

tempData = data

def checkHTMLhref():
    global data
    global tempData
    
    hrefValStart = tempData[tempData.index(forLINKstart) + 6:]
    hrefVal = hrefValStart[:hrefValStart.index('"')]
    
    if ('https' in hrefVal or 'mailto' in hrefVal or '{% static' in hrefVal):
        cssLink = hrefVal
    else:
        cssLink = "{% static '" + hrefVal + "' %}"
    
    # Adjusts django hrefs reference
    data = data.replace(hrefVal, cssLink)
    
    tempData = hrefValStart
    
    while tempData.find(forLINKstart) != -1:
        checkHTMLhref()
        
    return data


data2 = checkHTMLhref()
tempData2 = data2

def checkHTMLsrc():
    global data2
    global tempData2
    
    srcStart = tempData2[tempData2.index(forSRCstart) + 5:]
    srcVal = srcStart[:srcStart.index('"')]
    
    if 'https' in srcVal or '{% static' in srcVal:
        src = srcVal
    else:
        src = "{% static '" + srcVal + "' %}"
    
    # Adjusts django hrefs reference
    data2 = data2.replace(srcVal, src)
    
    tempData2 = srcStart
    
    while tempData2.find(forSRCstart) != -1:
        checkHTMLsrc()
        
    return data2


# Open index.html again to write data
HTMLFile = open(indexFile, 'wt')
# Overide it with the formatted data
HTMLFile.write(checkHTMLsrc())
# close file
HTMLFile.close()
# print(checkHTMLsrc())

newIndexFile = os.path.join(os.getcwd(), 'prod', 'index.html')
if os.path.isfile(newIndexFile):
    print('Index HTML File updated successfully!')