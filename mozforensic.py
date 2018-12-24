import re
import optparse
import os
import sqlite3

#get all downloaded files from firefox
def Downloads(downloadDB):
    conn = sqlite3.conncet(downloadDB)
    c =  conn.cursor()
    c.execute("SELECT name, source, datetime(endtime/1000000, 'unixpoch' FROM moz_downloads;")
    print("[*] Files Downloaded---")
    for row in c:
        print("[+] File: {} from source: {} at: {}".format(row[0], row[1], row[2]))

#get cookies to authenticate to site visited by the user
def Cookies(cookieDB):
    conn = sqlite3.connect(cookieDB)
    c = conn.cursor()
    c.execute("SELECT host, name, value FROM moz_cookies;")
    print("[*]Cookies found...")
    for row in c:
        host = str(row[0])
        name = str(row[1])
        value = str(row[2])
        print("[+] Host: {} Cookie: {} Value: {}".format(host,name,value))

#get the browser general history
def History(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    c.execute("SELECT url, datetime(visit_date/1000000, 'unixepoch') FROM moz_places, moz_historyvisits WHERE visit_count > 0 AND moz_places.id == moz_historyvisits.id;")
    print("[*] History Found...")
    for row in c:
        url = str(row[0])
        date = str(row[1])
        print("[+] Date {} Visited {}".format(date, url))


#get the words the user searched using google
def Google(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    c.execute("SELECT url, datetime(visit_date/1000000, 'unixepoch') FROM moz_places, moz_historyvisits WHERE visit_count > 0 AND moz_places.id == moz_historyvisits.id;")
    for row in c:
        url = str(row[0])
        date = str(row[1])

        if 'google' in url.lower():
            r = re.findall(r'q=.*\&', url)
            if r:
                search = r[0].split('&')[0]
                search=search.replace('q=', '').replace('+', ' ')
                print('[+] '+date+' Searched For: ' + search)

def main():
    parser = optparse.OptionParser("usage%prog " + "-p <firefox profile path> ")
    parser.add_option('-p', dest='pathName', type='string', help='specify skype profile path')
    (options, args) = parser.parse_args()
    pathName = options.pathName
    if pathName == None:
        print(parser.usage)
        exit(0)
    elif os.path.isdir(pathName) == False:
        print('[!] Path Does Not Exist: ' + pathName)
        exit(0)
    else:
        downloadDB = os.path.join(pathName, 'downloads.sqlite')
        if os.path.isfile(downloadDB):
            Downloads(downloadDB)
        else:
            print('[!] Downloads Db does not exist: '+downloadDB)
        cookiesDB = os.path.join(pathName, 'cookies.sqlite')
        if os.path.isfile(cookiesDB):
            Cookies(cookiesDB)
        else:
            print('[!] Cookies Db does not exist:' + cookiesDB)
        placesDB = os.path.join(pathName, 'places.sqlite')
        if os.path.isfile(placesDB):
            History(placesDB)
            Google(placesDB)
        else:
            print('[!] PlacesDb does not exist: ' + placesDB)


if __name__ == '__main__':
    main()
