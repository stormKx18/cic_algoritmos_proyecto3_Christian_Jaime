from Nodo import Nodo
from Arista import Arista
#******************************************************************************
import os
from queue import PriorityQueue
#https://www.educative.io/edpresso/what-is-the-python-priority-queue
#******************************************************************************
#Clase Grafo
class Grafo:
    def __init__(self,id="grafo",dirigido=False, auto=False):
        self.id=id
        self.nodos={}
        self.aristas={}
        self.dirigido=dirigido
        self.auto=auto

    def agregar_nodo(self, id):
        nuevo_nodo = Nodo(id)
        self.nodos[nuevo_nodo.id]=nuevo_nodo

    def agregar_nodoExistente(self,nodo_existente):
        self.nodos[nodo_existente.id]=nodo_existente

    def agregar_arista(self,source,target):
        try:
            nueva_arista = Arista(self.nodos[source],self.nodos[target])
            self.aristas[nueva_arista.id]=nueva_arista
            self.nodos[source].grado+=1 #aumentar el grado del nodo
            self.nodos[target].grado+=1 #aumentar el grado del nodo
        except:
            print('***Error - Checar que los nodos se hayan decalarado previamente!***')

    def agregar_aristaExistente(self,arista_existente):
        self.aristas[arista_existente.id]=arista_existente

    def calcularGrado(self, nodo):
        return self.nodos[nodo].grado

    def totalNodos(self):
        return len(self.nodos)

    def totalAristas(self):
        return len(self.aristas)

    def checarSiAristaExiste(self,source,target):
        nueva_arista = Arista(self.nodos[source],self.nodos[target])
        nueva_arista2 = Arista(self.nodos[target],self.nodos[source])
        if nueva_arista.id in self.aristas:
            return True
        if(not self.dirigido): #Si no es un grafo dirigido
            if nueva_arista2.id in self.aristas:
                return True
        return False

    def obtenerArista(self,source,target):
        nueva_arista = Arista(self.nodos[source],self.nodos[target])
        nueva_arista2 = Arista(self.nodos[target],self.nodos[source])
        if nueva_arista.id in self.aristas:
            return self.aristas[nueva_arista.id]
        if(not self.dirigido): #Si no es un grafo dirigido
            if nueva_arista2.id in self.aristas:
                return self.aristas[nueva_arista2.id]

    def obtenerPesoDeArista(self,source,target):
        nueva_arista = Arista(self.nodos[source],self.nodos[target])
        nueva_arista2 = Arista(self.nodos[target],self.nodos[source])
        if nueva_arista.id in self.aristas:
            return self.aristas[nueva_arista.id].weight
        if(not self.dirigido): #Si no es un grafo dirigido
            if nueva_arista2.id in self.aristas:
                return self.aristas[nueva_arista2.id].weight
        return 9999999

    def nodosConectados(self,nodo):
        nodos_conectados=[]
        for key, value in self.aristas.items():
            if(value.source == self.nodos[nodo]):
                nodos_conectados.append(int(str(value.target)))
            if(not self.dirigido): #Si no es un grafo dirigido
                if(value.target==self.nodos[nodo]):
                    nodos_conectados.append(int(str(value.source)))
        return nodos_conectados

    def graphviz(self):
        contenido=''
        contenido+='digraph '+self.id+' {\n'

        for nodo in self.nodos: #imprimir nodos
            contenido+=str(nodo)+';\n'

        for key, value in self.aristas.items(): #imprimir aristas
            contenido+= value.id+';\n'

        contenido+='}'

        nombre_completo='gv/'+self.id+'.gv'
        #nombre_completo=self.id+'.gv'
        f = open(nombre_completo, "w")
        f.write(contenido)
        f.close()
        print('Arhivo Graphviz generado: '+nombre_completo+'\n')

    def graphvizWithLabels(self):
        contenido=''
        contenido+='digraph '+self.id+' {\n'

        for key, value in self.nodos.items(): #imprimir nodos
            contenido+='\"nodo_'+str(value.id)+' ('+str(value.distancia)+')\";\n'

        for key, value in self.aristas.items(): #imprimir aristas
            contenido+= '\"nodo_'+str(value.source.id)+' ('+str(value.source.distancia)+')\" -> '+'\"nodo_'+str(value.target.id)+' ('+str(value.target.distancia)+')\" [label='+str(value.weight)+' weight='+str(value.weight)+'];\n'

        contenido+='}'

        nombre_completo='gv/'+self.id+'_labels.gv'
        #nombre_completo=self.id+'.gv'
        f = open(nombre_completo, "w")
        f.write(contenido)
        f.close()
        print('Arhivo Graphviz generado: '+nombre_completo+'\n')

    def display(self):
        print('---'+str(self.totalNodos())+' Nodos---')
        print('---'+str(self.totalAristas())+' Aristas---')

    #Funciones proyecto 2 (BFS, DFS recursivo y DFS iterativo)
    def BFS(self,s): #BFS
        nombre = self.id+ '_BFS_'+str(s)
        #Generar objeto grafo
        grafoBFS = Grafo(nombre)

        #Agregar todos los nodos del grafo como no visitados
        visited=[False] * (self.totalNodos()+ 1)

        # Crear una fila para el algoritmo BFS
        queue = []

        # Agreagr el nodo fuente a la fila y marcarlo como vistiado
        queue.append(s)
        visited[s] = True

        grafoBFS.agregar_nodo(s) #Agregar nodo inicial a grafo BFS

        while queue: #Mientras haya nodos en la fila

            # Sacar de la fila un vertice
            s = queue.pop(0)

            #obtener todos los vertices adyacentes al vertice s
            #si hay un nodo que no ha sido visitado antes, marcarlo y agregarlo a la fila
            vecinos = self.nodosConectados(s)
            for i in vecinos:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
                    grafoBFS.agregar_nodo(i) #Agregar nodo a grafo BFS
                    grafoBFS.agregar_arista(s,i) #Agregar arista

        return grafoBFS

    def DFS_R(self,s): #DFS recursivo
        nombre = self.id+ '_DFS_R_'+str(s)

        #Generar objeto grafo
        grafoDFS_R = Grafo(nombre)

        # Crear un set de vertices visitados
        visitados = set()

        # Llamar la funcion recursiva DFS
        self.DFS_rec(s, visitados,grafoDFS_R)

        return grafoDFS_R

    def DFS_rec(self,s,visitados,grafoDFS_R):
        # Marcar el nodo como visitado
        visitados.add(s)
        grafoDFS_R.agregar_nodo(s) #Agregar nodo inicial a grafo BFS

        #obtener todos los vertices adyacentes al vertice s
        vecinos = self.nodosConectados(s)

        #Recorrer de manera recursiva todos los vertices vecinos
        for vecino in vecinos:
            if vecino not in visitados:
                self.DFS_rec(vecino, visitados,grafoDFS_R)
                grafoDFS_R.agregar_arista(s,vecino) #Agregar arista

    def DFS_I(self,s): #DFS iterativo
        nombre = self.id+ '_DFS_I_'+str(s)

        #Generar objeto grafo
        grafoDFS_I = Grafo(nombre)

        #Agregar todos los nodos del grafo como no visitados
        visited=[False] * (self.totalNodos()+ 1)

        # Create una pila para el algoritmo DFS
        stack = []

        # Agregar el nodo raiz
        stack.append(s)

        #Guardar nodos terminales
        terminal={}
        while (len(stack)):
            # Remover un elemento de la pila
            s = stack[-1]
            stack.pop()

            grafoDFS_I.agregar_nodo(s) #Agregar nodo al grafo

            # Si no ha sido visitado marcarlo como visitado
            if (not visited[s]):
                visited[s] = True

            # Obtener todos los vecinos del vertice
            vecinos = self.nodosConectados(s)

            # Si un vecino no ha sido visitado, agregarlo a la pila
            for vecino in vecinos:
                if (not visited[vecino]):
                    stack.append(vecino)
                    terminal[vecino]=s

        for key, value in terminal.items():
            grafoDFS_I.agregar_arista(key,value) #Agregar arista

        return grafoDFS_I

    def Dijkstra(self,s): #DFS iterativo
        nombre = self.id+ '_Dijkstra__source_'+str(s)

        #Generar objeto grafo
        grafoDijkstra = Grafo(nombre)
        q = PriorityQueue() #Crear cola de prioridad

        self.nodos[s].distancia=0; #Marcar el nodo fuente que tiene una distancia de cero
        q.put(self.nodos[s]) #Agregar nodo a la cola de prioridad


        while not q.empty():
            u = q.get() #Extraer el siguiente nodo (Es una tupla, por eso solo se regresa el segundo element que contiene al nodo)
            u.visitado=True #Marcar el nodo como visitado

            # Obtener todos los vecinos del nodo
            vecinos = self.nodosConectados(u.id)
            for vecino in vecinos:
                if (not self.nodos[vecino].visitado): #si el nodo no ha sido visitado antes
                    peso_arista = self.obtenerPesoDeArista(u.id,vecino)
                    if self.nodos[vecino].distancia > u.distancia + peso_arista:
                        self.nodos[vecino].distancia = u.distancia + peso_arista
                        self.nodos[vecino].padre = u.id
                        q.put(self.nodos[vecino]) #Agregar a la cola de prioridad (en base a distancia)


        #Crear arbol dijkstra
        for key, value in self.nodos.items():
            grafoDijkstra.agregar_nodoExistente(self.nodos[value.id]) #Agregar nodo inicial a grafo Dijkstra
            if value.padre!=None:
                if self.checarSiAristaExiste(value.id,value.padre): #Agregar arista si existe en el grafo original
                    nueva_arista = self.obtenerArista(value.id,value.padre)
                    grafoDijkstra.agregar_aristaExistente(nueva_arista)

        return grafoDijkstra
#******************************************************************************
