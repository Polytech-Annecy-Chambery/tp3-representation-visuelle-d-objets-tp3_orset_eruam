# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul
"""
import OpenGL.GL as gl

class Section:
    # Constructor
    def __init__(self, parameters = {}) :  
        # Parameters
        # position: position of the wall 
        # width: width of the wall - mandatory
        # height: height of the wall - mandatory
        # thickness: thickness of the wall
        # color: color of the wall        

        # Sets the parameters
        self.parameters = parameters
        
        # Sets the default parameters
        if 'position' not in self.parameters:
            self.parameters['position'] = [0, 0, 0]        
        if 'width' not in self.parameters:
            raise Exception('Parameter "width" required.')   
        if 'height' not in self.parameters:
            raise Exception('Parameter "height" required.')   
        if 'orientation' not in self.parameters:
            self.parameters['orientation'] = 0              
        if 'thickness' not in self.parameters:
            self.parameters['thickness'] = 0.2    
        if 'color' not in self.parameters:
            self.parameters['color'] = [0.5, 0.5, 0.5]       
        if 'edges' not in self.parameters:
            self.parameters['edges'] = False             
            
        # Objects list
        self.objects = []

        # Generates the wall from parameters
        self.generate()   
        
    # Getter
    def getParameter(self, parameterKey):
        return self.parameters[parameterKey]
    
    # Setter
    def setParameter(self, parameterKey, parameterValue):
        self.parameters[parameterKey] = parameterValue
        return self     

    # Defines the vertices and faces 
    def generate(self):
        self.vertices = [ 
                [0, 0, 0 ], 
                [0, 0, self.parameters['height']], 
                [self.parameters['width'], 0, self.parameters['height']],
                [self.parameters['width'], 0, 0],         
                [0, self.parameters['thickness'], 0 ], 
                [0, self.parameters['thickness'], self.parameters['height']], 
                [self.parameters['width'], self.parameters['thickness'], self.parameters['height']],
                [self.parameters['width'], self.parameters['thickness'], 0],         
                
                ]
        self.faces = [
                [0,1,2,3],
                [4,5,6,7],
                [0,1,5,4],
                [2,6,7,3],
                [0,4,7,3],
                [1,5,6,2]
                ]   

    # Checks if the opening can be created for the object x
    def canCreateOpening(self, x):
        if x.parameters['position'][0] + x.parameters['width'] > self.parameters['position'][0]+self.parameters['width']:
            return False
        if x.parameters['position'][2]+x.parameters['height'] > self.parameters['position'][2]+self.parameters['height']:
            return False
        if x.parameters['position'][0] < self.parameters['position'][0]:
            return False
        if x.parameters['position'][2] < self.parameters['position'][2]:      
            return False
        if x.parameters['position'][1] != self.parameters['position'][1]:      
            return False
        return True
        
        
        
    # Creates the new sections for the object x
    def createNewSections(self, x):
        resSections = []
        if self.canCreateOpening(x):
            section1 = Section({'position':self.parameters['position'],\
                                'width':x.parameters['position'][0]-self.parameters['position'][0],\
                                'height':self.parameters['height'],\
                                'thickness':self.parameters['thickness'],\
                                'orientation':self.parameters['orientation'],\
                                'color':self.parameters['color']})
            resSections.append(section1)
            
            section2 = Section({'position':[x.parameters['position'][0],x.parameters['position'][1],x.parameters['position'][2]+x.parameters['height']],\
                                'width':x.parameters['width'],\
                                'height':self.parameters['height'] - (x.parameters['position'][2] + x.parameters['height']),\
                                'thickness':self.parameters['thickness'],\
                                'orientation':self.parameters['orientation'],\
                                'color':self.parameters['color']})
            resSections.append(section2)
            
            section3 = Section({'position':[x.parameters['position'][0],x.parameters['position'][1],self.parameters['position'][2]],\
                                'width': x.parameters['width'],\
                                'height': x.parameters['position'][2] - self.parameters['position'][2],\
                                'thickness': self.parameters['thickness'],\
                                'orientation': self.parameters['orientation'],\
                                'color': self.parameters['color']})
            resSections.append(section3)
            
            section4 = Section({'position':[x.parameters['position'][0]+x.parameters['width'],self.parameters['position'][1],self.parameters['position'][2]],\
                                'width':self.parameters['position'][0]+self.parameters['width'] - x.parameters['position'][0]+x.parameters['width'],\
                                'height':self.parameters['height'],\
                                'thickness':self.parameters['thickness'],\
                                'orientation':self.parameters['orientation'],\
                                'color':self.parameters['color']})
           
            resSections.append(section4)
        return resSections



             
        
    # Draws the edges
    def drawEdges(self):
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_LINE)    
        gl.glTranslatef(self.parameters['position'][0],self.parameters['position'][1], self.parameters['position'][1])       

        for face in self.faces:
            gl.glBegin(gl.GL_QUADS) # Tracé d’un quadrilatère
            gl.glColor3fv([self.parameters['color'][0]*0.5,self.parameters['color'][1]*0.5,self.parameters['color'][1]*0.5]) # Couleur gris moyen
            gl.glVertex3fv(self.vertices[face[0]])
            gl.glVertex3fv(self.vertices[face[1]])
            gl.glVertex3fv(self.vertices[face[2]])
            gl.glVertex3fv(self.vertices[face[3]])
            gl.glEnd()
                    
    # Draws the faces
    def draw(self):
        gl.glPushMatrix() 
        gl.glTranslatef(self.parameters['position'][0],self.parameters['position'][1], self.parameters['position'][2])       
        gl.glRotatef(self.parameters['orientation'], 0, 0, 1)
        if self.parameters['edges']:
            self.drawEdges()
            
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL) # on trace les faces : GL_FILL
        for face in self.faces:
            gl.glBegin(gl.GL_QUADS) # Tracé d’un quadrilatère
            gl.glColor3fv(self.parameters['color']) # Couleur gris moyen
            gl.glVertex3fv(self.vertices[face[0]])
            gl.glVertex3fv(self.vertices[face[1]])
            gl.glVertex3fv(self.vertices[face[2]])
            gl.glVertex3fv(self.vertices[face[3]])
            gl.glEnd()
            
        gl.glPopMatrix()
  