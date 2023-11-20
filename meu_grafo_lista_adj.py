from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *





class MeuGrafo(GrafoListaAdjacencia):

    def vertices_nao_adjacentes(self): 
        retorno = set()     #set de retorno
        vertices_adijacentes = set()
        for i in self.arestas.values():
            vertices_adijacentes.add(str(i.v1)+'-'+str(i.v2))
            vertices_adijacentes.add(str(i.v2)+'-'+str(i.v1))
        vertices = self.vertices
        for i in range(len(vertices)):
            for j in range(i+1,len(vertices)):
                v = str(vertices[i])+'-'+str(vertices[j])
                if v not in vertices_adijacentes:
                    retorno.add(v)
        return retorno

            

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
        for i in self.arestas.values():      #pega todas as arestas
            r1 = str(i.v1)+str(i.v2)      #cria um rotulo com os vertices
            r2 = str(i.v2)+str(i.v1)
            if r1 in s or r2 in s:  # se esse rotulo já apareceu antes
                return True
            s.add(r1)       # adiciona o rotulo à lista
        return False

    def arestas_sobre_vertice(self, V):
        if not(self.existe_rotulo_vertice(V)):
            raise VerticeInvalidoError(f"o Vertice {V} não é um vertice valido")

        V = str(V)
        retorno = set()
        for j,i in self.arestas.items():
            if str(i.v1) == V or str(i.v2) == V:
                retorno.add(j)
        return retorno

    def eh_completo(self):
        if self.ha_laco() or self.ha_paralelas(): return False
        s = set()    #set novo
        for i in self.arestas.values():   # pega todas as arestas
            s.add(str(i.v1)+' '+str(i.v2)) # guarda todas as combinações existentes de arestas
            s.add(str(i.v2)+' '+str(i.v1)) 

        vertices = self.vertices    # pega todos os vertices
        for i in range(len(vertices)):  # pega todos os vertices 
            for j in range(i+1,len(vertices)): # pega todos os vertices que faltam para forma um par
                if str(vertices[i])+' '+str(vertices[j]) not in s:  #cria todas as combinações possíveis de arestas e vê se elas estão nas combinações existentes
                    return False    # se alguma combinação possível não existir ele não é Completo
        return True  # se todas as combinações possíveis estiverem no grafo ele é completo

    def dfs(self, V=''): #V = Verticie raiz
        def recursao(w,passed,grafo:MeuGrafo):
            passed.add(w)
            arestas = list(self.arestas_sobre_vertice(w))
            arestas.sort()
            for a in arestas:
                a = self.arestas[a]
                v = a.v1.rotulo if a.v1.rotulo != w else a.v2.rotulo
                if v in passed: continue
                grafo.adiciona_vertice(v)
                grafo.adiciona_aresta(a.rotulo,a.v1.rotulo,a.v2.rotulo,a.peso)

                recursao(v,passed,grafo)
            return grafo
        g = MeuGrafo()
        g.adiciona_vertice(V)
        return recursao(V,set(),g)

    def Menores_Caminhos_Bellman_Ford(self,Inicio:str,Final:str) -> tuple(bool,any):
        

        if not(self.existe_rotulo_vertice(Inicio)):
            raise VerticeInvalidoError(f"O Rotulo do Vertice '{Inicio}' não foi encontrado") 
        elif not(self.existe_rotulo_vertice(Final)):
            raise VerticeInvalidoError(f"O Rotulo do Vertice '{Final}' não foi encontrado")
        
        def Ciclo() -> bool:
            b = False
            for aresta in self.arestas().values():
                soma = self.Bellman_Ford_Var['B'][aresta.v1.rotulo] + aresta.peso
                if soma < self.Bellman_Ford_Var['B'][aresta.v2.rotulo]:
                    b = True
                    self.Bellman_Ford_Var['B'][aresta.v2.rotulo] = soma
                    self.Bellman_Ford_Var['P'][aresta.v2.rotulo] = [(aresta.v1.rotulo,aresta)]
                elif soma == self.Bellman_Ford_Var['B'][aresta.v2.rotulo]:
                    b = True
                    self.Bellman_Ford_Var['P'][aresta.v2.rotulo].append((aresta.v1.rotulo,aresta))
            return b
        

        def Finalizar() -> tuple(bool,any):
            
            if Ciclo(): return (False,"Ciclo Negativo")    
                
            def recursao(atual) -> list(MeuGrafo):
                if self.Bellman_Ford_Var['P'][atual][0] is None:
                    g = MeuGrafo()
                    g.adiciona_vertice(self.vertices[atual])
                    return [g]
                
                l = []
                for i in self.Bellman_Ford_Var['P'][atual]:
                    for j in recursao(i[0]):
                        if atual in j.vertices: continue
                        j.adiciona_vertice(self.vertices[atual])
                        j.adiciona_aresta(i[1])
                        l.append(j)
                return l
                

            if self.Bellman_Ford_Var['B'][Final] == float('inf'): return (False,"Sem Caminho") # retorno caso não exista caminho até o Vertice
            g = recursao(Final)
            return (True, g)


        self.Bellman_Ford_Var = {}

        self.Bellman_Ford_Var['B'] = {i.rotulo:float('inf') for i in self.vertices}
        self.Bellman_Ford_Var['B'][Inicio] = 0
        self.Bellman_Ford_Var['P'] = {i.rotulo:[None] for i in self.vertices}
        
        for i in range(len(self.vertices)-1):Ciclo()
        return Finalizar()

