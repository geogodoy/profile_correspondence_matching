import os
import json
import requests
from matching.matcher import match
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def path_to_id(profile_path):
    """
    Converte o path do profile em um ID.

    Args:
        profile_path: o caminho do arquivo que contém os dados de cada profile

    Returns:
        o nome do arquivo sem a extensão '.json'
    """
    return profile_path.rstrip('.json').split('/')[-1]

# throws


def get_profile_by_file(profile_path):
    """
    Pega os perfis pelo arquivo

    Returns:
        uma tupla com o nome do arquivo (sem a extensão), que deve ser 
        o ID do perfil e o próprio perfil
    """
    try:
        with open(profile_path) as f:
            profile = json.load(f)
    except json.decoder.JSONDecodeError as ex:
        raise json.decoder.JSONDecodeError(ex.msg, profile_path, ex.pos)
    return path_to_id(profile_path), profile

def get_profiles_by_dir(profiles_dir):
    """
    Pega os perfis pelo diretório

    Args:
        profiles_dir: o caminho para o diretório para os arquivos json dos perfis

    Returns:
        uma tupla com uma lista com os nomes de arquivo (sem a extensão), 
        que devem ser os IDs dos perfis, e uma lista com os perfis
    """
    profiles = []
    ids = []
    if not profiles_dir.endswith('/'):
        profiles_dir += '/'
    for filename in os.listdir(profiles_dir):
        if filename.endswith('.json') and not filename.startswith('.'):
            profile_id, profile = get_profile_by_file(profiles_dir + filename)
            ids.append(profile_id)
            profiles.append(profile)

    return ids, profiles


def main(profile_path, cmp_profiles_dir):
    """
    Args:
        profile_path: o caminho onde contém os dados dos perfis para compatibilizar 
        com o perfil corrente

        cmp_profiles_dir: o diretório que contém os perfis existentes
            (json)
    """
    try:
        _, profile = get_profile_by_file(profile_path)
        cmp_ids, cmp_profiles = get_profiles_by_dir(cmp_profiles_dir)
        results = match(profile, cmp_profiles, cmp_ids)
        for i, (id, match_values) in enumerate(results):
            mostSimilar = 0
            print("Resultados de similaridade de %s:" % id )
            for j in range(len(match_values)):
                if id != cmp_ids[j]:
                    print("Similaridade com %s: %f" % (cmp_ids[j], match_values[j]))
                    if  mostSimilar < match_values[j]:
                        mostSimilar = match_values[j] 
                        nameMostSimilar =  cmp_ids[j]                      
            print("Maior Similaridade com: %s\n" % nameMostSimilar)
    except (FileNotFoundError, IsADirectoryError) as ex:
        print("O nome do arquivo não foi encontrado: %s" % (str(ex)))
    except (json.decoder.JSONDecodeError) as ex:
        print("Erro ao converter o arquivo %s: %s" % (ex.doc, str(ex)))
    except requests.exceptions.ConnectionError as ex:
        print("Erro ao se conectar com a API da Wikipedia: %s" % (str(ex)))


if __name__ == "__main__":
    ap = ArgumentParser(description="""
        Avalia a semelhança de um perfil com um conjunto de
        ones(função retorna uma nova matriz de uma determinada forma e tipo de dados)
        e retorna o id do mais semelhante.
        """, formatter_class=ArgumentDefaultsHelpFormatter)

    ap.add_argument('--cmp_profiles_dir', action='store',
        dest='cmp_profiles_dir', type=str, default='cmp_profile/',
        help="""
        diretório com os arquivos dos perfis usados ​​para a comparação.
        O diretório deve conter apenas esses arquivos e cada arquivo 
        deve estar no formato json. Veja os arquivos de exemplo no diretório 
        tapoi_models para obter mais informações
        """)
    ap.add_argument('profile_path', type=str, help="""
        o arquivo json que contém o perfil com o qual você deseja comparar
        os existentes
        """)
    args = ap.parse_args()

    main(args.profile_path, args.cmp_profiles_dir)
