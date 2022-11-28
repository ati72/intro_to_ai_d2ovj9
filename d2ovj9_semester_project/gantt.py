import matplotlib.pyplot as plt
import numpy as np
import random

def init_gantt(masinak, ht):
    #paraméterek:
    hbar = 10
    tticks = 10
    masinak_szama = len(masinak)

    #plot object creation:
    fig, gantt = plt.subplots()

    #paraméterek szótár:
    diagram = {
        "fig": fig,
        "ax": gantt,
        "hbar": hbar,
        "tticks": tticks,
        "masinak": masinak,
        "ht" : ht,
        "colors":{}
    }

    #tengelyek feliratai:
    gantt.set_xlabel("Idő")
    gantt.set_ylabel("Erőforrások")

    #tengelyek határai:
    gantt.set_xlim(0, ht)
    gantt.set_ylim(masinak_szama * hbar, 0)

    #időtengely felosztása:
    gantt.set_xticks(range(0, ht, 1), minor=True)
    gantt.grid(True, axis='x', which='both')

    #erőforrás tengely felosztása:
    gantt.set_yticks(range(hbar, masinak_szama*hbar, hbar), minor=True)
    gantt.grid(True, axis='y', which='minor')

    #erőforrás feliratok:
    gantt.set_yticks(np.arange(hbar/2, hbar*masinak_szama - hbar/2 + hbar, hbar))
    gantt.set_yticklabels(masinak)

    return diagram

#metodus a feladatok letrehozasahoz:
def reszfeladat_szamitas(diagram, t0, d, masina, feladat_nevek, color=None):
    masinak = diagram["masinak"]
    hbar = diagram["hbar"]
    gantt = diagram["ax"]
    ht = diagram["ht"]

    #színezés:
    if diagram["colors"].get(feladat_nevek) == None:
        if color == None:
            r = random.random()
            g = random.random()
            b = random.random()
            color = (r, g, b)
            diagram["colors"].update({feladat_nevek:color})
    else:
        color = diagram["colors"].get(feladat_nevek)

    #erőforrás indexek:
    masina_index = masinak.index(masina)

    #sávok elhelyezése:
    gantt.broken_barh([(t0, d)], (hbar*masina_index, hbar), facecolors=(color))

    #szöveg elhelyezése:
    gantt.text(x=(t0 + d/2), y=(hbar*masina_index + hbar/2), s=f"{feladat_nevek} ({d})", va='center', ha='center', color='black')

def gantt_befejez(diagram, munkaterv, masina_nevek, munka_nevek):
    #részfeladatok hozzáadása:
    for reszfeladat in munkaterv:
        reszfeladat_szamitas(diagram, reszfeladat["t0"], reszfeladat["d"], masina_nevek[reszfeladat["masina_index"]], munka_nevek[reszfeladat["munka_index"]])

def gantt_letrehoz(munkaterv, masina_nevek, munka_nevek):
    #idő határok:
    utolso_reszfeladat = munkaterv[-1]
    ht = utolso_reszfeladat["t0"] + utolso_reszfeladat["d"] #ht a completion time

    #gantt diagram létrehozása:
    diagram = init_gantt(masina_nevek, ht)

    gantt_befejez(diagram, munkaterv, masina_nevek, munka_nevek)

    return diagram

def gantt_megrajzol(munkaterv, masina_nevek, munka_nevek):
    gantt_letrehoz(munkaterv, masina_nevek, munka_nevek)
    plt.show()
