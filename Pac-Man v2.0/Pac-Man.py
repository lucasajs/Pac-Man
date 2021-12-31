import pygame
from abc import ABCMeta, abstractmethod
from random import choice

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
fonte = pygame.font.SysFont('arial', 28, True, False)

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (10, 16, 204)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
LARANJA = (255, 140, 0)
ROSA = (255, 15, 192)
CIANO = (0, 255, 255)
VELOCIDADE = 1
CIMA = 1
BAIXO = 2
DIR = 3
ESQ = 4


class Elementos(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def cal_Rules(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass

class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    def esquina(self, direcoes):
        pass


class Cenario(Elementos):
    def __init__(self, tamanho, pac):
        self.pacman = pac
        self.moviveis = []
        self.tamanho = tamanho
        self.pontos = 0
        # Estados: 0: Jogando; 1: Pausado; 2: Game Over; 3: Vitoria
        self.estado = 0
        self.vidas = 3
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 0, 0, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 0, 0, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)

    def pintar_pontos(self, tela):
        pontos_x = 30 * self.tamanho
        img_pontos = fonte.render(f'SCORE: {self.pontos}', True, AMARELO)
        img_vidas = fonte.render(f'LIVES: {self.vidas}', True, AMARELO)
        tela.blit(img_pontos, (pontos_x, 45))
        tela.blit(img_vidas, (pontos_x, 95))

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = int(self.tamanho / 2)
            cor = PRETO
            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, BRANCO, (x + half, y + half), int(self.tamanho / 10), 0)

    def pintar(self, tela):
        if self.estado == 0:
            self.pintar_jogando(tela)
        elif self.estado == 1:
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == 2:
            self.pintar_jogando(tela)
            self.pintar_GameOver(tela)
        elif self.estado == 3:
            self.pintar_jogando(tela)
            self.pintar_Win(tela)

    def pintar_texto_centro(self, tela, texto):
        text_img = fonte.render(texto, True, AMARELO)
        text_x = int((tela.get_width() - text_img.get_width()) / 2)
        text_y = int((tela.get_width() - text_img.get_width()) / 2)
        tela.blit(text_img, (text_x, text_y))

    def pintar_Win(self, tela):
        self.pintar_texto_centro(tela, 'Y O U  W I N !!!')

    def pintar_GameOver(self, tela):
        self.pintar_texto_centro(tela, 'G A M E  O V E R')

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, 'P A U S E D')

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_pontos(tela)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(CIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(BAIXO)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQ)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIR)
        return direcoes

    def cal_Rules(self):
        if self.estado == 0:
            self.cal_Rules_Play()
        elif self.estado == 1:
            self.cal_Rules_Pause()
        elif self.estado == 2:
            self.cal_Rules_GameOver()
        elif self.estado == 3:
            self.cal_Rules_Win()

    def cal_Rules_Win(self):
        pass

    def cal_Rules_GameOver(self):
        pass

    def cal_Rules_Pause(self):
        pass

    def cal_Rules_Play(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha and \
                    movivel.coluna == self.pacman.coluna:
                self.vidas -= 1
                if self.vidas <= 0:
                    self.estado = 2
                else:
                    self.pacman.linha = 17.0
                    self.pacman.coluna = 13.0
            else:
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and \
                        self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0
                        if self.pontos >= 316:
                            self.estado = 3
                else:
                    movivel.recusar_movimento(direcoes)

    def processar_eventos(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.estado == 0:
                        self.estado = 1
                    else:
                        self.estado = 0


class Pacman(Elementos, Movivel):
    def __init__(self, tamanho):
        self.centro_x = 400
        self.centro_y = 300
        self.coluna = 13.0
        self.linha = 17.0
        self.tamanho = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.raio = int(self.tamanho / 2)
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.boca_abertura = 0
        self.vel_abertura = 1

    def cal_Rules(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def pintar(self, tela):
        # corpo pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio)

        self.boca_abertura += self.vel_abertura
        if self.boca_abertura > self.raio - 5:
            self.vel_abertura = - 2.5
        elif self.boca_abertura <= 0:
            self.vel_abertura = 1

        # boca pacman
        canto_boca = (self.centro_x, self.centro_y)
        labio_sup = (self.centro_x + self.raio, self.centro_y - self.boca_abertura)
        labio_inf = (self.centro_x + self.raio, self.centro_y + self.boca_abertura)
        pontos = [canto_boca, labio_sup, labio_inf]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # olho pacman
        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.60)
        olho_tam = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_tam, 0)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = VELOCIDADE
                elif e.key == pygame.K_LEFT:
                    self.vel_x = - VELOCIDADE
                elif e.key == pygame.K_UP:
                    self.vel_y = - VELOCIDADE
                elif e.key == pygame.K_DOWN:
                    self.vel_y = VELOCIDADE
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass

class Fantasma(Elementos):
    def __init__(self, cor, tamanho):
        self.coluna = 13.0
        self.linha = 10.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.velocidade = 1
        self.direcao = BAIXO
        self.tamanho = tamanho
        self.cor = cor

    def pintar(self, tela):
        fatia = int(self.tamanho / 8)
        pix_x = int(self.coluna * self.tamanho)
        pix_y = int(self.linha * self.tamanho)
        contorno = [(pix_x, pix_y + self.tamanho),
                    (pix_x + fatia, pix_y + fatia * 2),
                    (pix_x + fatia * 2, pix_y + int(fatia / 2)),
                    (pix_x + fatia * 3, pix_y),
                    (pix_x + fatia * 5, pix_y),
                    (pix_x + fatia * 6, pix_y + int(fatia / 2)),
                    (pix_x + fatia * 7, pix_y + fatia * 2),
                    (pix_x + self.tamanho, pix_y + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raioExt = fatia
        olho_raioInt = int(fatia / 2)

        olho_EsqX = int(pix_x + fatia * 2.5)
        olho_EsqY = int(pix_y + fatia * 2.5)

        olho_DirX = int(pix_x + fatia * 5.5)
        olho_DirY = int(pix_y + fatia * 2.5)

        pygame.draw.circle(tela, BRANCO, (olho_EsqX, olho_EsqY), olho_raioExt, 0)
        pygame.draw.circle(tela, PRETO, (olho_EsqX, olho_EsqY), olho_raioInt, 0)
        pygame.draw.circle(tela, BRANCO, (olho_DirX, olho_DirY), olho_raioExt, 0)
        pygame.draw.circle(tela, PRETO, (olho_DirX, olho_DirY), olho_raioInt, 0)

    def cal_Rules(self):
        if self.direcao == CIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == BAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == ESQ:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == DIR:
            self.coluna_intencao += self.velocidade

    def mudar_direcao(self, direcoes):
        self.direcao = choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def processar_eventos(self, events):
        pass


if __name__ == "__main__":
    size = int(650 / 30)
    pacman = Pacman(size)
    blinky = Fantasma(VERMELHO, size)
    inky = Fantasma(CIANO, size)
    clyde = Fantasma(LARANJA, size)
    pinky = Fantasma(ROSA, size)
    cenario = Cenario(size, pacman)
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)

    while True:
        # game rules
        pacman.cal_Rules()
        blinky.cal_Rules()
        inky.cal_Rules()
        clyde.cal_Rules()
        pinky.cal_Rules()
        cenario.cal_Rules()

        # screen
        screen.fill(PRETO)
        cenario.pintar(screen)
        pacman.pintar(screen)
        blinky.pintar(screen)
        inky.pintar(screen)
        clyde.pintar(screen)
        pinky.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

        # events
        eventos = pygame.event.get()
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)
