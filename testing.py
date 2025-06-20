class Nodo():

    def __init__(self, pos, papa=None):
        self.pos = pos
        self.hijos = []
        self.papa = papa

    def genera_hijos(self, obstaculos, limites):
        global mov
        # uno arriba
        pos_arriba = self.pos[:]
        pos_arriba[1] += mov

        # uno abajo
        pos_abajo = self.pos[:]
        pos_abajo[1] -= mov

        # uno izq
        pos_izq = self.pos[:]
        pos_izq[0] -= mov

        # uno der
        pos_der = self.pos[:]
        pos_der[0] += mov

        if es_punto_valido(pos_arriba, obstaculos):
            hijo = self.__class__(pos_arriba, self)
            self.hijos.append(hijo)

        if es_punto_valido(pos_abajo, obstaculos):
            hijo = self.__class__(pos_abajo, self)
            self.hijos.append(hijo)

        if es_punto_valido(pos_izq, obstaculos):
            hijo = self.__class__(pos_izq, self)
            self.hijos.append(hijo)

        if es_punto_valido(pos_der, obstaculos):
            hijo = self.__class__(pos_der, self)
            self.hijos.append(hijo)

    def __eq__(self, n2):
        return self.pos == n2.pos

    def __str__(self):
        s = f"[{self.pos[0]}, {self.pos[1]}]"
        return s

    def rrt(self, meta, robot, max_iter=1000):
        global expandidos
        nodos = [self]
        for iter in range(max_iter):
            # generar punto aleatorio
            r_x = random.randint(robot.limites[0], robot.limites[2])
            r_y = random.randint(robot.limites[1], robot.limites[3])
            r_P = [r_x, r_y]  # random point

            # encontrar nodo más cercano al punto aleatorio
            N_c = min(nodos, key=lambda n: math.dist(n.pos, r_P))  # closest node

            # vector hacia el punto aleatorio
            v = np.array(r_P) - np.array(N_c.pos)  # vector

            h = np.linalg.norm(v)  # hypotenuse

            if h == 0:  # X o Y infinitos
                continue
            v = (v / h) * mov

            n_P = list(np.array(N_c.pos) + v)  # nuevo punto

            # es válido?
            if es_punto_valido(n_P, robot.obstaculos, robot.limites):
                N_N = Nodo(n_P, N_c)  # nuevo nodo
                N_c.hijos.append(N_N)
                nodos.append(N_N)
                expandidos.append(N_N)

                # esta cerca de la meta (a un movimiento de distancia)?
                if math.dist(n_P, meta) < mov:
                    meta_nodo = Nodo(meta, N_N)
                    N_N.hijos.append(meta_nodo)
                    nodos.append(meta_nodo)
                    expandidos.append(meta_nodo)

                    camino = []
                    papa = meta_nodo
                    while papa:
                        camino.append(papa)
                        papa = papa.papa
                    camino.reverse()
                    print(f"Encontrado a las {iter} de {max_iter} iteraciones")
                    return camino
        return None