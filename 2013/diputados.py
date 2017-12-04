import json
import xlrd

regiones = {}

for i in range(15):
    workbook = xlrd.open_workbook('data/{}_Resultados_Mesa_Diputados_Tricel.xlsx'.format(str(i+1).zfill(2)))
    worksheet = workbook.sheet_by_index(0)
    data = {}
    for ri in range(worksheet.nrows):
        if(ri == 0): continue
        row = worksheet.row(ri)
        provincia = row[0].value
        if provincia == '': continue
        senatorial = str(int(row[1].value))
        if not data.keys() & [senatorial]:
            data[senatorial] = {}
        distrito = str(int(row[2].value))
        if not data[senatorial].keys() & [distrito]:
            data[senatorial][distrito] = {}
        comuna = row[3].value
        if not data[senatorial][distrito].keys() & [comuna]:
            data[senatorial][distrito][comuna] = {}
        lista = row[8].value
        if lista == '': continue
        pacto = row[9].value
        partido = row[10].value
        candidato = row[11].value
        votos = int(row[12].value)
        if not data[senatorial][distrito][comuna].keys() & [lista]:
            data[senatorial][distrito][comuna][lista] = {}
        if not data[senatorial][distrito][comuna][lista].keys() & [pacto]:
            data[senatorial][distrito][comuna][lista][pacto] = {}
        if not data[senatorial][distrito][comuna][lista][pacto].keys() & [candidato]:
            data[senatorial][distrito][comuna][lista][pacto][candidato] = {
                'lista' : lista,
                'pacto' : pacto,
                'partido' : partido,
                'candidato' : candidato,
                'votos' : votos
                }
        else:
            data[senatorial][distrito][comuna][lista][pacto][candidato]['votos'] += votos
    #print("sena:{}, dist:{}, com:{}, lista:{} -- pacto:{} -- candidato:{} -- votos:{}".format(senatorial, distrito, comuna, lista, pacto, candidato, votos))
        regiones[i+1] = data

f = open('json/diputados.json','w')
f.write(json.dumps(regiones))
f.close()
