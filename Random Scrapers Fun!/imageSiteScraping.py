import requests, os, bs4, re

targetURL = 'http://85st.com/forum-36-6.html'
os.makedirs('85st6', exist_ok = True)

res = requests.get(targetURL)

res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")

threadElem = soup.select('.ptn a')

threadURL = []

for i in range(30):
    threadURL.append('http://85st.com/' + threadElem[i].get('href'))

for url in threadURL:
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    picElem = soup.select('.mbn.savephotop img')
    #####MY ADDITIONAL####
    print("Creating Folder...")
    #create a subfolder for this thread
        #getting variable folderName
    titleRegex = re.compile('meta name="keywords" content="(\w+)')
    titleMatch = titleRegex.search(res.text)
    title = titleMatch.group(1)

    dateReg = re.compile(r'((發表於 <span title=")|(發表於 ))(\d+-\d+-\d+)')
    dateMatch = dateReg.search(res.text)
    date = dateMatch.group(4)

    folderName = "[" + date + "]" + title

    # Create Folder within 85st
    print("Folder Created: %s..." % (folderName))
    os.makedirs('85st6/' + folderName, exist_ok = True)

    ################
    if picElem == []:
        print("Redefining Pic Element...")
        #for this site, some pages the images are stored
        #within <ignore_js_op> <img> element
        picElem = soup.select('ignore_js_op img')

        #download pictures and store in file
        for i in range(len(picElem)):
            picURL = 'http://85st.com/' + picElem[i].get('file')
            print('Downloading image %s...' % (picURL))
            res = requests.get(picURL)
            res.raise_for_status()

            imageFile = open(os.path.join('85st6',folderName, os.path.basename(picURL)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
    else:
        #for all the pictures in a single page
        for i in range(len(picElem)):
            picURL = 'http://85st.com/' + picElem[i].get('file')
            print('Downloading image %s...' % (picURL))
            res = requests.get(picURL)
            res.raise_for_status()

            imageFile = open(os.path.join('85st6',folderName, os.path.basename(picURL)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

print('Done.')
