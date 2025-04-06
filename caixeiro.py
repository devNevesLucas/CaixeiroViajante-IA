import random
import math
import copy

DOMINIO = {
    0: (5, 10),
    1: (15, 25),
    2: (30, 5),
    3: (40, 20),
    4: (20, 40),
    5: (35, 35),
    6: (10, 30),
    7: (50, 45),
    8: (45, 10),
    9: (60, 30),
    10: (25, 15),
    11: (55, 20),
    12: (70, 10),
    13: (80, 25),
    14: (65, 40),
    15: (90, 30),
    16: (75, 50),
    17: (85, 15),
    18: (95, 35),
    19: (40, 50),
    20: (10, 5),
    21: (20, 25),
    22: (35, 10),
    23: (50, 15),
    24: (60, 5),
    25: (70, 20),
    26: (30, 50),
    27: (45, 25),
    28: (55, 35),
    29: (65, 15)
}

IDS_DOMINIO = {
    (5, 10): 0, 
    (15, 25): 1, 
    (30, 5): 2, 
    (40, 20): 3, 
    (20, 40): 4, 
    (35, 35): 5, 
    (10, 30): 6, 
    (50, 45): 7, 
    (45, 10): 8, 
    (60, 30): 9, 
    (25, 15): 10, 
    (55, 20): 11, 
    (70, 10): 12, 
    (80, 25): 13, 
    (65, 40): 14, 
    (90, 30): 15, 
    (75, 50): 16, 
    (85, 15): 17, 
    (95, 35): 18, 
    (40, 50): 19, 
    (10, 5): 20, 
    (20, 25): 21, 
    (35, 10): 22, 
    (50, 15): 23, 
    (60, 5): 24, 
    (70, 20): 25, 
    (30, 50): 26, 
    (45, 25): 27, 
    (55, 35): 28, 
    (65, 15): 29
}

class Rota:
    def __init__(self, caixeiros=None, cidades_visitadas=None):
        self.base = (30, 30)
        self.cidades_visitadas = []
        self.distancia_total = 0
        self.caixeiros = [[], [], []]


        if caixeiros is None:     
            for i in range(15):
                # Obtem o index do caixeiro
                caixeiro = random.choice(range(0, 3))
                
                # Obtem as cidades que não foram visitadas ainda
                opcoes_disponiveis = set(range(30)) - set(self.cidades_visitadas)
                
                cidade = random.choice(list(opcoes_disponiveis))
                
                self.caixeiros[caixeiro].append(DOMINIO[cidade])
                
                self.cidades_visitadas.append(cidade)
        
        else:
            self.caixeiros = copy.deepcopy(caixeiros)
            self.cidades_visitadas = copy.deepcopy(cidades_visitadas)

    def fitness(self):
        
        distancia = 0
        
        for caixeiro in self.caixeiros:
            
            for i in range(len(caixeiro)):
                
                if i == 0:
                    distancia += self._calcular_distancia(self.base, caixeiro[i])
                    continue
                
                if i == len(caixeiro) - 1:
                    distancia += self._calcular_distancia(caixeiro[i], self.base)
                    continue
            
                distancia += self._calcular_distancia(caixeiro[i], caixeiro[i + 1])
        
        self.distancia_total = distancia
        
        return distancia
    
    
    def _calcular_distancia(self, ponto_atual: tuple, ponto_seguinte: tuple):
        
        x_quadratico = (ponto_seguinte[0] - ponto_atual[0])**2
        y_quadratico = (ponto_seguinte[1] - ponto_atual[1])**2
        
        distancia = math.sqrt((x_quadratico + y_quadratico))
        
        return distancia


    def mutacao(self, max_mutacoes=10):
        
        casos = [
                self._mutacao_cidade_entre_caixeiros,
                self._mutacao_cidades_do_mesmo_caixeiro,
                self._mutacao_cidade_fora_do_gene 
            ]
        
        qtd_mutacoes = random.choice(range(0, max_mutacoes))
    
        for i in range(qtd_mutacoes):    
            caso_escolhido = random.choice(range(0, len(casos)))        
            casos[caso_escolhido]()
        
        return self
    
    @staticmethod
    def crossover(rotaA, rotaB):
        
        caixeiros = [[], [], []]
        cidades_visitadas = []
        
        for i in range(2):
            caixeiros[i] = rotaA.caixeiros[i]
            cidades_visitadas += [IDS_DOMINIO[cidade] for cidade in caixeiros[i]]
        
        cidades_rotaB = []
        cidades_rotaB += rotaB.caixeiros[0] + rotaB.caixeiros[1] + rotaB.caixeiros[2]
        
        for cidade in cidades_rotaB:
            
            if len(cidades_visitadas) == 15:
                break;

            if IDS_DOMINIO[cidade] not in cidades_visitadas:
                caixeiros[2].append(cidade)
                cidades_visitadas.append(IDS_DOMINIO[cidade])    
                
        return Rota(caixeiros, cidades_visitadas)
    

    def _mutacao_cidade_entre_caixeiros(self):
        
        caixeiro_A = random.choice(range(0, 3))        
        caixeiros_disponiveis = []
        
        if len(self.caixeiros[caixeiro_A]) == 0:            
            caixeiros_disponiveis = set(range(3)) - set([caixeiro_A])            
            caixeiro_A = random.choice(list(caixeiros_disponiveis))    
        
        caixeiros_disponiveis = set(range(3)) - set([caixeiro_A])        
        caixeiro_B = random.choice(list(caixeiros_disponiveis))
        
        if len(self.caixeiros[caixeiro_B]) == 0:
            caixeiros_disponiveis = set(range(3)) - set([caixeiro_A, caixeiro_B])
            caixeiro_B = random.choice(list(caixeiros_disponiveis))
        
        index_A = random.choice(range(0, len(self.caixeiros[caixeiro_A])))
        index_B = random.choice(range(0, len(self.caixeiros[caixeiro_B])))
        
        cidade_temporaria = self.caixeiros[caixeiro_A][index_A]
        
        self.caixeiros[caixeiro_A][index_A] = self.caixeiros[caixeiro_B][index_B]
        self.caixeiros[caixeiro_B][index_B] = cidade_temporaria
        
        
    def _mutacao_cidades_do_mesmo_caixeiro(self):
            
        caixeiro = random.choice(range(0, 3))
        
        if len(self.caixeiros[caixeiro]) < 2:
            caixeiros_disponiveis = set(range(3)) - set([caixeiro])
            caixeiro = random.choice(list(caixeiros_disponiveis))
            
        index_A = random.choice(range(0, len(self.caixeiros[caixeiro])))
        
        indexes_disponiveis = set(range(0, len(self.caixeiros[caixeiro]))) - set([index_A])
        
        index_B = random.choice(list(indexes_disponiveis))
        
        cidade_temporaria = self.caixeiros[caixeiro][index_A]
        
        self.caixeiros[caixeiro][index_A] = self.caixeiros[caixeiro][index_B]
        self.caixeiros[caixeiro][index_B] = cidade_temporaria
        
        
    def _mutacao_cidade_fora_do_gene(self):
        
        caixeiro = random.choice(range(0, 3))
        
        if len(self.caixeiros[caixeiro]) < 2:
            caixeiros_disponiveis = set(range(3)) - set([caixeiro])
            caixeiro = random.choice(list(caixeiros_disponiveis))
            
        index = random.choice(range(0, len(self.caixeiros[caixeiro])))
        
        index_dominio = list(DOMINIO.values()).index(self.caixeiros[caixeiro][index])
        
        self.cidades_visitadas.remove(index_dominio)
        
        opcoes_disponiveis = set(range(30)) - set(self.cidades_visitadas)
            
        nova_cidade = random.choice(list(opcoes_disponiveis))
        
        self.caixeiros[caixeiro][index] = DOMINIO[nova_cidade]        
        self.cidades_visitadas.append(nova_cidade)
        
        
    def imprime(self):
        print(f"Distancia atual: {self.distancia_total}")
        
    
    def imprimir_rota_final(self):
        print("Rota final:")
        
        icones_caixeiros = ["🚚", "🚛", "🚐"]
        icones_cidades = ["🌉", "🌃", "🌆", "🏠", "🏭", "🌇"]
        
        frase_impressa = ""
        
        for i in range(len(self.caixeiros)):
            frase_impressa = f"Caixeiro {i + 1} {icones_caixeiros[i]}: "    
            
            frase_impressa += "Base.(30, 30) 🏬 -> "
        
            for cidade in self.caixeiros[i]:
                icone_cidade = random.choice(icones_cidades)
                
                frase_impressa += f"{IDS_DOMINIO[cidade]}.{cidade} {icone_cidade} -> "
        
            frase_impressa += "Base.(30, 30) 🏬"
        
            print(frase_impressa)
            
        print(f"Distância total: {self.fitness()}")
        
        
