'''
Made with ⚡by The Purple One :)
https://www.codigoroxo.com.br
Youtube.com/@codigoroxo
'''


import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# Configurações da Tela
LARGURA_TELA = 500
ALTURA_TELA = 800
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Flappy Bird - Codigo Roxo")

ALTURA_CHAO = 660 

# Configurações de sofrimento humanóide
GRAVIDADE_BASE = 0.25
IMPULSO_PULO_BASE = -6
VELOCIDADE_CANO = 25
ESPACO_C_CANOS = 150

# Caminhos dos arquivos
ARQUIVO_FONTE = "./assets/Fonts/flappy-font.ttf" 
ARQUIVO_HIGHSCORE = "highscore.txt"

# Cores do Sistema
BRANCO = (255, 255, 255)
AMARELO_OURO = (255, 215, 0)
CINZA_CLARO = (240, 240, 240)
PRETO = (0, 0, 0)

# Configurações de Texto
FONTE_TITULO = pygame.font.Font(ARQUIVO_FONTE, 55) 
FONTE_PONTOS = pygame.font.Font(ARQUIVO_FONTE, 60) 
FONTE_INTERFACE = pygame.font.Font(ARQUIVO_FONTE, 20) 
FONTE_RECORD = pygame.font.Font(ARQUIVO_FONTE, 25) 

