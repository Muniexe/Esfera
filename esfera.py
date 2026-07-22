import pygame
import math
import sys

# ==========================================
# INICIALIZAÇÃO
# ==========================================

pygame.init()

LARGURA = 1000
ALTURA = 700

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption(
    "Esfera 3D - Controle pelo Mouse"
)

# ==========================================
# FONTE
# ==========================================

fonte = pygame.font.SysFont(
    "consolas",
    16,
    bold=True
)

# ==========================================
# RELÓGIO
# ==========================================

clock = pygame.time.Clock()

# ==========================================
# CARACTERES
# ==========================================

CARACTERES = ".,-~:;=!*#$@"

# ==========================================
# ESFERA
# ==========================================

RAIO = 200

DISTANCIA_CAMERA = 600

# ==========================================
# ROTAÇÃO
# ==========================================

angulo_y = 0.0
angulo_x = 0.0

# Sensibilidade do mouse
SENSIBILIDADE = 0.01

# ==========================================
# MOUSE
# ==========================================

arrastando = False

mouse_anterior_x = 0
mouse_anterior_y = 0


# ==========================================
# DESENHAR ESFERA
# ==========================================

def desenhar_esfera():

    global angulo_x
    global angulo_y

    # ======================================
    # Z-BUFFER
    # ======================================

    zbuffer = {}

    # ======================================
    # PRÉ-CALCULAR SENO E COSSENO
    # ======================================

    cos_y = math.cos(angulo_y)
    sin_y = math.sin(angulo_y)

    cos_x = math.cos(angulo_x)
    sin_x = math.sin(angulo_x)

    # ======================================
    # PONTOS DA ESFERA
    # ======================================

    for theta in range(0, 360, 3):

        for phi in range(-90, 90, 3):

            # Converter para radianos

            t = math.radians(theta)
            p = math.radians(phi)

            # ==================================
            # COORDENADAS 3D
            # ==================================

            x = (
                RAIO
                * math.cos(p)
                * math.cos(t)
            )

            y = (
                RAIO
                * math.sin(p)
            )

            z = (
                RAIO
                * math.cos(p)
                * math.sin(t)
            )

            # ==================================
            # ROTAÇÃO Y
            # ==================================

            x2 = (
                x * cos_y
                - z * sin_y
            )

            z2 = (
                x * sin_y
                + z * cos_y
            )

            # ==================================
            # ROTAÇÃO X
            # ==================================

            y2 = (
                y * cos_x
                - z2 * sin_x
            )

            z3 = (
                y * sin_x
                + z2 * cos_x
            )

            # ==================================
            # PERSPECTIVA
            # ==================================

            if (
                DISTANCIA_CAMERA
                + z3
                <= 0
            ):
                continue

            escala = (
                DISTANCIA_CAMERA
                /
                (
                    DISTANCIA_CAMERA
                    + z3
                )
            )

            # ==================================
            # POSIÇÃO NA TELA
            # ==================================

            tela_x = int(
                x2 * escala
                + LARGURA / 2
            )

            tela_y = int(
                y2 * escala
                + ALTURA / 2
            )

            # ==================================
            # LIMITES
            # ==================================

            if not (
                0 <= tela_x < LARGURA
                and
                0 <= tela_y < ALTURA
            ):
                continue

            # ==================================
            # Z-BUFFER
            # ==================================

            chave = (
                tela_x,
                tela_y
            )

            if chave in zbuffer:

                if zbuffer[chave] > z3:
                    continue

            zbuffer[chave] = z3

            # ==================================
            # ILUMINAÇÃO
            # ==================================

            # Direção da luz

            luz_x = -0.5
            luz_y = -0.5
            luz_z = -1.0

            iluminacao = (
                x2 * luz_x
                + y2 * luz_y
                + z3 * luz_z
            )

            # Normalizar

            iluminacao /= RAIO

            # Limitar

            iluminacao = max(
                0,
                min(
                    1,
                    iluminacao
                )
            )

            # ==================================
            # ESCOLHER CARACTERE
            # ==================================

            indice = int(
                iluminacao
                *
                (
                    len(CARACTERES)
                    - 1
                )
            )

            indice = max(
                0,
                min(
                    indice,
                    len(CARACTERES)
                    - 1
                )
            )

            caractere = CARACTERES[
                indice
            ]

            # ==================================
            # DESENHAR CARACTERE
            # ==================================

            texto = fonte.render(
                caractere,
                True,
                (
                    255,
                    255,
                    255
                )
            )

            tela.blit(
                texto,
                (
                    tela_x,
                    tela_y
                )
            )


# ==========================================
# LOOP PRINCIPAL
# ==========================================

rodando = True

while rodando:

    # ======================================
    # EVENTOS
    # ======================================

    for evento in pygame.event.get():

        # Fechar janela

        if evento.type == pygame.QUIT:

            rodando = False

        # ==================================
        # MOUSE PRESSIONADO
        # ==================================

        if (
            evento.type
            == pygame.MOUSEBUTTONDOWN
        ):

            if evento.button == 1:

                arrastando = True

                mouse_anterior_x = evento.pos[0]
                mouse_anterior_y = evento.pos[1]

        # ==================================
        # MOUSE SOLTO
        # ==================================

        if (
            evento.type
            == pygame.MOUSEBUTTONUP
        ):

            if evento.button == 1:

                arrastando = False

        # ==================================
        # MOVIMENTO DO MOUSE
        # ==================================

        if (
            evento.type
            == pygame.MOUSEMOTION
        ):

            if arrastando:

                mouse_x = evento.pos[0]
                mouse_y = evento.pos[1]

                # Diferença do movimento

                delta_x = (
                    mouse_x
                    - mouse_anterior_x
                )

                delta_y = (
                    mouse_y
                    - mouse_anterior_y
                )

                # ==================================
                # ROTACIONAR ESFERA
                # ==================================

                angulo_y += (
                    delta_x
                    * SENSIBILIDADE
                )

                angulo_x += (
                    delta_y
                    * SENSIBILIDADE
                )

                # ==================================
                # LIMITAR ROTAÇÃO VERTICAL
                # ==================================

                angulo_x = max(
                    -math.pi / 2,
                    min(
                        math.pi / 2,
                        angulo_x
                    )
                )

                # Atualizar posição anterior

                mouse_anterior_x = mouse_x
                mouse_anterior_y = mouse_y

    # ======================================
    # LIMPAR TELA
    # ======================================

    tela.fill(
        (
            0,
            0,
            0
        )
    )

    # ======================================
    # DESENHAR
    # ======================================

    desenhar_esfera()

    # ======================================
    # ATUALIZAR
    # ======================================

    pygame.display.flip()

    # ======================================
    # FPS
    # ======================================

    clock.tick(60)


# ==========================================
# ENCERRAR
# ==========================================

pygame.quit()

sys.exit()