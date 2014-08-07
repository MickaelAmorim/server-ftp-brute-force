__author__ = 'oxa'

from time import gmtime, strftime


#Function qui génère du log
def tolog(message,level):
    date = strftime("[%d/%m/%Y] %H:%M:%S", gmtime())
    with open("log.txt","a") as myfile:
        myfile.write("["+level+"] "+date+" <> "+message+"\n")
    myfile.close()


def tologbrute(message,level):
    date = strftime("[%d/%m/%Y] %H:%M:%S", gmtime())
    with open("logbrute.txt","a") as myfile:
        myfile.write("["+level+"] "+date+" <> "+message+"\n")
    myfile.close()