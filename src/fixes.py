import datetime
x = datetime.datetime.now()
print(x)
#******************************************************************************
nodo_raiz=1
print('nodo_raiz: ',nodo_raiz)
#******************************************************************************
from grafoErdosRenyi import grafoErdosRenyi
#******************************************************************************
#grafoErdosRenyi - Muchos nodos
gfErdosReny = grafoErdosRenyi(n=100, m=100, dirigido=False, auto=False)
gfErdosReny.display()
gfErdosReny.graphvizWithLabels()

dijkstra=gfErdosReny.Dijkstra(nodo_raiz)
dijkstra.display()
dijkstra.graphvizWithLabels()
