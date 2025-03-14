import pygame
import json
import socket

class Game:

    def __init__(self, client_socket):
        pygame.init()

        # tela
        self.WIDTH, self.HEIGHT = 800, 600
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Trivia")
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT = pygame.font.Font("C:\\Users\\gabit\\socket-redes\\src\\Kathen Font by Situjuh (7NTypes).otf", 36)
        
       # Inicialize os botões com valores específicos
        button_width = 100
        button_height = 50
        button_color = (100, 100, 100)

        self.botao_a = self.Button(50, 200, button_width, button_height, "A", button_color, self.enviar_resposta_a)
        self.botao_b = self.Button(200, 200, button_width, button_height, "B", button_color, self.enviar_resposta_b)
        self.botao_c = self.Button(50, 300, button_width, button_height, "C", button_color, self.enviar_resposta_c)
        self.botao_d = self.Button(200, 300, button_width, button_height, "D", button_color, self.enviar_resposta_d)


        # variável global para a pergunta atual
        self.perguntas = []  # Lista de perguntas do arquivo JSON
        self.pergunta_atual = None

        # client socket aqui
        self.clientSocket = client_socket

        # Carregar as perguntas do arquivo JSON
        with open('trivia.json', 'r') as file:
            self.perguntas = json.load(file)

        # Iniciar o jogo (exibir a primeira pergunta)
        self.iniciar_jogo()
    
    def iniciar_jogo(self):
        # Verifique se há perguntas disponíveis
        if self.perguntas:
            # Pegue a primeira pergunta
            self.pergunta_atual = self.perguntas[0]
            # Remova a pergunta da lista
            del self.perguntas[0]

            # Exiba a primeira pergunta na tela
            self.display_pergunta()
        else:
            # Não há mais perguntas, encerre o jogo
            self.quit_game()

    # FUNCAO exibir a pergunta
    def display_pergunta(self):
        self.SCREEN.fill(self.WHITE)  # Limpar a tela
        texto_pergunta = self.FONT.render(self.pergunta_atual['pergunta'], True, self.BLACK)
        self.SCREEN.blit(texto_pergunta, (50, 50))

    # FUNCAO enviar RESPOSTA
    def enviar_resposta(self, resposta):
        self.clientSocket.send(resposta.encode())

    # FUNCAO atualizar pergunta
    def atualizar_pergunta(self):
        pergunta = self.clientSocket.recv(1024).decode()
        if not pergunta:
            self.clientSocket.close()
            pygame.quit()
            quit()
        else:
            self.pergunta_atual = json.loads(pergunta)
            self.display_pergunta()

    # Conectando-se e exibindo a primeira pergunta
    def iniciar_jogo(self):
        self.atualizar_pergunta()

    class Button:
        def __init__(self, x, y, width, height, text, color, action=None):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.color = color
            self.action = action

        def draw(self, screen, outline=None):
            if outline:
                pygame.draw.rect(screen, outline, self.rect, 0)
            pygame.draw.rect(screen, self.color, self.rect, 2)
            if self.text != "":
                font = pygame.font.Font(None, 36)
                text = font.render(self.text, True, (0, 0, 0))
                screen.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.centery - text.get_height() // 2))

        def click(self):
            if self.action:
                self.action()

    def enviar_resposta_a(self):
        self.enviar_resposta('A')

    def enviar_resposta_b(self):
        self.enviar_resposta('B')

    def enviar_resposta_c(self):
        self.enviar_resposta('C')

    def enviar_resposta_d(self):
        self.enviar_resposta('D')

    def run_game(self):
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botão esquerdo do mouse
                        pos = pygame.mouse.get_pos()
                        if self.botao_a.rect.collidepoint(pos):
                            self.enviar_resposta_a()
                        elif self.botao_b.rect.collidepoint(pos):
                            self.enviar_resposta_b()
                        elif self.botao_c.rect.collidepoint(pos):
                            self.enviar_resposta_c()
                        elif self.botao_d.rect.collidepoint(pos):
                            self.enviar_resposta_d()

            # Aqui você pode adicionar mais lógica do jogo, como atualização de estado, verificação de vitória/derrota, etc.

            # Atualize a tela
            self.SCREEN.fill(self.WHITE)
            self.display_pergunta()
            self.botao_a.draw(self.SCREEN)
            self.botao_b.draw(self.SCREEN)
            self.botao_c.draw(self.SCREEN)
            self.botao_d.draw(self.SCREEN)
            pygame.display.flip()


    def quit_game(self):
        pygame.quit()