def carregar_highscore():
    if os.path.exists(ARQUIVO_HIGHSCORE):
        try:
            with open(ARQUIVO_HIGHSCORE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def salvar_highscore(novo_recorde):
    try:
        with open(ARQUIVO_HIGHSCORE, "w") as f:
            f.write(str(novo_recorde))
    except Exception as e:
        print(f"Erro ao salvar o high score: {e}")

def carregar_imagem(nome, largura, altura, cor_fallback):
    if os.path.exists(nome):
        img = pygame.image.load(nome).convert_alpha()
        if largura != 0 and altura != 0:
             img = pygame.transform.scale(img, (largura, altura))
        return img
    else:
        w = largura if largura != 0 else 50
        h = altura if altura != 0 else 50
        img = pygame.Surface((w, h), pygame.SRCALPHA)
        img.fill(cor_fallback)
        return img

def carregar_som(caminho, volume=0.3):
    if os.path.exists(caminho):
        som = pygame.mixer.Sound(caminho)
        som.set_volume(volume)
        return som
    return None

IMAGENS_PASSARO = [
    carregar_imagem("./assets/Images/1.png", 50, 45, (255, 255, 0)),
    carregar_imagem("./assets/Images/2.png", 50, 45, (255, 220, 0)),
    carregar_imagem("./assets/Images/3.png", 50, 45, (255, 180, 0)),
    carregar_imagem("./assets/Images/4.png", 50, 45, (255, 220, 0))
]
IMAGEM_FUNDO = carregar_imagem("./assets/Images/fundo.png", LARGURA_TELA, ALTURA_TELA, (0, 191, 255))

IMAGEM_CHAO = carregar_imagem("./assets/Images/chao.png", LARGURA_TELA, ALTURA_TELA, (0, 255, 0))

IMAGENS_MOEDA = [
    carregar_imagem("./assets/Images/coin1.png", 40, 40, (255, 215, 0)),
    carregar_imagem("./assets/Images/coin2.png", 40, 40, (255, 195, 0)),
    carregar_imagem("./assets/Images/coin3.png", 40, 40, (255, 175, 0)),
    carregar_imagem("./assets/Images/coin4.png", 40, 40, (255, 195, 0))
]

LARGURA_REAL_CANO = 90

img_top_original = pygame.image.load("./assets/Images/pipetop.png").convert_alpha()
prop_top = LARGURA_REAL_CANO / img_top_original.get_width()
ALTURA_TOP = int(img_top_original.get_height() * prop_top)
IMAGEM_PIPETOP = pygame.transform.scale(img_top_original, (LARGURA_REAL_CANO, ALTURA_TOP))

img_body_original = pygame.image.load("./assets/Images/pipebody.png").convert_alpha()
prop_body = LARGURA_REAL_CANO / img_body_original.get_width()
ALTURA_BODY = int(img_body_original.get_height() * prop_body)
IMAGEM_PIPEBODY = pygame.transform.scale(img_body_original, (LARGURA_REAL_CANO, ALTURA_BODY))

SFX_MOEDA = carregar_som("./assets/Sfx/coinsfx.mp3", volume=0.15)
SFX_MORTE = carregar_som("./assets/Sfx/ripsfx.mp3", volume=0.20)
SFX_PULO = carregar_som("./assets/Sfx/wingsfx.mp3", volume=0.10)


class Passaro:
    def __init__(self):
        self.x = 100
        self.y = ALTURA_TELA // 2 - 40
        self.velocidade = 0
        self.imagens = IMAGENS_PASSARO
        self.index_imagem = 0
        self.imagem = self.imagens[self.index_imagem]
        self.mask = pygame.mask.from_surface(self.imagem)
        self.tempo_animacao = 5
        self.contador_tempo = 0
        self.angulo = 0
        self.VELOCIDADE_ROTACAO = 2
        self.vivo = True 

    def pular(self, forca_pulo):
        if self.vivo:
            self.velocidade = forca_pulo 
            self.angulo = 15
            if SFX_PULO: 
                SFX_PULO.play()

    def mover(self, gravidade_atual):
        self.velocidade += gravidade_atual
        self.y += int(self.velocidade)
        
        if self.vivo:
            if self.velocidade < 0:
                if self.angulo < 25:
                    self.angulo += 1
            else:
                if self.angulo > -40:
                    self.angulo -= self.VELOCIDADE_ROTACAO
            self.atualizar_animacao()
        else:
            if self.angulo > -80:
                self.angulo -= 5

    def atualizar_animacao(self):
        self.contador_tempo += 1
        if self.contador_tempo >= self.tempo_animacao:
            self.contador_tempo = 0
            if self.angulo <= -45:
                self.index_imagem = 1
            else:
                self.index_imagem = (self.index_imagem + 1) % len(self.imagens)
            self.imagem = self.imagens[self.index_imagem]

    def desenhar(self, tela):
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        rect_original = self.imagem.get_rect(topleft=(self.x, self.y))
        novo_rect = imagem_rotacionada.get_rect(center=rect_original.center)
        self.mask = pygame.mask.from_surface(imagem_rotacionada)
        tela.blit(imagem_rotacionada, novo_rect.topleft)


class Cano:
    def __init__(self, espaco_vao):
        self.x = LARGURA_TELA + 50
        self.espaco_c_canos = espaco_vao
        self.altura_vao = random.randint(120, ALTURA_CHAO - self.espaco_c_canos - 120)
        self.passou = False
        
        self.tem_moeda = random.random() < 0.1 
        self.moeda_coletada = False
        self.moeda_index = 0
        self.moeda_tempo = 6 
        self.moeda_contador = 0
        
        self.moeda_x_offset = (LARGURA_REAL_CANO // 2) - 20 
        self.moeda_y = self.altura_vao + (self.espaco_c_canos // 2) - 20 
        
        self.img_superior = pygame.Surface((LARGURA_REAL_CANO, ALTURA_TELA), pygame.SRCALPHA)
        self.img_inferior = pygame.Surface((LARGURA_REAL_CANO, ALTURA_TELA), pygame.SRCALPHA)
        
        pipetop_invertido = pygame.transform.flip(IMAGEM_PIPETOP, False, True)
        pipebody_invertido = pygame.transform.flip(IMAGEM_PIPEBODY, False, True)

        SOBREPOSICAO = 6

        pos_boca_sup = self.altura_vao - ALTURA_TOP
        self.img_superior.blit(pipetop_invertido, (0, pos_boca_sup))
        
        y_corpo_sup = pos_boca_sup - ALTURA_BODY + SOBREPOSICAO
        while y_corpo_sup + ALTURA_BODY > 0:
            self.img_superior.blit(pipebody_invertido, (0, y_corpo_sup))
            y_corpo_sup -= (ALTURA_BODY - SOBREPOSICAO)

        pos_boca_inf = self.altura_vao + self.espaco_c_canos
        self.img_inferior.blit(IMAGEM_PIPETOP, (0, pos_boca_inf))
        
        y_corpo_inf = pos_boca_inf + ALTURA_TOP - SOBREPOSICAO
        while y_corpo_inf < ALTURA_TELA:
            self.img_inferior.blit(IMAGEM_PIPEBODY, (0, y_corpo_inf))
            y_corpo_inf += (ALTURA_BODY - SOBREPOSICAO)

        self.mask_superior = pygame.mask.from_surface(self.img_superior)
        self.mask_inferior = pygame.mask.from_surface(self.img_inferior)

    def mover(self, velocidade):
        self.x -= velocidade
        if self.tem_moeda and not self.moeda_coletada:
            self.moeda_contador += 1
            if self.moeda_contador >= self.moeda_tempo:
                self.moeda_contador = 0
                self.moeda_index = (self.moeda_index + 1) % len(IMAGENS_MOEDA)

    def desenhar(self, tela):
        tela.blit(self.img_superior, (self.x, 0))
        tela.blit(self.img_inferior, (self.x, 0))
        
        if self.tem_moeda and not self.moeda_coletada:
            img_moeda = IMAGENS_MOEDA[self.moeda_index]
            tela.blit(img_moeda, (self.x + self.moeda_x_offset, self.moeda_y))

    def verificar_colisao(self, passaro):
        passaro_mask = passaro.mask
        offset_superior = (self.x - passaro.x, 0 - passaro.y)
        offset_inferior = (self.x - passaro.x, 0 - passaro.y)

        colisao_sup = passaro_mask.overlap(self.mask_superior, offset_superior)
        colisao_inf = passaro_mask.overlap(self.mask_inferior, offset_inferior)

        return bool(colisao_sup or colisao_inf)

    def verificar_coleta_moeda(self, passaro):
        if self.tem_moeda and not self.moeda_coletada and passaro.vivo:
            img_moeda = IMAGENS_MOEDA[self.moeda_index]
            moeda_mask = pygame.mask.from_surface(img_moeda)
            moeda_x_atual = self.x + self.moeda_x_offset
            offset_moeda = (moeda_x_atual - passaro.x, self.moeda_y - passaro.y)
            
            if passaro.mask.overlap(moeda_mask, offset_moeda):
                self.moeda_coletada = True
                if SFX_MOEDA: 
                    SFX_MOEDA.play()
                return True
        return False


class Piso:
    def __init__(self):
        self.x1 = 0
        self.x2 = LARGURA_TELA
        self.imagem = IMAGEM_CHAO

    def mover(self):
        self.x1 -= VELOCIDADE_CANO
        self.x2 -= VELOCIDADE_CANO
        if self.x1 + LARGURA_TELA <= 0:
            self.x1 = self.x2 + LARGURA_TELA
        if self.x2 + LARGURA_TELA <= 0:
            self.x2 = self.x1 + LARGURA_TELA

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, 0))
        tela.blit(self.imagem, (self.x2, 0))


def desenhar_texto_com_borda(tela, texto, fonte, cor, centro_x, y):
    superficie_texto = fonte.render(texto, True, cor)
    superficie_borda = fonte.render(texto, True, PRETO)
    rect = superficie_texto.get_rect(center=(centro_x, y))
    
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                tela.blit(superficie_borda, (rect.x + dx, rect.y + dy))
                
    tela.blit(superficie_texto, rect.topleft)


def reiniciar_jogo():
    return Passaro(), [Cano(ESPACO_C_CANOS)], 0, Piso()


def main():
    clock = pygame.time.Clock()
    passaro, canos, pontos, piso = reiniciar_jogo()
    highscore = carregar_highscore()
    
    ESTADO_GET_READY = 0
    ESTADO_JOGANDO = 1
    ESTADO_GAME_OVER = 2
    
    estado_jogo = ESTADO_GET_READY
    jogando_loop = True
    contador_piscado = 0 

    while jogando_loop:
        clock.tick(60)
        contador_piscado = (contador_piscado + 1) % 60

        if pontos > highscore:
            highscore = pontos

        # --- TRATAMENTO DE INPUTS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogando_loop = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if estado_jogo == ESTADO_GET_READY:
                        estado_jogo = ESTADO_JOGANDO
                        passaro.velocidade = IMPULSO_PULO_BASE
                        if SFX_PULO: 
                            SFX_PULO.play()
                    elif estado_jogo == ESTADO_JOGANDO:
                        passaro.pular(IMPULSO_PULO_BASE)
                    elif estado_jogo == ESTADO_GAME_OVER:
                        if passaro.y + 35 >= ALTURA_CHAO:
                            passaro, canos, pontos, piso = reiniciar_jogo()
                            estado_jogo = ESTADO_GET_READY

        if estado_jogo == ESTADO_GET_READY:
            passaro.atualizar_animacao()
            piso.mover()
            
        elif estado_jogo == ESTADO_JOGANDO:
            passaro.mover(GRAVIDADE_BASE)
            piso.mover()

            # COLISÃO COM O CHÃO REAL
            if passaro.y + 35 >= ALTURA_CHAO or passaro.y < 0:
                passaro.vivo = False
                if SFX_MORTE: 
                    SFX_MORTE.play()
                estado_jogo = ESTADO_GAME_OVER

            adicionar_cano = False
            for cano in list(canos):
                cano.mover(VELOCIDADE_CANO)
                
                if cano.verificar_colisao(passaro):
                    passaro.vivo = False
                    if SFX_MORTE: 
                        SFX_MORTE.play()
                    estado_jogo = ESTADO_GAME_OVER
                    break

                if cano.verificar_coleta_moeda(passaro):
                    pontos += 10

                if not cano.passou and cano.x < passaro.x:
                    cano.passou = True
                    adicionar_cano = True

                if cano.x < -LARGURA_REAL_CANO:
                    canos.remove(cano)
            
            DISTANCIA_HORIZONTAL = 220 

            # Se o último cano da lista já andou o suficiente para a esquerda, joga o próximo na tela ;)
            if canos[-1].x < LARGURA_TELA - DISTANCIA_HORIZONTAL:
                canos.append(Cano(ESPACO_C_CANOS))

            # A pontuação continua subindo normalmente quando você passa pelo cano
            if adicionar_cano:
                pontos += 1
                
        elif estado_jogo == ESTADO_GAME_OVER:
            if passaro.y + 35 < ALTURA_CHAO:
                passaro.velocidade += GRAVIDADE_BASE
                passaro.y += int(passaro.velocidade)
                if passaro.angulo > -80:
                    passaro.angulo -= 5
            else:
                passaro.y = ALTURA_CHAO - 35
                salvar_highscore(highscore)

        TELA.blit(IMAGEM_FUNDO, (0, 0))
        
        for cano in list(canos):
            cano.desenhar(TELA)
            
        piso.desenhar(TELA) 
        passaro.desenhar(TELA)

        # INTERFACE / HUD
        texto_recorde = FONTE_RECORD.render(f"BEST: {highscore}", True, AMARELO_OURO)
        TELA.blit(texto_recorde, (20, 20))

        if estado_jogo == ESTADO_GET_READY:
            desenhar_texto_com_borda(TELA, "Get Ready", FONTE_TITULO, AMARELO_OURO, LARGURA_TELA // 2, ALTURA_TELA // 2 - 120)
            if contador_piscado < 35: 
                desenhar_texto_com_borda(TELA, "PRESS SPACE TO PLAY", FONTE_INTERFACE, CINZA_CLARO, LARGURA_TELA // 2, ALTURA_TELA // 2 + 120)
                
        elif estado_jogo == ESTADO_JOGANDO:
            desenhar_texto_com_borda(TELA, str(pontos), FONTE_PONTOS, BRANCO, LARGURA_TELA // 2, 80)
            
        elif estado_jogo == ESTADO_GAME_OVER:
            desenhar_texto_com_borda(TELA, "Game Over", FONTE_TITULO, AMARELO_OURO, LARGURA_TELA // 2, ALTURA_TELA // 2 - 120)
            if contador_piscado < 35: 
                desenhar_texto_com_borda(TELA, "PRESS SPACE TO RESTART", FONTE_INTERFACE, CINZA_CLARO, LARGURA_TELA // 2, ALTURA_TELA // 2 + 120)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()