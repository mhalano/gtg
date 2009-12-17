# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Gettings Things Gnome! - a personal organizer for the GNOME desktop
# Copyright (c) 2008-2009 - Lionel Dricot & Bertrand Rousseau
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import os, xml.dom.minidom
import shutil
import sys

#This is for the awful pretty xml things
tab = "\t"
enter = "\n"
BACKUP_NBR = 7

#Those two functions are there only to be able to read prettyXML
#Source : http://yumenokaze.free.fr/?/Informatique/Snipplet/Python/cleandom       
def cleanDoc(document,indent="",newl=""):
    node = document.documentElement
    cleanNode(node,indent,newl)

def cleanNode(currentNode,indent,newl):
    myfilter = indent+newl
    if currentNode.hasChildNodes:
        for node in currentNode.childNodes:
            if node.nodeType == 3 :
                node.nodeValue = node.nodeValue.lstrip(myfilter).strip(myfilter)
                if node.nodeValue == "":
                    currentNode.removeChild(node)
        for node in currentNode.childNodes:
            cleanNode(node,indent,newl)

#This add a text node to the node parent. We don't return anything
#Because the doc object itself is modified.
def addTextNode(doc,parent,title,content) :
    if content :
        element = doc.createElement(title)
        parent.appendChild(element)
        element.appendChild(doc.createTextNode(content))
        
#This is a method to read the textnode of the XML
def readTextNode(node,title) :
    n = node.getElementsByTagName(title)
    if n and n[0].hasChildNodes() :
        content = n[0].childNodes[0].nodeValue
        if content :
            return content
    return None
            
#This function open an XML file if it exists and return the XML object
#If the file doesn't exist, it is created with an empty XML tree    
def openxmlfile(zefile,root ):
    try :
        if os.path.exists(zefile) :
            #We should be more defensive here
            doc = xml.dom.minidom.parse(zefile)
            cleanDoc(doc,tab,enter)
            #We should be more defensive here
            xmlproject = doc.getElementsByTagName(root)[0]
        #the file didn't exist, create it now
        else :
            doc,xmlproject = emptydoc(root)
            #then we create the file
            f = open(zefile, mode='a+')
            f.write(doc.toxml().encode("utf-8"))
            f.close()
        return doc,xmlproject
    except IOError, msg:
        print msg
        sys.exit(1)

#Return a doc element with only one root element of the name "root"
def emptydoc(root) :
    doc = xml.dom.minidom.Document()
    rootproject = doc.createElement(root)
    doc.appendChild(rootproject)
    return doc, rootproject
    
#write a XML doc to a file
def savexml(zefile,doc,backup=False) :
    f = open(zefile, mode='w+')
    pretty = doc.toprettyxml(tab,enter)
    if f and pretty:
        f.write(pretty.encode("utf-8"))
        f.close()
        if backup :
            #We will now backup the file
            backup_nbr = BACKUP_NBR
            #We keep BACKUP_NBR versions of the file
            #The 0 is the youngest one
            while backup_nbr > 0 :
                older = "%s.bak.%s" %(zefile,backup_nbr)
                backup_nbr -= 1
                newer = "%s.bak.%s" %(zefile,backup_nbr)
                if os.path.exists(newer) :
                    shutil.move(newer,older)
            #The bak.0 is always a fresh copy of the closed file
            #So that it's not touched in case of bad opening next time
            current = "%s.bak.0" %(zefile)
            shutil.copy(zefile,current)
    else:
        print "no file %s or no pretty xml"%zefile