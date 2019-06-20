"""
MachineLearning for Early-Alert System project.

Created by Brayan Rojas, Elkin Prada, on June 2019.
Co-workers: Carlos Sierra, Santiago Salazar
Copyright (c) 2019 Brayan Rojas, Elkin Prada Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.
"""

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import random
import wx

class Simulation(wx.Frame, TemplateView):
    
    """docstring for ."""
    def __init__(self, parent , id , title):
        self.contador = 0
        self.velocidad = 1.0
        self.intervalo_reproduccion = 10
        self.intervalo_muerte = 22
        wx.Frame.__init__(self , parent , id , title ,
            style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX |
            wx.MINIMIZE_BOX)
        self.Size = (1200 , 630)
        self.Centre()
        self.Show(True)
        self.numBacterias = 0
        self.areaHojas = 3300 - ((130 - 35)* 3) - 915
        self.gradoSeveridad = "Grado 0"
        #escenario de 100 * 5
        self.tamano_cuadros = [10]
        self.intervalo_tiempo = 200
        #matriz cuadros 130 * 50
        self.imagen_escenario = []
        self.numero_filas = 200 #130
        self.numero_columnas =  50

        #mostrar contador de tiempo
        grilla = wx.GridBagSizer()
        self.entradaTiempo = wx.TextCtrl(self,-1,value=u"Tiempo transcurrido: 0 Días")
        #grilla.Add(self.entradaTiempo,(0,0),(1,1),wx.EXPAND)
        #   self.SetSizerAndFit(grilla)
        self.Show(True)

        for i in range(self.numero_filas):
            self.imagen_escenario.append([])
            for j in range(self.numero_columnas):
                self.imagen_escenario[i].append(None)

        self.barra_menu_metodo()
        self.UI()

    def barra_menu_metodo(self):
        self.barra_menu = wx.MenuBar()
        self.menu_programa = wx.Menu()
        self.menu_ayuda = wx.Menu()
        self.barra_menu.Append(self.menu_ayuda, "&Ayuda")
        #self.Bing(wx.EVT_MENU, self.On_About_it, self.sub_menu_acerca)
        self.SetMenuBar(self.barra_menu)

    def UI(self):
        #timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        #panel universal
        self.panel = wx.Panel(self, -1, size = (1200,600))
        self.panel.SetBackgroundColour(wx.Colour(0,0,0))
        #panel escenario
        self.panel_escenario = wx.Panel(self, -1, size = (1200,500))
        self.panel_escenario.SetBackgroundColour(wx.Colour(250, 250, 250))
        #panel controles
        self.panel_controles = wx.Panel(self, -1, size = (1200,50))
        self.panel_controles.SetBackgroundColour(wx.Colour(225,227,171))
        #logica
        self.data = wx.TextCtrl(self.panel_controles, value = "Grado 0, Tiempo: 0 Días", style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY, size=(200, -1))
        #self.slider_tamano = wx.Slider(self.panel_controles, -1,10, self.tamano_cuadros[0],30)
        self.boton_aleatorio = wx.Button(self.panel_controles, -1, u"Aleatoreo")
        self.boton_parar = wx.Button(self.panel_controles, -1,u"Parar")
        self.boton_iniciar = wx.Button(self.panel_controles, -1,u"¡Iniciar!")
        self.boton_borrar = wx.Button(self.panel_controles, -1,u"Borrar")
        self.boton_relentizar = wx.Button(self.panel_controles, -1,u"Seco")
        self.boton_acelerar = wx.Button(self.panel_controles, -1,u"Lluvia")
        self.boton_MiniPoblado = wx.Button(self.panel_controles, -1,u"Inicio de Inoculación")
        #sizeando
        self.sizer_controles = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_controles.Add(self.data, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer_controles.Add(self.boton_aleatorio, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer_controles.Add(self.boton_parar, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer_controles.Add(self.boton_iniciar, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer_controles.Add(self.boton_borrar, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer_controles.Add(self.boton_relentizar, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer_controles.Add(self.boton_acelerar, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer_controles.Add(self.boton_MiniPoblado, 1, wx.EXPAND | wx.ALL, 10)
        self.panel_controles.SetSizer(self.sizer_controles)
        self.sizer_universal = wx.BoxSizer(wx.VERTICAL)
        self.sizer_universal.Add(self.panel_escenario, 1, wx.EXPAND|wx.ALL,10)
        self.sizer_universal.Add(self.panel_controles, 1, wx.EXPAND|wx.ALL,10)
        self.panel.SetSizer(self.sizer_universal)
        #eventos
        self.panel_escenario.Bind(wx.EVT_PAINT, self.onPaint)
        #self.slider_tamano.Bind(wx.EVT_SLIDER, self.onSlider_tamano)
        self.boton_aleatorio.Bind(wx.EVT_BUTTON,self.onBoton_aleatorio)
        self.boton_parar.Bind(wx.EVT_BUTTON,self.onBoton_parar)
        self.boton_iniciar.Bind(wx.EVT_BUTTON,self.onBoton_iniciar)
        self.boton_borrar.Bind(wx.EVT_BUTTON,self.onBoton_borrar)
        self.boton_relentizar.Bind(wx.EVT_BUTTON,self.onBoton_relentizar)
        self.boton_acelerar.Bind(wx.EVT_BUTTON,self.onBoton_acelerar)
        self.boton_MiniPoblado.Bind(wx.EVT_BUTTON,self.onBoton_MiniPoblado)
        self.Bind(wx.EVT_WINDOW_DESTROY,self.onSalir)
        self.device_context_PAINT = wx.ClientDC(self.panel_escenario)
        self.device_context_PAINT.SetBrush(wx.Brush("BLACK"))



    def onBoton_MiniPoblado(self,evento):
        self.borrar_escenario()
        self.contador = 0
        self.data.SetValue("Grado 0, Tiempo: 0 Días")
        #130*50 es el escenario las celulas vivas se deben estar cerca
        for i in range(self.tamano_cuadros[0]):
            x_aleatorio = random.randrange(30) + int(90)
            y_aleatorio = random.randrange(10) + int (33)


            if(x_aleatorio > 90):
                self.imagen_escenario[x_aleatorio][y_aleatorio] = 1
                break

        for i in range(self.tamano_cuadros[0]):
            x_aleatorio = random.randrange(30)
            y_aleatorio = random.randrange(10) + int (33)

            if(x_aleatorio < 40):
                self.imagen_escenario[x_aleatorio][y_aleatorio] = 1            
                break


    def onSalir(self, evento):
        self.timer.Stop()
    
    def onPaint(self, evento):
        tamCogollo = 0
        countm = 0
        for y in range(0, self.numero_columnas):
            if( y <= 25):
                if(y > 3):
                    tamCogollo = tamCogollo + 1
            else:
                tamCogollo = tamCogollo - 1

            for x in range(0, self.numero_filas):
                #self.dibujar_cuadrado()
                #Se dibuja el cogollo
                if x >= (60-tamCogollo) and x <= 60 + tamCogollo:
                    if y >= (25-15) and y <= (25 + 15):
                        dc = wx.PaintDC(self.panel_escenario)
                        dc.SetBrush(wx.Brush(wx.Colour(117,63,10)))
                        dc.DrawRectangle((x*self.tamano_cuadros[0]), (y*self.tamano_cuadros[0]), self.tamano_cuadros[0], self.tamano_cuadros[0])
                        countm = countm + 1
                    else:
                        if((y == 20) or (y == 28) or (y == 37) or (y == 47)):
                            dc = wx.PaintDC(self.panel_escenario)    
                            dc.DrawRectangle((x*self.tamano_cuadros[0]), (y*self.tamano_cuadros[0]), self.tamano_cuadros[0], self.tamano_cuadros[0])
                        else:
                            if (y > (25-16) and y < 25+16):
                                dc = wx.PaintDC(self.panel_escenario)
                                dc.SetBrush(wx.Brush(wx.Colour(87,166,57)))
                                dc.DrawRectangle((x*self.tamano_cuadros[0]), (y*self.tamano_cuadros[0]), self.tamano_cuadros[0], self.tamano_cuadros[0])
                            else:
                                dc = wx.PaintDC(self.panel_escenario)
                                dc.SetBrush(wx.Brush(wx.Colour(87,166,57)))
                                dc.DrawRectangle((x*self.tamano_cuadros[0]), (y*self.tamano_cuadros[0]), self.tamano_cuadros[0], self.tamano_cuadros[0])

                else:
                    if (y > (25-16) and y < 25+16):
                        dc = wx.PaintDC(self.panel_escenario)
                        dc.SetBrush(wx.Brush(wx.Colour(87,166,57)))
                        dc.DrawRectangle((x*self.tamano_cuadros[0]), (y*self.tamano_cuadros[0]), self.tamano_cuadros[0], self.tamano_cuadros[0])
                        if((y == 20) or (y == 28) or (y == 37) or (y == 47)):
                            dc = wx.PaintDC(self.panel_escenario)    
                            dc.DrawRectangle((x*self.tamano_cuadros[0]), (y*self.tamano_cuadros[0]), self.tamano_cuadros[0], self.tamano_cuadros[0])
                    else:
                        dc = wx.PaintDC(self.panel_escenario)
                        dc.SetBrush(wx.Brush(wx.Colour(87,166,57)))
                        dc.DrawRectangle((x*self.tamano_cuadros[0]), (y*self.tamano_cuadros[0]), self.tamano_cuadros[0], self.tamano_cuadros[0])   




    def update(self,evento):
        self.device_context_PAINT.Clear()
        self.algoritmo_juego_de_la_vida()
        self.Refresh()
        self.actualizar_escenario()
        #print (self.imagen_escenario)

    def onSlider_tamano (self, evento):
        self.device_context_PAINT.Clear()
        self.Refresh()
        self.tamano_cuadros[0] = self.slider_tamano.GetValue()
        self.actualizar_escenario()

    def onBoton_aleatorio(self, evento):
        #primero se formatea el escenario
        self.borrar_escenario()
        #el escenario es una matriz de 2 dimensiones
        for i in range(self.numero_filas):
            for j in range(self.numero_columnas):
                #como solo busca entre 1 y 0 es probable que escoja muchos unos
                self.imagen_escenario[i][j] = random.randrange(0, 2) #01
        self.actualizar_escenario()

    def onBoton_parar(self, evento):
        self.timer.Stop()

    def onBoton_borrar(self, evento):
        #el escenario es una matriz de 2 dimensiones
        self.borrar_escenario()
 

    def onBoton_relentizar(self,evento):
        self.timer.Stop()
        self.intervalo_tiempo = 200
        self.timer.Start(self.intervalo_tiempo)
        self.velocidad = 1
        self.intervalo_reproduccion = 15
        self.intervalo_muerte = 10

    def onBoton_acelerar(self, evento):
        self.timer.Stop()
        self.intervalo_tiempo = 100
        self.timer.Start(self.intervalo_tiempo)
        self.velocidad = 0.5
        self.intervalo_reproduccion = 5
        self.intervalo_muerte = 30



    def onBoton_iniciar(self, evento):
        self.timer.Start((self.intervalo_tiempo))


    def algoritmo_juego_de_la_vida(self):
        imagen_escenario_temp = self.imagen_escenario
        muerte_bacteria = False
        if(self.contador % self.intervalo_muerte == 0 and self.contador != 0):
            muerte_bacteria = True

        for x in range(0, self.numero_filas):
            for y in range(0, self.numero_columnas):
                cuadro = self.imagen_escenario[x][y]
                if(cuadro):
                    if(muerte_bacteria):
                        imagen_escenario_temp[x][y] = 0
                        muerte_bacteria = False
                    else:

                        #Reproduccion asexual bacteria
                        if(self.contador % self.intervalo_reproduccion == 0 and self.contador != 0):
                            validador = True
                            try:
                                if (self.imagen_escenario[x][y+1]):
                                    validador = True    
                            except Exception:
                                validador = False
                            
                            try:

                                if(self.imagen_escenario[x][y-1]):
                                    validador = True
                            except Exception:
                                validador = False

                            try:
                                if(self.imagen_escenario[x+1][y]):
                                    validador = True
                            except Exception:
                                validador = False

                            try:
                                if (self.imagen_escenario[x-1][y]):
                                    validador = True
                            except Exception:
                                validador = False

                            if (validador):
                                whileValidator = True
                                lugarOne = False
                                lugarTwo = False
                                lugarTree = False
                                lugarFour = False
                                while(whileValidator):
                                    lugar = random.randrange(4)
                                    if(lugar == 0):
                                        try:
                                            if(imagen_escenario_temp[x][y-1] != 1):
                                                #print('entro')
                                                imagen_escenario_temp[x][y-1] = 1
                                                whileValidator = False
                                            else:
                                                lugarOne = True
                                                print('e1')
                                        except Exception:
                                            lugarOne = True
                                            print('e1')
                                    else:
                                        if(lugar == 1):
                                            try:
                                                if(imagen_escenario_temp[x][y+1] != 1):
                                                    #print('entro')
                                                    imagen_escenario_temp[x][y+1] = 1
                                                    whileValidator = False
                                                else:
                                                    lugarTwo = True
                                                    print('e2')
                                            except Exception:
                                                lugarTwo = True
                                                print('e2')
                                        else:
                                            if(lugar == 2):
                                                try:
                                                    if(imagen_escenario_temp[x-1][y] != 1):
                                                        #print('entro')
                                                        imagen_escenario_temp[x-1][y] = 1
                                                        whileValidator = False
                                                    else:
                                                        lugarTree = True
                                                        print('e3')
                                                    
                                                except Exception:
                                                    lugarTree = True
                                                    print('e3')
                                            else:
                                                if(lugar == 3):
                                                    try:
                                                        if(imagen_escenario_temp[x+1][y] != 1):
                                                            #print('entro')
                                                            imagen_escenario_temp[x+1][y] = 1
                                                            whileValidator = False
                                                        else:
                                                            lugarFour = True
                                                            print('e4')
                                                        
                                                    except Exception:
                                                        lugarFour = True
                                                        print('e4')

                                    if(lugarOne and lugarTwo and lugarTree and lugarFour):
                                        print('entro')
                                        whileValidator = False

                        else:
                            #movimiento normal
                            imagen_escenario_temp[x][y] = 0
                            whileValidator = True
                            lugarOne = False
                            lugarTwo = False
                            lugarTree = False
                            lugarFour = False
                            while(whileValidator):
                                lugar = random.randrange(4)
                                if(lugar == 0):
                                    try:
                                        if(imagen_escenario_temp[x][y-1] != 1):
                                            #print('entro')
                                            imagen_escenario_temp[x][y-1] = 1
                                            whileValidator = False
                                        else:
                                            lugarOne = True
                                    except Exception:
                                        lugarOne = True
                                else:
                                    if(lugar == 1):
                                        try:
                                            if(imagen_escenario_temp[x][y+1] != 1):
                                                #print('entro')
                                                imagen_escenario_temp[x][y+1] = 1
                                                whileValidator = False
                                            else:
                                                lugarTwo = True
                                        except Exception:
                                            lugarTwo = True
                                    else:
                                        if(lugar == 2):
                                            try:
                                                if(imagen_escenario_temp[x-1][y] != 1):
                                                    #print('entro')
                                                    imagen_escenario_temp[x-1][y] = 1
                                                    whileValidator = False
                                                else:
                                                    lugarTree = True
                                                
                                            except Exception:
                                                lugarTree = True
                                        else:
                                            if(lugar == 3):
                                                try:
                                                    if(imagen_escenario_temp[x+1][y] != 1):
                                                        #print('entro')
                                                        imagen_escenario_temp[x+1][y] = 1
                                                        whileValidator = False
                                                    else:
                                                        lugarFour = True
                                                    
                                                except Exception:
                                                    lugarFour = True
                                                    
                                if(lugarOne and lugarTwo and lugarTree and lugarFour):
                                    whileValidator = False




                    

        self.imagen_escenario = imagen_escenario_temp


    def movimientoUnoBacteria(imagen_escenario_temp,x,y):
        lugar = random.randrange(4)
        if(lugar == 1):
            try:
                imagen_escenario_temp[x][y-1] = 1
            except Exception:
                pass
        else:
            if(lugar == 2):
                try:
                    imagen_escenario_temp[x][y+1] = 1
                except Exception:
                    pass
            else:
                if(lugar == 3):
                    try:
                        imagen_escenario_temp[x-1][y] = 1
                    except Exception:
                        pass
                else:
                    if(lugar == 4):
                        try:
                            imagen_escenario_temp[x+1][y] = 1
                        except Exception:
                            pass


    def borrar_escenario(self): #se establecen en 0 todas las casillas
        self.contador = 0
        for x in range(0, self.numero_filas):
            for y in range(0, self.numero_columnas):
                self.imagen_escenario[x][y] = 0
        self.Refresh()
        self.actualizar_escenario()

    def dibujar_cuadrado(self, x, y):
        # se dibuja un cuadrado en exactamente esa coordenadas
        #print ("!!!!!!!!!!!!!!!!!!!!!!!!!1")
        width = self.tamano_cuadros[0]

        height = self.tamano_cuadros[0]
        dc = wx.PaintDC(self.panel_escenario)
        sc.DrawRectangle(x,y,width,height)

    def actualizar_escenario(self):
        # se dibuja todo en el escenario
        #se dibuja la malla (1200, 500) la malla es de 130 * 50 cuadros
        #se dibujan cuadrados
        self.numBacterias = 0
        for x in range(0, self.numero_filas):
            for y in range(0, self.numero_columnas):
                if(self.imagen_escenario[x][y] == 1):
                    dc = wx.ClientDC(self)
                    if(self.contador >= 0 and self.contador <= 25):
                        dc.SetBrush(wx.Brush(wx.Colour(138,102,66)))
                    else:
                        if(self.contador >= 26 and self.contador <= 40):
                            dc.SetBrush(wx.Brush(wx.Colour(166,94,46)))
                        else:
                            if(self.contador >= 41 and self.contador <= 80):
                                dc.SetBrush(wx.Brush(wx.Colour(237,255,33)))
                            else:
                                if(self.contador >= 81):
                                    dc.SetBrush(wx.Brush(wx.Colour(237,255,33)))

                    dc.DrawRectangle((x*self.tamano_cuadros[0]), (y*self.tamano_cuadros[0]), self.tamano_cuadros[0], self.tamano_cuadros[0])
                    self.numBacterias = self.numBacterias + 1

                    #print ("yo soy 1 -------------")
        if (self.numBacterias >= (self.areaHojas * 0.01) and self.numBacterias <= (self.areaHojas * 0.2)):
            self.gradoSeveridad = "Grado 1"
        else:
            if (self.numBacterias >= (self.areaHojas * 0.201) and self.numBacterias <= (self.areaHojas * 0.4)):
                self.gradoSeveridad = "Grado 2"
            else:
                if (self.numBacterias >= (self.areaHojas * 0.401) and self.numBacterias <= (self.areaHojas * 0.6)):
                    self.gradoSeveridad = "Grado 3"
                else:
                    if (self.numBacterias >= (self.areaHojas * 0.601) and self.numBacterias <= (self.areaHojas * 0.8)):
                        self.gradoSeveridad = "Grado 4"
                    else:
                        if (self.numBacterias >= (self.areaHojas * 0.801) and self.numBacterias <= (self.areaHojas * 1)):
                            self.gradoSeveridad = "Grado 5"

        self.contador = self.contador + self.velocidad
        
        dias = "Tiempo: "+ str(self.contador) + " Días"

        self.data.SetValue(self.gradoSeveridad + " " + dias)
        #print(self.gradoSeveridad)
        print(self.contador)

@login_required
def main(self):
    Programa = wx.App()
    juego_de_la_vida = Simulation(None,-1,u'Pudrición del Cogollo Palma de Aceite')
    aux = Programa.MainLoop()
    print ("<<<<<<<<<<<<", aux)
    return HttpResponse("Start Simulation")

if __name__ == '__main__':
    main()


@login_required
def load_file(request):
    return render(request,'../templates/network/load_file.html')

@login_required
def list_alerts(request):
    return render(request,'../templates/network/alert.html')