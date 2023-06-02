# Pentru a calcula produsul scalar (dot product) al vectorilor AB și BC, puteți folosi următoarea formulă:
#
# AB · BC = |AB| * |BC| * cos(θ)
#
# Unde:
#
# AB reprezintă primul vector,
# BC reprezintă al doilea vector,
# |AB| reprezintă norma (lungimea) vectorului AB,
# |BC| reprezintă norma (lungimea) vectorului BC,
# θ reprezintă unghiul dintre vectorii AB și BC.
# Această formulă ne ajută să calculăm produsul scalar al vectorilor și să obținem o valoare numerică care exprimă măsura de corelație sau similaritate între aceștia.
#
# Dacă aveți coordonatele punctelor A, B și C, puteți calcula vectorii AB și BC utilizând coordonatele acestora și apoi puteți aplica formula de mai sus pentru a calcula produsul scalar.


import math

# calculeaza unghiul dintre doi vectori concurenti
# ia ca input un array 3 puncte relevante. ordinea conteaza
def compute_angle(points, relevant_poits):
    if len(relevant_poits) > 3:
        print(" Functia Compute Angle calculeaza ungliul doar intre doi vectori concurenti")
        return False
    vector_AB = (points[relevant_poits[0]][0] - points[relevant_poits[1]][0], points[relevant_poits[0]][1] - points[relevant_poits[1]][1])
    vector_BC = (points[relevant_poits[1]][0] - points[relevant_poits[2]][0], points[relevant_poits[1]][1] - points[relevant_poits[2]][1])

    # Produsul scalar AB si BC
    dot_product_AC = vector_AB[0] * vector_BC[0] + vector_AB[1] * vector_BC[1]

    # Calculeaza norma intre AB si BC
    magnitude_AB = math.sqrt(vector_AB[0] ** 2 + vector_AB[1] ** 2)
    magnitude_BC = math.sqrt(vector_BC[0] ** 2 + vector_BC[1] ** 2)

    # Calculeaza cosinusul unghiului intre AB and BC
    cosine_angle_AC = dot_product_AC / (magnitude_AB * magnitude_BC)

    # Calculeaza unghiul in radiani
    angle_rad_AC = math.acos(cosine_angle_AC)

    # Conversie din unghi in grade angle_deg_AC
    return abs(math.degrees(angle_rad_AC) - 180)