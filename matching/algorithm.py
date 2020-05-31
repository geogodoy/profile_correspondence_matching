"""
Algorithm:

Seja cmp_profiles o conjunto de perfis existentes e o profile seja
o perfil que queremos encontrar o mais semelhante.

Cada cmp_profile recebe um valor de correspondência que representa o
semelhança com o perfil, e aquele com o maior valor é dito que
mais parecido.

Ao confrontar dois perfis, cada tópico discutido pelos dois perfis
contribui para o match_value com uma pontuação proporcional à
similaridade da porcentagem de discussão do tópico nos dois
perfis.

"""
import math


def get_similarity(value1, value2):
    """
    Evaluate the similarity of two discussion percentages for a topic.

    Args:
        value1: discussion percentage of the topic in the first profile
        value2: discussion percentage of the topic in the second profile

    Returns:
        A value representing the similarity of the two percentages.
    """
    diff = abs(value1-value2)
    return math.exp(-(diff**2) / 1000) * min(value1, value2)


def match_value(profile1, profile2):
    """
    Cada tópico discutido pelos dois perfis contribui para o match_value
    com uma pontuação proporcional à semelhança de sua discussão

    Args:
    profile1: primeiro perfil a comparar
    profile2: segundo perfil para comparar
    
    Returns:
    O valor de correspondência que avalia a semelhança entre os dois
    perfis
    """
    value = 0
    for topic, times1 in profile1.items():
        if topic in profile2:
            sim = get_similarity(times1, profile2[topic])
            value += sim
    return value


def match(profile, cmp_profiles):
    """
    Args:
    profile: o perfil para o qual tenta encontrar o mais semelhante para ele
    cmp_profiles: lista de perfis com os quais a comparação é
    feito.

    Returns:
    uma tupla com o índice do cmp_profile mais semelhante ao perfil e uma lista 
    com os valores de similaridade para cada perfil
    """
    best_match_id = None
    best_match_value = 0
    match_values = []

    for i, cmp_p in enumerate(cmp_profiles):
        curr_match_value = match_value(profile, cmp_p)
        match_values.append(curr_match_value)
        if curr_match_value > best_match_value:
            best_match_value = curr_match_value
            best_match_id = i
    return best_match_id, match_values
