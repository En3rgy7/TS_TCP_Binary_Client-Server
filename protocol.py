
d = {}
def datadecode(raw_data):
    data = ""
    for byte in raw_data:
        data += "{0:b}".format(byte).rjust(8, '0')
    print('-----------------------------ODEBRANO------------------------------')
    print('Binary data: ', data)

    d['operation'] = int(data[0:5], 2)
    d['answer'] = int(data[5:9], 2)
    d['id'] = int(data[9:12], 2)
    d['number'] = int(data[12:20], 2)
    d['supplement'] = int(data[20:24], 2)

    print("Decode message: Operation:{}, answer:{}, id:{}, number:{}, supplement:{}".format(d['operation'],d['answer'],d['id'],d['number'],d['supplement']))
    print('-------------------------------------------------------------------')
    return d

def dataencode(oper,ans,i,num,supp):
    print('------------------------------WYSLANO------------------------------')
    print("Operation:{}, answer:{}, id:{}, number:{}, supplement:{}".format(oper,ans,i,num,supp))
    oper = "{0:b}".format(oper).rjust(5, '0')
    ans = "{0:b}".format(ans).rjust(4, '0')
    i = "{0:b}".format(i).rjust(3, '0')
    num = "{0:b}".format((num)).rjust(8, '0')
    supp = "{0:b}".format(supp).rjust(4, '0')

    message = oper + ans + i + num + supp
    print('Binary message: ', message)
    print('-------------------------------------------------------------------')
    l = len(message)
    if l % 8 != 0:
        message += '0' * (8 - (len(message) % 8))
    b_message = int(message, 2).to_bytes(len(message) // 8, byteorder='big')
    return b_message