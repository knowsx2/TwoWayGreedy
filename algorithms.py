def twowaygreedy(agents, solutions):
    P = solutions
    I = set()
    A = agents
    while len(P) > 1:
        i_in = max(enumerate(A.difference(I)), key=lambda x: x[1].domain[-1])[1]  # ritorna l'agente col massimo dominio
        i_out = min(enumerate(A.difference(I)), key=lambda x: x[1].domain[0])[1]  # ritorna l'agente col minimo dominio
        i = i_in
        if i == i_in and [solution for solution in P if i in P]:
            P_in = [solution for solution in P if i in P]
            P = P_in
            A.remove(i)
        elif i == i_out and [solution for solution in P if i not in P]:
            P_out = [solution for solution in P if i not in P]
            P = P_out
            A.remove(i)
        else:
            I.add(i)
    return P.pop()
