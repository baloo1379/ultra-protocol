import time
import re

DEBUG = True

CONNECTING = 'connecting'
RANGE = 'range'
GUESS = 'guess'
SESSION = 'session'
RESPONSE = 'response'

PUSH = 'push'
SYN = 'syn'
ACK = 'ack'

UNSET = "XXXXXXX"

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

        if type(o) is not tuple:
            self.response = o,
        else:
            self.response = o

        self.session_id = I

        if type(f) is not tuple:
            self.flags = f,
        else:
            self.flags = f

        if type(n) is not tuple:
            self.flags_id = n,
        else:
            self.flags_id = n
        self.time = t

    def __str__(self):
        result = str()
        # debugger("O", self.operation)
        if self.operation is not UNSET:
            result += f"#O#$#{self.operation}#\n"

        # debugger("o", self.response)
        if self.response is not UNSET and self.response[0] is not UNSET:
            result += "#o#$#"
            for i, el in enumerate(self.response):
                result += str(el)
                if i < len(self.response) - 1:
                    result += ":"
            result += "#\n"

        # debugger("I", self.session_id)
        if self.session_id is not UNSET:
            result += f"#I#$#{self.session_id}#\n"

        # debugger("f", self.flags)
        if self.flags is not UNSET:
            result += "#f#$#"
            for i, el in enumerate(self.flags):
                result += str(el)
                if i < len(self.flags) - 1:
                    result += ":"
            result += "#\n"

        # debugger("n", self.flags_id)
        if self.flags_id is not UNSET:
            result += "#n#$#"
            for i, el in enumerate(self.flags_id):
                result += str(el)
                if i < len(self.flags_id) - 1:
                    result += ":"
            result += "#\n"
        result += f"#t#$#{self.time}#"
        return result

    @staticmethod
    def parse(data: str):
        packet = Ultra()
        row_data = data.split("\n")
        data = {}
        for el in row_data:
            row = el.split("#")
            row = row[1:-1]
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
            pattern2 = "[=<>]"
            result = tuple(re.findall(pattern1, data["o"]))
            if result is not None:
                debugger(result)
                packet.response = result
            else:
                result = tuple(re.findall(pattern2, data["o"]))
                debugger(result)
                packet.response = result
        except KeyError:
            packet.response = UNSET
        try:
            pattern = "\w+"
            result = tuple(re.findall(pattern, data["f"]))
            debugger(result)
            packet.flags = result
        except KeyError:
            packet.flags = UNSET
        try:
            pattern = "\d+"
            result = tuple(re.findall(pattern, data["n"]))
            debugger(result)
            packet.flags_id = result
        except KeyError:
            packet.flags_id = UNSET
        try:
            packet.session_id = data["I"]
        except KeyError:
            packet.session_id = UNSET
        try:
            packet.time = data["t"]
        except KeyError:
            packet.time = UNSET
        return packet

    def print(self):
        return self.operation, self.response, self.session_id, self.flags, self.flags_id, self.time


def main():
    # # connecting by client
    # packet = Ultra(O=CONNECTING, f=(PUSH, SYN), n=100)
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack connecting from server
    # packet = Ultra(O=CONNECTING, f=(PUSH, ACK, SYN), n=(200,ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # give a session
    # ses = 123456
    # packet = Ultra(O=SESSION, I=ses, f=PUSH, n=(400, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=SESSION, I=ses, f=ACK, n=(500, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # send range
    # packet = Ultra(O=RANGE, o=(100, 9000), I=ses, f=PUSH, n=(600, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=RANGE, I=ses, f=ACK, n=(700, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # guess number
    # packet = Ultra(O=GUESS, o=500, I=ses, f=PUSH, n=(800, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=GUESS, I=ses, f=ACK, n=(900, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # send response
    # packet = Ultra(O=RESPONSE, o='>', I=ses, f=PUSH, n=(1000, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=RESPONSE, I=ses, f=ACK, n=(1100, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # guess number
    # packet = Ultra(O=GUESS, o=400, I=ses, f=PUSH, n=(1200, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=GUESS, I=ses, f=ACK, n=(1300, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # send response - who wins
    # packet = Ultra(O=RESPONSE, o="You win/You loss", I=ses, f=PUSH, n=(1400, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1

    # # ack
    # ses = 123
    # packet = Ultra(O=RESPONSE, I=ses, f=PU, n=(1500, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1

    print("@@@@@ parsing @@@@@")
    packet = Ultra()
    x = Ultra(O=RANGE, o=(500, 400), I=123456, f=(PUSH, ACK), n=(1400, 1401))
    print(x.print())
    print(packet, x)
    packet.parse(str(x))
    print(packet.print())


if __name__ == "__main__":
    main()
