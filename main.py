#!/usr/local/bin/python3

# this file will request for book info and write files
import os

class book:
    def __init__(self):
        infoList = ["bookName", "bookAuthor", "bookSeries", "seriesNumber"]
        print("Enter the bookName: ", end='')
        self.bookName = input()
        print("Enter the bookAuthor: ", end='')
        self.bookAuthor = input()
        print("Enter the bookSeries: ", end='')
        self.bookSeries = input()
        print("Enter the seriesNumber: ", end='')
        self.seriesNumber = input()
        while True:
            print("If page progression from left to right? [Y/n]", end='')
            progressionRes = input()
            if progressionRes == 'Y':
                self.rtl = True
                break
            elif progressionRes == 'n':
                self.rtl = False
                break
            else:
                continue
            
        #generate pages
        self.generatePages()

    def generatePages(self):
        #<p class="calibre1"><a id="p1"></a><img src="index-1_1.jpg" class="calibre2"/></p>
        pics = os.listdir("./pics")
        pics.sort()
        for num in range(1, len(pics)+1):
            f = open("./pages/page_" + "%003d"%num+ ".html", "w")
            f.write(r'<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>'+self.bookName+'</title><link type="text/css" rel="stylesheet" href="page_styles.css"/><link type="text/css" rel="stylesheet" href="stylesheet.css"/></head><body>')
            f.write('<p class="calibre1"><a id="p' + str(num) + '"></a><img src="'+ pics[num-1] +'" class="calibre2"/></p>')
            f.write("</body></html>")
            f.close()

    def createFiles(self):
        # create toc.ncx
        tocNCX = '''<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="ja">
<head>
  <meta name="dtb:uid" content="85b6b608-f62b-48ac-99d1-e3c7fa0769f0"/>
  <meta name="dtb:depth" content="2"/>
  <meta name="dtb:generator" content="calibre (5.18.0)"/>
  <meta name="dtb:totalPageCount" content="0"/>
  <meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle>
  <text>''' + self.bookName + '''</text>
</docTitle>
<navMap>
  <navPoint id="num_1" playOrder="1">
    <navLabel>
      <text>开始</text>
    </navLabel>
    <content src="titlepage.xhtml"/>
  </navPoint>
</navMap>
</ncx>
'''
        f = open("./res/toc.ncx", 'w')
        f.write(tocNCX)
        f.close()

        # create content.opf
        contentCONF_firstPart = '''<?xml version="1.0"  encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uuid_id">
  <metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata">
    <dc:title>''' + self.bookName + '''</dc:title>
    <dc:creator opf:role="aut" opf:file-as="'''+ self.bookAuthor +'''">'''+ self.bookAuthor + '''</dc:creator>
    <dc:contributor opf:role="bkp">calibre (5.18.0) [https://calibre-ebook.com]</dc:contributor>
    <meta name="calibre:series" content="'''+ self.bookSeries + '''"/>
    <meta name="calibre:series_index" content="'''+ self.seriesNumber + '''"/>
    <meta name="cover" content="cover"/>
    </metadata>
  <manifest>
    <item id="titlepage" href="titlepage.xhtml" media-type="application/xhtml+xml"/>'''

        contentCONF_secondPart = self.manifest() #pages and pictures toc.ncx stable files
        if self.rtl:
            contentCONF_thirdPart = '''</manifest>
  <spine toc="ncx">
    <itemref idref="titlepage"/>'''
        else:
            contentCONF_thirdPart = '''</manifest>
  <spine toc="ncx" page-progression-direction="rtl">
    <itemref idref="titlepage"/>'''
        
        contentCONF_fourthPart = self.spine()  # items for display
        contentCONF_fifthPart = '''  </spine>
  <guide>
    <reference type="cover" href="titlepage.xhtml" title="Cover"/>
  </guide>
</package>'''
        

        contentCONF = contentCONF_firstPart + contentCONF_secondPart + contentCONF_thirdPart + contentCONF_fourthPart + contentCONF_fifthPart
        f = open("./res/content.opf", 'w')
        f.write(contentCONF)
        f.close()

    def manifest(self):
        manifest = ''
        # input pages tags
        pages = os.listdir("./pages")
        pages.sort()
        self.pageNum = len(pages)
        for pageNum in range(1, len(pages)+1):
            manifest += '    ' + r'<item id="id'+str(10000+pageNum-1)+'" href="page_' +  "%003d"%(pageNum) + '.html" media-type="application/xhtml+xml"/>'

        # input regular tags
        manifest += '''<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="page_css" href="page_styles.css" media-type="text/css"/>
    <item id="css" href="stylesheet.css" media-type="text/css"/>
    <item id="cover" href="cover.jpeg" media-type="image/jpeg"/>\n'''

        # input pics
        pics = os.listdir("./pics")
        for pic in range(1, len(pics)+1):
            manifest += '    ' + r'<item id="id'+str(pic-1)+'" href="' + pics[pic-1] + '" media-type="image/jpeg"/>'

        return manifest

    def spine(self):
        spine = ''
        for page in range(1, self.pageNum+1):
            spine += '    ' + r'<itemref idref="id' + str(10000 + page - 1) + r'"/>'

        return spine



            
if __name__ ==  '__main__':
    b = book()
    b.createFiles()
