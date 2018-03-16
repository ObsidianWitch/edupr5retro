# Constantes

## Événements

~~~
| Constante       | Attributs
| --------------- | --------------------- |
| General                                 |
| QUIT            | none                  |
| USEREVENT       | code                  |
| --------------- | --------------------- |
| Fenêtre                                 |
| ACTIVEEVENT     | gain, state           |
| VIDEORESIZE     | size, w, h            |
| VIDEOEXPOSE     | none                  |
| --------------- | --------------------- |
| Clavier                                 |
| KEYDOWN         | unicode, key, mod     |
| KEYUP           | key, mod              |
| --------------- | --------------------- |
| Souris                                  |
| MOUSEMOTION     | pos, rel, buttons     |
| MOUSEBUTTONDOWN | pos, button           |
| MOUSEBUTTONUP   | pos, button           |
| --------------- | --------------------- |
| Joystick / Manette                      |
| JOYAXISMOTION   | joy, axis, value      |
| JOYBALLMOTION   | joy, ball, rel        |
| JOYHATMOTION    | joy, hat, value       |
| JOYBUTTONUP     | joy, button           |
| JOYBUTTONDOWN   | joy, button           |

~~~

## Clavier

~~~
| Constante       | Nom                   |
| --------------- | --------------------- |
| K_0 -> K_9      | 0 -> 9                |
| K_a -> K_z      | a -> z                |
| --------------- | --------------------- |
| K_UP            | flèche haut           |
| K_DOWN          | flèche bas            |
| K_RIGHT         | flèche droite         |
| K_LEFT          | flèche gauche         |
| --------------- | --------------------- |
| K_ESCAPE        | echap                 |
| K_SPACE         | espace                |
| K_RETURN        | entrée                |
~~~

La liste ci-dessus est tronquée et contient les constantes les plus couramment
utilisées. Vous pouvez trouver la liste complète dans la documentation du
module [pygame.key](https://www.pygame.org/docs/ref/key.html).

## Souris

~~~
M_LEFT
M_MIDDLE
M_RIGHT
~~~

## Couleurs

~~~
BLACK
GREY
WHITE
RED
GREEN
BLUE
CYAN
MAGENTA
YELLOW
~~~
