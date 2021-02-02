from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from pytube import YouTube

import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import threading

Folder_Name = ""
T=False

def openLocation():
    global Folder_Name
    Folder_Name = filedialog.askdirectory()
    locationError.config(text=Folder_Name,fg="green")
    
def update_status(vid,no): 
    download_status.config(text="Status :: %d/%d downloading"%(vid,no))

def download(url,ID,choice):

    yt = YouTube(url)
    if(choice == choices[0]):
        select = yt.streams.filter(progressive=True).first()
    else:
        select = yt.streams.filter(progressive=True).last() 
        
    select.download(Folder_Name,filename=str(ID)) 

def DownloadVideos():
    global Folder_Name
    global T
    if(len(Folder_Name)<1):
        locationError.config(text="Please Choose Folder",fg="red")
        return
    payload = {"Gender":"All","MacAddress":"b8:27:eb:45:c7:21","Location":"","Business":"","Age":""}
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    r=session.post('http://smartgsc.rannlabprojects.com/api/CMS/SearchAdvertisement',data=payload)
    r_dict = json.loads(r.json())

    choice = ytdchoices.get()
    
    vid=0
    no=len(r_dict)
    download_status.config(text="Download started")
    for v_dict in r_dict:
        t1 = threading.Thread(target=download, args=(v_dict["VideoUrl"],v_dict["ID"],choice))
        t1.start()
        t2 = threading.Thread(target=update_status, args=(vid,no))
        t2.start()
        t1.join()
        t2.join()

        vid+=1
    T=False    
    download_status.config(text="download completed!!!") 
       

def DownloadVideosThread():
    global T
    t=threading.Thread(target=DownloadVideos) 
    T=True
    t.start()        


root=Tk()
root.title("YTD Downloader")
root.geometry("350x400")
root.columnconfigure(0,weight=1)

saveLabel = Label(root,text="Save The Video File To",font=("jost",15,"bold"))
saveLabel.grid()

saveEntry = Button(root,width=10,bg="red",fg="white",text="Choose path",command=openLocation)
saveEntry.grid()

locationError = Label(root,text=" ",fg="red",font=("jost",10))
locationError.grid()

ytdQuality = Label(root,text="Select Quality",font=("jost",15))
ytdQuality.grid()

choices = ["720p","144p"]
ytdchoices = ttk.Combobox(root,values=choices)
ytdchoices.grid()

ytdempty = Label(root,text=" ",font=("jost",15))
ytdempty.grid()

downloadbtn = Button(root,text="Start Download",width=15,bg="red",fg="white",command=DownloadVideosThread)
downloadbtn.grid()

download_status = Label(root,text="Status :: ",font=("jost",15,"bold"))
download_status.grid()

ThreadError = Label(root,text=" ",fg="red",font=("jost",10))
ThreadError.grid()

download_status.config(text=" ")

def on_closing():
    if(T):
        ThreadError.config(text="cant close until download is finished")
    else:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()