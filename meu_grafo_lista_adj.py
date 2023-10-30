from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *



class MeuGrafo(GrafoListaAdjacencia):

    def vertices_nao_adjacentes(self): 
        retorno = set()     #set de retorno
        for vertice in self.vertices:     #pega todos os vertices um a um
            verticesAdijacentes = set()     #set com todos os vertices adjacentes e o proprio vertice
            for i in self.arestas_sobre_vertice():     #pega todas as arestas que passam pelo vertice um a um
                verticesAdijacentes.add(i.v1)     # adiciona ambas das pontas da areasta no set
                verticesAdijacentes.add(i.v2)
            for i in self.vertices:     #pega todos os vertices um a um
                if i in verticesAdijacentes:    # se ele for adjacente passa para o proximo
                    continue
                retorno.add(vertice+"-"+i)    #adiciona os não adjasentes ao set
        return retorno      # retorna os não adjacentes

            

    def ha_laco(self):
        for i in self.arestas.values(): #pega todas as arestas um a um
            if i.v1 == i.v2:    # vê se os vertices na ponta são o mesmo
                return True     
        return False

    def grau(self, V=''):
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError()
        grau = 0
        arestas = self.arestas

        for a in arestas:
            if arestas[a].v1.rotulo == V:
                grau += 1
            if arestas[a].v2.rotulo == V:
                grau += 1
        return grau

    def ha_paralelas(self):
        s = set()       #cria um set
        for i in self.arestas:      #pega todas as arestas
            r1 = i.v1+i.v2      #cria um rotulo com os vertices
            r2 = i.v2+i.v1
            if r1 in s or r2 in s:  # se esse rotulo já apareceu antes
                return True
            s.add(r1)       # adiciona o rotulo à lista
        return False

    def arestas_sobre_vertice(self, V):
        if not(self.vertice_valido(V)):
            VerticeInvalidoError(f"o Vertice {V} não é um vertice valido")
        elif V not in self.vertices:
            VerticeInvalidoError(f"o Vertice {V} não é um vertice do grafo {self}")#asdasdxcxza


        retorno = set()
        for i in self.arestas:
            if i.v1 == V or i.v2 == V:
                retorno.add(i)
        return retorno

    def eh_completo(self):
        s = set()    #set novo
        for i in self.arestas:
            s.add(i.v1+i.v2) # sim
            s.add(i.v2+i.v1) # sim

        for i in range(len(self.vertices)):
            for j in range(i,len(self.vertices)):
                if self.vertices[i]+self.vertices[j] not in s:
                    return False
        return True