class Populacao:
  def __init__(self, tamanho_populacao=10):
    self.tamanho_populacao = tamanho_populacao
    self.populacao = []
    self.fitness = 0
    
    for i in range(self.tamanho_populacao):
      self.populacao.append(Rota())     

  def mutacao(self):
    nova_lista = []
    
    for individuo in self.populacao: 
      nova_lista.append((Rota(individuo.caixeiros, individuo.cidades_visitadas)).mutacao())
      
    return nova_lista

  def crossover(self):
    nova_lista = []
    
    for i in range(0, self.tamanho_populacao, 2):
      nova_lista.append(Rota.crossover(self.populacao[i], self.populacao[i + 1]))
  
    return nova_lista

  def selecionar(self, populacao1 = [], populacao2 = []):
    
    self.populacao.extend(populacao1)
    self.populacao.extend(populacao2)
    
    nova_lista = sorted(self.populacao, key=self._fitness_populacao)
    
    self.populacao = nova_lista[0:self.tamanho_populacao]

  def top_fitness(self):
    return self.top_individuo().fitness()

  def top_individuo(self):
    return self.populacao[0]

  def _fitness_populacao(self, individuo):
    return individuo.fitness()


class AlgoritmoGeneticoPopulacao:
  def __init__(self, populacao):
    self.populacao = populacao
    self.erro = float('inf')
    self.geracoes = 1

  def erro_final(self):
    return self.erro

  def qtd_geracoes(self):
    return self.geracoes

  def rodar(self, max_geracoes = 1000, imprimir_em_geracaoes = 100, erro_min = 150):
  
    while True:
      if self.geracoes >= max_geracoes or self.erro <= erro_min:
        print("\n --- Final:\n")
        print(f"Geração: {self.geracoes}, Distancia: {self.erro}")
        break

      populacao_mutada = self.populacao.mutacao()
      populacao_crossover = self.populacao.crossover()

      self.populacao.selecionar(populacao_mutada, populacao_crossover)
      fitness = self.populacao.top_fitness()

      if fitness <= self.erro:
        self.erro = fitness

      self.geracoes += 1
      if self.geracoes % imprimir_em_geracaoes == 0:
        print(f"Geração: {self.geracoes}, Distancia: {self.erro}")
              
    return self.populacao.top_individuo()

populacao = Populacao()

algoritmoGenetico = AlgoritmoGeneticoPopulacao(populacao)

individuo_max = algoritmoGenetico.rodar()

individuo_max.imprimir_rota_final()
