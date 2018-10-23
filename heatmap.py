import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import ImageTk,Image  
import time
import serial
import csv
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import shutil


BAUDRATE= 9600
SerialportPIC1="COM6"
SerialportPIC2="COM3"
    #Iniciar puerto Serial con la creación de un objeto de la clase Serial:
PIC1=serial.Serial(SerialportPIC1, BAUDRATE)
#PIC2=serial.Serial(SerialportPIC2, BAUDRATE)
#"""


#C:\Users\ADMIN\Desktop
class mclass:
    #def getData():
    def __init__(self,  window):
        self.window = window
        window.config(background='white')
        window.title("Estacio de Calidad de Mateado")
        pad=3
        window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth()-pad, window.winfo_screenheight()-pad))
        #Titulo
        box = Label(self.window,text="CONTROL DE CALIDAD DEL PROCESO DE MATEADO", bg='white', font=("Helvetica", 28))
        box.place(x=120, y=10)
        #Logo Vitro
        Estado=Label(self.window, text="Estado del sistema: ", background="white", font=("Helvetica",20))
        Estado.place(x=740, y=200)
        
        Uniformidad=Label(self.window, text="Uniformidad del mateado del Vidrio: ", background="white", font=("Helvetica",20))
        Uniformidad.place(x=740, y=280)
        
        Calidad=Label(self.window, text="Grado de Calidad: ", background="white", font=("Helvetica",20))     
        Calidad.place(x=740, y=360)
        
        self.logo=ImageTk.PhotoImage(Image.open("Vitro.png")) 
        logoLy=Label(self.window, image=self.logo)
        logoLy.place(x=1100,y=0)

        
    def plot (self, data, LblEstado):
        LblEstado.configure(text="Graficando")
        self.fig, self.ax = plt.subplots(figsize=(9.5,9.5))
        sns.heatmap(data, cmap='Blues',vmax=100, vmin=0, xticklabels=False, yticklabels=False, ax=self.ax, cbar_kws={'label': '% DE TRANSPARENCIA'})      
        canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        canvas.get_tk_widget().place(x=50, y=50)
        canvas.draw()
        self.window.update()
        
    def unplot(self):
        self.ax.clear()
        self.window.update()
        #imgcanvas=Canvas.
        
def crearCSV():
    fecha=datetime.date(datetime.now())
    Reporte='Reporte'+fecha.strftime('%d-%m-%Y')+".csv"
    Titulo=["VITRO", "Reporte de proceso de mateado"]
    Tit2=["Fecha:", datetime.now().strftime('%c')]
    blank=[" ", " "]
    formato=["Calidad:","Uniformidad", "Hora:"]
    with open(Reporte, 'w', newline='') as csvFile:
        Repo = csv.writer(csvFile)
        Repo.writerow(Titulo)
        Repo.writerow(Tit2)
        Repo.writerow(blank)
        Repo.writerow(formato)
        
def add2CSV(info):
    fecha=datetime.date(datetime.now())
    Reporte='Reporte'+fecha.strftime('%d-%m-%Y')+".csv"
    tiempo= datetime.time(datetime.now())
    row=[info[0], info[1], tiempo.strftime('%H:%M:%S')]
    with open(Reporte, 'a', newline='') as csvFile:
        Repo = csv.writer(csvFile)
        Repo.writerow(row) 
#Creacion de ventana
def degQlty(window, texto):
    if texto=="A":
        fg="green"
        
    if texto=="B":
        fg="yellow"
        
    if texto=="C":
        fg="red"
    Qlty=Label(window, text=texto, background="white", fg=fg, font=("Helvetica",50))
    Qlty.place(x=1000, y=340)
    window.update()
    return Qlty

def quitLabel(Label, LblCalidad):
    Label.place_forget()  
    LblCalidad.place_forget()
    
def getdata(LblEstado):
    Datos=[]
    Vidrio=np.array([])   
    Linea=serialRead()
    LblEstado.configure(text="Leyendo Sensores")
    window.update()
    while np.mean(Linea)>50:     
        Linea=serialRead()
        window.update()
        print(np.mean(Linea))
    
    Vidrio=np.append(Vidrio,Datos)
    for x in range(1,37):
        Datos=serialRead()
        Vidrio=np.append(Vidrio,Datos)
        
    Vidrio=np.reshape(Vidrio, (26,36))
    #data=np.random.rand(26,36)*100
    return Vidrio
    
    
"""PIC1, PIC2"""
def serialRead():
    
    """
    data=[]
    sensores=[]
    Lectura=""
    Lectura2=""
    PIC1.write(b'R')
    Lectura=PIC1.readline()
    sensores=Lectura.split(" ")
    np.append(data, sensores)
    sensores=[]
    PIC2.write(b'R')
    Lectura2=PIC2.readline()
    sensores=Lectura2.split(" ")
    np.append(data,sensores)
    """
    data=np.random.randint(0,101,size=(1,26))
    return data


def detQlty(data,LblCalidad):
    Uniformidad= np.std(data)
    UniformidadTxt="{0:.2f}".format(Uniformidad)
    LblCalidad.configure(text=UniformidadTxt)
    LblUnif.place(x=1180, y=280)
    window.update()
    #print(suma)
    print(Uniformidad)
    if Uniformidad>50:
        return ["C", UniformidadTxt]
    elif Uniformidad>30:
        return ["B", UniformidadTxt]
    else:
        return ["A", UniformidadTxt]
    
    
def mainloop():
    global LblUnif
    global LblEstado
    crearCSV()
    Inicio.configure(text="Finalizar", command=finalizar)
    while True:
        window.update()
        lbl=""
        data=getdata(LblEstado)
        lbl=detQlty(data, LblUnif)
        Qlty=degQlty(window, lbl[0])
        add2CSV(lbl)
        start.plot(data, LblEstado)
        time.sleep(.5)
        start.unplot()
        quitLabel(Qlty, LblUnif)
        time.sleep(.5)


def exportarReporte():
    global LblEstado
    LblEstado.configure(text="Exportando reporte")
    window.update()
    fecha=datetime.date(datetime.now())
    Reporte='Reporte'+fecha.strftime('%d-%m-%Y')+".csv"
    emailfrom = "alberto.herrera@udem.edu"
    emailto = "alberto.herrera@udem.edu"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = 'Reporte'+fecha.strftime('%d-%m-%Y')
    filename = Reporte
    attachment = open(Reporte, "rb")
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()   
    server.login(emailfrom, "jasiel1996")
    text = msg.as_string()
    server.sendmail(emailfrom, emailto, text)
    server.quit()
    attachment.close()
    shutil.move(Reporte, "C:\\Users\\ADMIN\\Desktop\\oldreports")


def finalizar():
    global window
    #exportarReporte()
    global LblEstado
    LblEstado.configure(text="Finalizando")
    window.update()
    time.sleep(2)
    window.destroy()
    exit()
    
window= Tk()
#Inicio de aplicacion
start= mclass (window)
Inicio= Button(window, text="Iniciar", command=mainloop ,font=("Helvetica",16), height=1, width=10, cursor="hand1")
Inicio.place(x=740,y=600)
LblEstado=Label(window, text="--------", bg='white', font=("Helvetica", 20))        
LblEstado.place(x=1000, y=200)
LblUnif=Label(window, text="", bg='white', font=("Helvetica", 20))
LblUnif.place(x=1180, y=280)
window.update()
while True:
    window.update()
