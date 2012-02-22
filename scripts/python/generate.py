#!/usr/bin/python

import io, os, sys, time
from jinja2 import Template

class Generate(object):
    def __init__(self, templateFile, contentBase, publishBase):
        templateFileHandle = io.open(templateFile)
        templateLines = templateFileHandle.readlines()
        templateContent = ' '.join(templateLines)
        templateFileHandle.close()
        self.template = Template(templateContent)
        self.contentBase = contentBase
        self.publishBase = publishBase

    def __getSortedDirList(self, d):
        l = os.listdir(d)
        l.sort()
        return l

    def __getSortedFileList(self, d):
        l = [(x, os.path.getmtime(d + '/' + x)) for x in os.listdir(d)]
        l.sort(key = lambda x: x[1])
        self.latestUpdateMTime = time.ctime(l[-1][1])
        return [x[0] for x in l]

    def __getContent(self):
        dirList = self.__getSortedDirList(self.contentBase)
        filesDict = dict()
        for d in dirList:
            files = self.__getSortedFileList(self.contentBase + '/' + d) 
            filesDict[d] = filter(lambda x: x.endswith('txt'), files)
        return filesDict

    def __getContentPath(self, d, f):
        return self.contentBase + '/' + d + '/' + f

    def __getWebPath(self, f):
        filename = f.split('/')[-1]
        filenameWithoutExt = ''.join(filename.split('.')[:-1])
        return filenameWithoutExt.lower() + '.html'

    def __getPublishPath(self, f):
        return self.publishBase + '/' + self.__getWebPath(f)

    def __getCleanedUpTitle(self, f):
        f2 = f.replace('_', ' ')
        return ''.join(f2.split('.')[:-1])

    def __getFileMTime(self, f):
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(f)
        return "%s" % time.ctime(mtime)

    def run(self):
        # gather all input content
        filesDict = self.__getContent()
        dirs = filesDict.keys()
        dirs.sort()
        # this holds the mapping from a section to its "default" page
        # (which loads when the section name is clicked)
        defaultLinks = dict()
        for d in dirs:
            defaultLinks[d] = self.__getWebPath(filesDict[d][0]) # just use the "first" link
        for currentDir in dirs:
            inFilePaths  = [self.__getContentPath(currentDir, f) for f in filesDict[currentDir]]
            outFilePaths = [self.__getPublishPath(f) for f in filesDict[currentDir]]
            fileWebPaths = [self.__getWebPath(f) for f in filesDict[currentDir]]
            inFileTitles = [self.__getCleanedUpTitle(f) for f in filesDict[currentDir]]
            for idx in range(len(inFilePaths)):
                inFilePath = inFilePaths[idx]
                inFileTitle = inFileTitles[idx]
                if idx > 0:
                    prevFileTitle = inFileTitles[idx - 1]
                    prevFileWebPath = fileWebPaths[idx - 1]
                else:
                    prevFileTitle = None
                    prevFileWebPath = None
                if idx < len(inFileTitles) - 1:
                    nextFileTitle = inFileTitles[idx + 1]
                    nextFileWebPath = fileWebPaths[idx + 1]
                else:
                    nextFileTitle = None
                    nextFileWebPath = None
                outFilePath = outFilePaths[idx]
                print('%s --> %s' % (inFilePath, outFilePath))
                inFile = io.open(inFilePath, 'r')
                inFileMTime = self.__getFileMTime(inFilePath)
                outFile = io.open(outFilePath, 'w')
                inFileLines = [x.rstrip('\n') for x in inFile.readlines()]
                result = self.template.render(topMenu          = dirs,
                                              sectionLinksDict = defaultLinks,
                                              currentSection   = currentDir,
                                              sideMenu         = zip(inFileTitles, fileWebPaths),
                                              currentTitle     = inFileTitle,
                                              contentMTime     = inFileMTime,
                                              contentLines     = inFileLines,
                                              prevPageTitle    = prevFileTitle,
                                              prevPagePath     = prevFileWebPath,
                                              nextPageTitle    = nextFileTitle,
                                              nextPagePath     = nextFileWebPath,
                                              siteMTime        = self.latestUpdateMTime)
                outFile.write(result)
                outFile.close()
                inFile.close()

templateFile = sys.argv[1]
contentBase = sys.argv[2]
publishBase = sys.argv[3]
g = Generate(templateFile, contentBase, publishBase)
g.run()

