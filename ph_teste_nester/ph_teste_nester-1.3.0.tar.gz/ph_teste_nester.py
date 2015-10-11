"""Este é o módulo "nester.py", e fornece uma função chamada print_lol()
que imprime listas que podem ou não incluir listas aninhadas"""
def print_lol(the_list, indent = False, level = 0):
    """Esta função requer um argumento chamado "the_list", que é qualquer lista
    Python (de possíveis listas aninhadas).Cada item de dados na lista fornecida
    é (recursivamente) impresso na tela em sua própria linha. 
    Um segundo argumento chamado 'indent' certifica-se do desenvolvedor querer a 
    indentação sendo o argumento padrão NÃO identar.
    Um terceiro argumento chamado 'level' é usado para inserir as tabulações quando
    uma lista aninhada é encontrada, sendo o padrão 0 """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1)
        else:
            if indent == True:
                for tabulation in range(level):
                    print("\t",end='')
            print(each_item)