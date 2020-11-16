import os

headTag = '<head>'
djangoStatic = '{% load static %}'

forLINKstart = 'href="'

forSRCstart = 'src="'

data = ''
# Call for user values
userHTMLValue = input("Name of the HTML document (include '.html'): \n")

htmlFile = os.path.join(os.getcwd(), 'prod', userHTMLValue)

if os.path.isfile(htmlFile):
    print(f'{htmlFile} file found')
    oldhtmlFile = open(htmlFile, 'rt') #read the index file
    data = oldhtmlFile.read() #read index contents to string
    oldhtmlFile.close()
else:
    print(f'{htmlFile} file NOT found')
    quit()
    
# Adds djangoStatic load
if data.find(djangoStatic) == -1:
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
newHTMLFile = open(htmlFile, 'wt')
# Overide it with the formatted data
newHTMLFile.write(checkHTMLsrc())
# close file
newHTMLFile.close()
# print(checkHTMLsrc())


if os.path.isfile(htmlFile):
    print('HTML File updated successfully!')