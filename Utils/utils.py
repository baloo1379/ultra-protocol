DEBUG = False
padding = 15


def debugger(*msgs):
    if DEBUG:
        result = "DEBUG:"
        for el in msgs:
            result += " "+str(el)
        print(result)


def str_padded(msg: str):
    global padding
    if len(msg) > padding:
        padding = len(msg)
    for el in range(padding-len(msg)):
        msg += "."
    return msg
