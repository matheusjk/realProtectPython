from datetime import datetime

arquivo = open('auth.log')

# print(arquivo.read())
# print(arquivo.readlines())
# for lin in arquivo.readlines():
#     print(lin)
# print(arquivo.readline())

for linhas in arquivo.readlines():
    print(linhas.split())
    dataString =  linhas.split()[1] + "-" + linhas.split()[0] + "-2020 " + linhas.split()[2]
    print(dataString)
    data = datetime.strptime(dataString, "%d-%b-%Y %H:%M:%S")
    print(data)
    ip = linhas.split()[3]
    print(ip.replace("ip-", "").replace("-","."))
    print(str(linhas.split()[5:]).replace("'", "").replace(",", "").replace("[","").replace("]", ""))
    print("\n")
    print("{} {}".format(linhas.split()[4],str(linhas.split()[5:]).replace("'", "").replace(",", "").replace("[","").replace("]", "")).rstrip())
    break

arquivo.close()