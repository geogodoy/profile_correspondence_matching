"""
Contém as funções para fazer a comparação entre o perfil e o
cmp_profiles e para obter o mais semelhante.
"""
from .parsing.parser import get_parsed_profile, get_parsed_profiles, \
    values_to_percentage
from .algorithm import match as match1


def match(profile, cmp_profiles, cmp_ids=None):
    """
    Encontre o perfil mais semelhante ao fornecido entre cmp_profiles.

    Args:
        profile: o perfil para o qual você deseja encontrar o mais semelhante
        cmp_profiles: os perfis com os quais a comparação é feita
        cmp_ids (opcional): os IDs dos cmp_profiles

    Returns:
        uma lista com uma tupla, cada tupla contém o ID do perfil mais semelhante retornado
        pelo algoritmo e uma lista de valores de similaridade calculados por ele
    """
    profile = get_parsed_profile(profile)
    cmp_profiles = get_parsed_profiles(cmp_profiles)

    if cmp_ids and not len(cmp_ids) == len(cmp_profiles):
        raise ValueError(
            "cmp_ids size and cmp_profiles size do not correspond")
    values_to_percentage(profile)

   
    """
    o algoritmo correspondente é baseado na porcentagem do número
    que é a quantidade de vezes que o perfil falou sobre um tópico no total
    """
    for cmp_p in cmp_profiles:
        values_to_percentage(cmp_p)

    best_match_id1, match_values1 = match1(profile, cmp_profiles)

    if cmp_ids:
        best_match_id1 = cmp_ids[best_match_id1]

    return [(best_match_id1, match_values1)]
