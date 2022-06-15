import psycopg2 #para conexão com o banco
import time #para ativar sleep de 1 em 1 minuto
import timeit
import requests #requisições de acesso na API
from datetime import date, datetime

iteracoes=1 #variavel para controle no while

while iteracoes != 6:
    requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL")#site da API onde está os valores
    requisicao_dic = requisicao.json()#formata o arquivo em json

    #atribuindo valores as variaveis
    id = 'default' #valor de identificação auto incrementavel no banco 
    cotacao_dolar = float(requisicao_dic ["USDBRL"]["bid"])
    cotacao_euro = float(requisicao_dic ["EURBRL"]["bid"])
    dataDAcotacao = datetime.today().strftime('%Y-%m-%d %H:%M')#pega a data e hora da cotação em que foi consultado

    print(f'{cotacao_dolar} e do {cotacao_euro}')
    
    #conectadno no banco
    con = psycopg2.connect(host='*******',
                       database='*******',
                      user='*******',
                     password='*******')

    #declarando um cursor
    cursor = con.cursor() 
    
    print('inserindo dados...\n\n')
    cursor.execute(f"""insert into cotação values({id}, {cotacao_dolar:,.6f}, {cotacao_euro:,.6f}, '{dataDAcotacao}');""")
    time.sleep(3)
    print('Dados inseridos com sucesso...')
    con.commit()
    cursor.close()
    con.close()

    print(f'aguardando proxima iteração {iteracoes}/10' )
    iteracoes +=1#atualiza o controle do while
    time.sleep(15)#faz com que o progrma rode a cada 1 minuto

print("terminou")
