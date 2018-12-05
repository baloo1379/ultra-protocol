import time
import re

DEBUG = False

CONNECTING = 'connecting'
RANGE = 'range'
GUESS = 'guess'
SESSION = 'session'
RESPONSE = 'response'

PUSH = 'push'
SYN = 'syn'
ACK = 'ack'

UNSET = "empty"

FIELDS = ('O', 'o', 'I', 'f', 'n', 't')

'''
Client initializes connection
Server ack
Server send session_id
Client ack
Server send (L1:L2)
Client ack
while (client hit):
    Client send L
    Server ack
    Server response
    client ack
Server send result to all clients
Clients ack
'''


def debugger(*msgs):
    if DEBUG:
        result = "DEBUG:"
        for el in msgs:
            result += " "+str(el)
        print(result)


class Ultra:
    def __init__(self, O=UNSET, o=UNSET, I=UNSET, f=UNSET, n=UNSET, t=time.time()):
        self.operation = O
        self.response = o
        self.session_id = I
        self.flags = f
        self.flags_id = n
        self.time = t

    def __str__(self):
        result = str()

        result += f"#O#$#{self.operation}#"

        result += "#o#$#"
        if type(self.response) is str:
            result += self.response
        elif type(self.response) is int:
            result += str(self.response)
        elif type(self.response) is tuple:
            for i, el in enumerate(self.response):
                result += str(el)
                if i < len(self.response) - 1:
                    result += ":"
        result += "#"

        result += f"#I#$#{self.session_id}#"

        result += "#f#$#"
        if type(self.flags) is str:
            result += self.flags
        elif type(self.flags) is tuple:
            for i, el in enumerate(self.flags):
                result += el
                if i < len(self.flags) - 1:
                    result += ":"
        result += "#"

        result += "#n#$#"
        if type(self.flags_id) is int:
            result += str(self.flags_id)
        elif type(self.flags_id) is tuple:
            for i, el in enumerate(self.flags_id):
                result += str(el)
                if i < len(self.flags_id) - 1:
                    result += ":"
        result += "#"

        result += f"#t#$#{self.time}#"

        return result

    def pack(self):
        result = str()

        result += f"#O#$#{self.operation}#"

        result += "#o#$#"
        if type(self.response) is str:
            result += self.response
        elif type(self.response) is int:
            result += str(self.response)
        elif type(self.response) is tuple:
            for i, el in enumerate(self.response):
                result += str(el)
                if i < len(self.response) - 1:
                    result += ":"
        result += "#"

        result += f"#I#$#{self.session_id}#"

        result += "#f#$#"
        if type(self.flags) is str:
            result += self.flags
        elif type(self.flags) is tuple:
            for i, el in enumerate(self.flags):
                result += el
                if i < len(self.flags) - 1:
                    result += ":"
        result += "#"

        result += "#n#$#"
        if type(self.flags_id) is int:
            result += str(self.flags_id)
        elif type(self.flags_id) is tuple:
            for i, el in enumerate(self.flags_id):
                result += str(el)
                if i < len(self.flags_id) - 1:
                    result += ":"
        result += "#"

        result += f"#t#$#{time.time()}#"
        return result

    @staticmethod
    def parse(data: str):
        packet = Ultra()
        row_data = data.split("##")
        data = {}
        for el in row_data:
            row = el.split("#")
            # row = row[1:-1]
            try:
                row.remove('')
            except ValueError:
                pass
            row.remove("$")
            dic = {row[0]: row[1]}
            data.update(dic)
            # debugger(i, dic)
        debugger(data)

        try:
            packet.operation = data["O"]
        except KeyError:
            packet.operation = UNSET

        try:
            pattern1 = "\d+"
            pattern2 = "[=<>]|\w+"
            result = re.findall(pattern1, data["o"])
            if len(result) is not 0:
                debugger(result)
                if len(result) > 1:
                    t = []
                    for el in result:
                        t.append(int(el))
                    packet.response = tuple(t)
                else:
                    packet.response = int(result[0])
            else:
                result = re.findall(pattern2, data["o"])
                debugger(result)
                packet.response = result[0]
        except KeyError:
            packet.response = UNSET

        try:
            pattern = "\w+"
            result = re.findall(pattern, data["f"])
            debugger(result)
            if len(result) is 1:
                packet.flags = result[0]
            else:
                packet.flags = tuple(result)
            debugger(packet.flags)
        except KeyError:
            packet.flags = UNSET
        try:
            pattern = "\d+"
            result = re.findall(pattern, data["n"])
            debugger(result)
            if len(result) is 1:
                packet.flags_id = int(result[0])
            else:
                t = []
                for el in result:
                    t.append(int(el))
                packet.flags_id = tuple(t)
        except KeyError:
            packet.flags_id = UNSET
        try:
            packet.session_id = int(data["I"])
        except KeyError:
            packet.session_id = UNSET
        except ValueError:
            packet.session_id = UNSET
        try:
            packet.time = data["t"]
        except KeyError:
            packet.time = UNSET
        return packet

    def print(self):
        result = "("
        if self.operation is not UNSET:
            result += self.operation + ", "
        if self.response is not UNSET:
            result += str(self.response) + ", "
        if self.session_id is not UNSET:
            result += str(self.session_id) + ", "
        if self.flags is not UNSET:
            result += str(self.flags) + ", "
        if self.flags_id is not UNSET:
            result += str(self.flags_id) + ", "
        result += str(self.time) + ")"
        return result


def main():
    print("@@@@@ parsing @@@@@")
    x = Ultra(O=RANGE, o=(500, 400), I=123456, f=PUSH, n=1400), \
        Ultra(O=RANGE, o=500, I=123456, f=(PUSH, ACK), n=(140, 100)), \
        Ultra(O=RANGE, o="=", I=123456, f=(PUSH, ACK, SYN), n=(400, 500)), \
        Ultra(O=RANGE, o=">", I=123456, f=PUSH, n=140), \
        Ultra(O=RANGE, o="<", I=123456, f=PUSH, n=140)

    # for el in x:
    #     print(el.print())

    print("===")
    x = Ultra.parse(x[0].pack())
    # y = []
    # for el in x:
    #     y.append(Ultra.parse(el.pack()))
    #
    # for el in y:
    #     print(el.print())


if __name__ == "__main__":
    main()
