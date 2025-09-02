import torch, numpy
import torch.nn.functional as F
from random import uniform

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

ActivationType = {
    'sigmoid': F.sigmoid,
    'relu': F.relu,
    'tanh': F.tanh,
    'leaky_relu': F.leaky_relu
}

class RedeNeural:
    def __init__(self, layer_settings, layer_functions, biases, index):

        self.input = []

        self.layer_settings = layer_settings
        self.layer_functions = layer_functions

        self.index = index
        self.reward = 0
        self.activation_threshold = self.get_activation_threshold()
        
        self.layers = [] # variavel onde vão ser colocados os pesos 
        self.tensors = [] # variavel onde vão ser colocados os pesos em tensores
        self.biases = [torch.zeros(self.layer_settings[i], dtype=torch.float16, device=device) for i in range(1, len(self.layer_settings))] # cria um bias para cada camada exceto a de entrada
        
        # cria a estrutura de layers com base nas configurações definidas
        for camada in range(1, len(self.layer_settings)):  # 1 porque a primeira camada é  de entrada inicial
            self.layers.append([numpy.array([0] * self.layer_settings[camada - 1], dtype=float) for neuronio in range(self.layer_settings[camada])])

    # função utilizada para criar a primeira geração
    def start_neural_network(self):
        self.layers = [ [ [uniform(-1, 1) for peso in range(len(neuronio))] for neuronio in camada] for camada in self.layers]
        self.initialize_tensors()

    def initialize_tensors(self):
        self.tensors = [torch.tensor(camada, dtype=torch.float16, device=device) for camada in self.layers]

    # seleciona a função de ativação de acordo com a configuração
    def apply_activation(self, tensor, tipo: str):

        func = ActivationType[tipo]
        return func(tensor)
    
    # retorna o valor mínimo para ativar o neuronio de acordo com a função de ativação
    def get_activation_threshold(self):
        
        if self.layer_functions[-1] in ['relu', 'tanh', 'leaky_relu']:
            return 0
    
        elif self.layer_functions[-1] == 'sigmoid':
            return 0.5
    
    def increment_reward(self, value: float):
        self.reward += value
    
    def set_input(self, input):
        self.input = input
    

    # atualiza o estado da rede a cada iteração
    def get_output(self) -> list[float]:

        # armazena o resultado temporario de cada camada
        self.current_network_state = torch.as_tensor(self.input, dtype=torch.float16, device=device)

        # Faz todos os calculos de cada camada e armazena em current_network_state 
        for camada in range(1, len(self.layer_settings)):
            linear_output  = F.linear(self.current_network_state , self.tensors[camada - 1], self.biases[camada - 1])
            self.current_network_state  = self.apply_activation(linear_output , self.layer_functions[camada - 1])

        # retorna a saída da rede como uma lista
        return self.current_network_state.tolist()