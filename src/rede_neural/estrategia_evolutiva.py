import json, numpy, os, copy, torch
from random import randint, uniform
from .rede_neural import RedeNeural

class GerenciadorNeural:
    def __init__(self, matches_by_generation, max_generations_history, elitism, mutation_rate, layer_settings, layer_functions, bias):
        
        self.matches_by_generation = matches_by_generation
        self.generation_counter = 0
        self.matches_counter = 0
        self.max_generations_history = max_generations_history

        self.elitism = elitism
        self.mutation_rate = mutation_rate
        self.biases = bias #######################
        self.best_record = 0
        
        self.layer_settings = layer_settings
        self.layer_functions = layer_functions

        self.network_dominance = []
        
        self.best_agent = None

        self.all_networks = []
        self.current_generation: list[RedeNeural] = []
        self.generation_archive = []
    
    def new_match(self, number_of_players):

        self.matches_counter += 1 # registra a conclusão de uma partida
        if self.matches_counter > self.matches_by_generation:# se as partidas da geração acabaram, cria a nova geração

            # registra que uma geração foi completa
            self.generation_counter += 1
            self.matches_counter = 1

            self.compute_generation()
            self.crossover_networks(number_of_players)
            self.apply_mutation()

        elif self.matches_counter == 1 and self.generation_counter == 0: # se for a primeira partida da primeira geração, cria a geração inicial
            self.start_generation(number_of_players)
        
    def start_generation(self, number_of_players):
        self.current_generation = [0] * number_of_players

        for agent in range(number_of_players):
            self.current_generation[agent] = RedeNeural(self.layer_settings, self.layer_functions, self.biases, agent)
            self.current_generation[agent].start_neural_network()
    
    def compute_generation(self):
        self.all_networks = []

        self.generation_archive.append(self.current_generation)
        if len(self.generation_archive) > self.max_generations_history:
            self.generation_archive.pop(0)

        for generation in self.generation_archive:
            self.all_networks.extend(generation)
        
        for agente in range(len(self.current_generation)):
            self.current_generation[agente].reward /= self.matches_by_generation

            if self.current_generation[agente].reward > self.best_record:
                self.best_record = self.current_generation[agente].reward
                self.best_agent = self.current_generation[agente]
    
    def get_generation_metrics(self):

        generation_metrics: dict[str, float] = {
            'best_score': 0,
            'average_score': 0,
        }

        sum_of_scores = 0

        for agent in range(len(self.current_generation)):
            self.current_generation[agent].reward /= self.matches_by_generation

            sum_of_scores += self.current_generation[agent].reward

            if self.current_generation[agent].reward > generation_metrics['best_score'] or generation_metrics['best_score'] == 0:
                generation_metrics['best_score'] = self.current_generation[agent].reward

        generation_metrics['average_score'] = sum_of_scores / len(self.current_generation)
        
        return generation_metrics
    
    def crossover_networks(self, numero_players: int):
        self.current_generation = [0] * numero_players 

        self.network_dominance = self.calculate_network_dominance()

        for index in range(numero_players):
            if index < numero_players * self.elitism:
                self.current_generation[index] = RedeNeural(self.layer_settings, self.layer_functions, self.biases, index)
                self.current_generation[index].layers = copy.deepcopy(self.best_agent.layers)
                self.current_generation[index].initialize_tensors()
            else:
                roullete1 = self.roullete()
                roullete2 = self.roullete()

                chosen_insertion_layer = randint(0, len(self.best_agent.layers) - 1)
                chosen_insertion_neuron = randint(0, len(self.best_agent.layers[chosen_insertion_layer]) - 1)
                
                cross_networks = RedeNeural(self.layer_settings, self.layer_functions, self.biases, index)
                for layer in range(len(self.best_agent.layers)):
                    for neuron in range(len(self.best_agent.layers[layer])):
                        if layer < chosen_insertion_layer or (layer == chosen_insertion_layer and neuron < chosen_insertion_neuron):
                            cross_networks.layers[layer][neuron] = copy.deepcopy(self.all_networks[roullete1].layers[layer][neuron])
                        else:
                            cross_networks.layers[layer][neuron] = copy.deepcopy(self.all_networks[roullete2].layers[layer][neuron])

                self.current_generation[index] = cross_networks
                self.current_generation[index].initialize_tensors()
    
    def has_save_model(self):
        return False

    def load_model(self, path: str = "recursos/saves/save_model.json"):

        if os.path.exists(path):
            with open(path, 'r') as arquivo:
                dada = json.load(arquivo)

                self.generation_counter = dada['generation_counter']

                num_networks = len(dada['networks'])

                self.layer_settings = dada['layer_settings']
                if self.layer_settings != self.layer_settings:
                    print("A rede neural do modelo salvo é diferente da atual")
                    return
                
                self.current_generation = [0] * num_networks
                for network in range(num_networks):
                    self.current_generation[network] = RedeNeural(self.layer_settings, self.layer_functions, self.biases, network)
                    self.current_generation[network].layers = dada['networks'][network]
                    self.current_generation[network].initialize_tensors()
                
        else:
            print("Arquivo não encontrado")
            return 
    
    def calculate_network_dominance(self):

        all_networks_size = len(self.all_networks)
        total_rewards = 0.0
        accumulated_value = 0.0

        proportional_values = all_networks_size * [0.0]

        for index in range(all_networks_size):
            total_rewards += self.all_networks[index].reward
        
        for i in range(all_networks_size):
            proportional_values[i] = (self.all_networks[i].reward / total_rewards) + accumulated_value
            accumulated_value = proportional_values[i]

        return proportional_values

    def apply_mutation(self):

        # randomizando cada peso de acordo com a taxa de mutação
        for agent in range(len(self.current_generation)):
            if agent == 0: # o melhor agente não sofre mutação
                continue

            for layer in range(len(self.best_agent.layers)):
                for neuron in range(len(self.best_agent.layers[layer])):
                    for weight in range(len(self.best_agent.layers[layer][neuron])):
            
                        # quanto maior a taxa de mutação, mais provavel é a alteração
                        if uniform(0, 1) <= self.mutation_rate:
                            self.current_generation[agent].layers[layer][neuron][weight] = uniform(-1, 1)
    
    def get_nn(self, index):

        if len(self.current_generation) > 0:

            if index < len(self.current_generation):
                return self.current_generation[index]
            
            return self.current_generation[randint(0, len(self.current_generation) - 1)]

        network = RedeNeural(self.layer_settings, self.layer_functions, self.biases, index)
        network.start_neural_network()
        network.initialize_tensors()

        return network
    
    def account_agent(self, agent: RedeNeural):
        if agent:
            self.current_generation[agent.index].increment_reward(agent.reward)

    def save_generation(self, path: str = "recursos/saves/save_model.json"):
        
        try:
            with open(path, 'w') as file:
                data = {
                    'generation_counter': self.generation_counter,
                    'layer_settings': self.layer_settings,
                    'networks': [agent.layers for agent in self.current_generation]
                }
                json.dump(data, file)

        except Exception as e:
            print(e)

    def roullete(self):

        left_index = 0
        right_index = len(self.network_dominance) - 1

        sorted_number = uniform(0, 1)

        while left_index < right_index:
            mid_index = left_index + (right_index - left_index) // 2

            if self.network_dominance[mid_index] < sorted_number:
                left_index = mid_index + 1
            else:
                right_index = mid_index

        return left_index