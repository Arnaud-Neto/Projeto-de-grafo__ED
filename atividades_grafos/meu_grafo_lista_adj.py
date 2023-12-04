from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *


class BellmanFordError(Exception):
    pass


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

    def Menores_Caminhos_Bellman_Ford(self,Inicio:str,Final:str,RetornarListaDe:str='Grafo') -> tuple(): # retona uma tupla sendo o primeiro items um booleano que diz se foi possivel pegar os menores caminhos e o segundo item sendo uma lista com os menores caminho caso pocivel, se não a saida vai ser uma string dizendo o motivo de não encontrar um menor caminho

        if not(self.existe_rotulo_vertice(Inicio)):
            raise VerticeInvalidoError(f"O Rotulo do Vertice '{Inicio}' não foi encontrado") 
        elif not(self.existe_rotulo_vertice(Final)):
            raise VerticeInvalidoError(f"O Rotulo do Vertice '{Final}' não foi encontrado")
        
        if RetornarListaDe not in ('Grafo', 'Lista de Vertices', 'Lista de Arestas', 'Lista de Vertices e Arestas', 'str'): raise ValueError(f"Tipo de Retorno '{RetornarListaDe}' não é um tipo de retorno valido")


        class Lista_Retorno(): # objeto que é criado pela função finalizar caso <RetornarListaDe> seja diferente de 'Grafo'
                def __init__(self) -> None:
                    self.List_vertices = []
                    self.vertices = set()      # Lista de Vertices
                    self.arestas = []       # Lista de Arestas
                    self.vertices_arestas = []  #Lista  de Vertices e Arestas
                    self.String = ''        # Lista de str

                def adiciona_vertice(self,V):
                    self.vertices.add(V)
                    self.List_vertices.append(V)
                    self.vertices_arestas.append(V)
                    self.String += V.rotulo

                def adiciona_aresta(self,A):
                    self.arestas.append(A)
                    self.vertices_arestas.append(A)
                    self.String += f" -{A.rotulo}-> "

                def Retorno(self):
                    match RetornarListaDe:

                        case 'Lista de Vertices':
                            return self.List_vertices
                        
                        case 'Lista de Arestas':
                            return self.arestas
                        
                        case 'Lista de Vertices e Arestas':
                            return self.vertices_arestas
                        
                        case 'str':
                            return self.String
                        


        def Ciclo() -> bool: # realiza um ciclo do algoritimo de Bellman_Ford

            b = False # se algum Beta Mudou ou não mudou ou não

            for aresta in self.arestas.values(): # Pega todos os Objetos <Aresta>, Conciderando todas como arestas direcionadas sendo v1 o inicio e v2 o final

                soma = self.Bellman_Ford_Var['B'][aresta.v1.rotulo] + aresta.peso #soma o Beta do inicio com o peso da aresta

                if soma < self.Bellman_Ford_Var['B'][aresta.v2.rotulo]: # se a soma for menor que o beta do final

                    b = True        # um beta mudou
                    self.Bellman_Ford_Var['B'][aresta.v2.rotulo] = soma     # troca o beta do final para a soma
                    self.Bellman_Ford_Var['P'][aresta.v2.rotulo] = {aresta.v1.rotulo : aresta}  # troca o pi 

                elif soma == self.Bellman_Ford_Var['B'][aresta.v2.rotulo] and aresta.v1.rotulo not in self.Bellman_Ford_Var['P'][aresta.v2.rotulo]:     # se o beta final for igual a soma
                    
                    self.Bellman_Ford_Var['P'][aresta.v2.rotulo][aresta.v1.rotulo] = aresta # adiciona o um novo pi ao vertice
            
            return b # retorna um bool se algum beta mudou
        

        def Finalizar() -> tuple(): # utiliza os pi's para retorna todos os menores caminhos do grafo em forma de grafos
             
                
            def recursao(atual) -> list():     # Passa recurcivamente por todos os pi's do final até o inicio retornado um uma lista de grafos que representam o caminho passado
                
                if Inicio in self.Bellman_Ford_Var['P'][atual] and self.Bellman_Ford_Var['P'][atual][Inicio] is None: # Se o pi atual é None então chegamos ao inicio
                    

                    g = MeuGrafo() if RetornarListaDe == 'Grafo' else Lista_Retorno()   # Cria o Objeto à ser retornado 
                    g.adiciona_vertice(self.Bellman_Ford_Var['Vertices'][atual]) # adiciona o vetice atual
                    return [g]          # Retorna uma lista com um grafo
                

                l = []  # cria uma lista
                
                for i in self.Bellman_Ford_Var['P'][atual].keys():   # pega todos os pi's do Vertice atual
                    for j in recursao(i):        # aplica recursão em todos os pi's do Vetice atual, sendo j cada um dos grafos retornados
                        
                        if self.Bellman_Ford_Var['Vertices'][atual] in j.vertices: continue    # se o Vertice atual já tiver aparecido no grafo então passa para o proximo sem adicionalo a lista l
                        
                        j.adiciona_vertice(self.Bellman_Ford_Var['Vertices'][atual])  # adiciona o Vertice atual no grafo
                        j.adiciona_aresta(self.Bellman_Ford_Var['P'][atual][i])         # adiciona a aresta do pi
                        l.append(j)               # adiciona o grafo a lista 
                
                return l # retorna uma lista de grafos
                

            if self.Bellman_Ford_Var['B'][Final] == float('inf'): return (False,"Sem Caminho") # retorno caso não exista caminho até o Vertice
            lg = recursao(Final) # recebe a lista de Objetos

            if RetornarListaDe != 'Grafo': # se Retorno não for grafos
                for i in range(len(lg)):     # Pegua todos os objetos
                    lg[i] = lg[i].Retorno()   # usa a Função Retorno de todos

            return (True, lg)    # retorna a lista


        self.Bellman_Ford_Var = {} # guarda as variaveis utilizadas em Bellman_Ford

        self.Bellman_Ford_Var['B'] = {i.rotulo:float('inf') for i in self.vertices} # Betas de cada vertice (Começão em float('inf'))
        self.Bellman_Ford_Var['B'][Inicio] = 0                                # O Beta do inicio começa em 0
        self.Bellman_Ford_Var['P'] = {i.rotulo:{} for i in self.vertices}       # pi's de cada vertice (começão em [])
        self.Bellman_Ford_Var['P'][Inicio] = {Inicio:None}                           # o inicio não tem pi
        self.Bellman_Ford_Var['Root'] = Inicio              # Guada o Root
        self.Bellman_Ford_Var['Vertices'] = {i.rotulo:i for i in self.vertices}
        
        for i in range(len(self.vertices)):   # roda o código N vezes sendo N a quantidade de Vertices 
            if Ciclo():continue       # Caso algum Beta tenha mudado continue
            return Finalizar()    # se não, return Finalizar()
        
        return (False,"Ciclo Negativo") # caso depois de N vezes o Beta Continuar mudando então, existe um ciclo negativo no grafo
