#!/usr/bin/env python
#https://raw.githubusercontent.com/dwyl/english-words/master/words2.txt
import urllib2
class FileDownloader(object):
    def __init__(self,url, output=False):
        self.url = url
        self.output = output
    def Url(self):
        return self.url
    def DownloadUrl(self, filename, url=None, block_size=8192):        
        if url is None:
            url = self.url
        url = self.url
        u = urllib2.urlopen(self.url)
        f = open(filename,'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        if self.output:
            print "Downloading: '{0}' from '{1}'' Size: '{2}''".format(filename, url, file_size)
        file_size_dl = 0
        while True:
            buffer = u.read(block_size)
            if not buffer:
                break #download completed
            file_size_dl += len(buffer)
            f.write(buffer)
            if self.output:
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,
        f.close()
