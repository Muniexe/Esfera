# Esfera 3D ASCII

Esse é um projeto que fiz em Python usando Pygame, onde criei uma esfera 3D formada por caracteres.

A ideia do projeto é estudar um pouco de matemática 3D e entender como funciona a renderização de objetos em 3D.

A esfera pode ser movimentada usando o mouse, segurando o botão esquerdo e arrastando.

## Como funciona

A esfera é formada por vários pontos em um espaço 3D.

Cada ponto possui uma posição nos eixos X, Y e Z. Depois, esses pontos são rotacionados e transformados para aparecerem na tela em 2D.

Também existe um sistema simples de iluminação que escolhe diferentes caracteres dependendo da posição do ponto em relação à luz.

Os caracteres utilizados são:

```text
.,-~:;=!*#$@
