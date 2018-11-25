import time


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


def debugger(*msgs):
    if DEBUG:
        result = "DEBUG:"
        for el in msgs:
            result += " "+str(el)
        print(result)


class Ultra:
    def __init__(self, O=UNSET, o=UNSET, I=UNSET, f=UNSET, n=UNSET):
        self.operation = O

        if type(o) is not tuple:
            self.response = o,
        else:
            self.response = o

        self.session_id = I
        self.flags = f

        if type(f) is not tuple:
            self.flags = f,
        else:
            self.flags = f

        if type(n) is not tuple:
            self.flags_id = n,
        else:
            self.flags_id = n

    def __str__(self):
        result = str()
        debugger("O", self.operation)
        if self.operation is not UNSET:
            result += f"#O#$#{self.operation}#\n"

        debugger("o", self.response)
        if self.response is not UNSET and self.response[0] is not UNSET:
            result += "#o#$#"
            for i, el in enumerate(self.response):
                result += str(el)
                if i < len(self.response) - 1:
                    result += ":"
            result += "#\n"

        debugger("I", self.session_id)
        if self.session_id is not UNSET:
            result += f"#I#$#{self.session_id}#\n"

        debugger("f", self.flags)
        if self.flags is not UNSET:
            result += "#f#$#"
            for i, el in enumerate(self.flags):
                result += str(el)
                if i < len(self.flags)-1:
                    result += ":"
            result += "#\n"

        debugger("n", self.flags_id)
        if self.flags_id is not UNSET:
            result += "#n#$#"
            for i, el in enumerate(self.flags_id):
                result += str(el)
                if i < len(self.flags_id) - 1:
                    result += ":"
            result += "#\n"
        result += f"#t#$#{time.time()}#"
        return result


def main():
    # connecting by client
    packet = Ultra(O=CONNECTING, f=(PUSH, SYN), n=100)
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # ack from server
    packet = Ultra(O=CONNECTING, f=(ACK, SYN), n=(300, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # give a session
    ses = 123456
    packet = Ultra(O=SESSION, I=ses, f=PUSH, n=(400, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # ack
    packet = Ultra(O=SESSION, I=ses, f=ACK, n=(500, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # send range
    packet = Ultra(O=RANGE, o=(100, 9000), I=ses, f=PUSH, n=(600, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # ack
    packet = Ultra(O=RANGE, I=ses, f=ACK, n=(700, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # guess number
    packet = Ultra(O=GUESS, o=500, I=ses, f=PUSH, n=(800, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # ack
    packet = Ultra(O=GUESS, I=ses, f=ACK, n=(900, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # send response
    packet = Ultra(O=RESPONSE, o='>', I=ses, f=PUSH, n=(1000, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # ack
    packet = Ultra(O=RESPONSE, I=ses, f=ACK, n=(1100, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # guess number
    packet = Ultra(O=GUESS, o=400, I=ses, f=PUSH, n=(1200, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # ack
    packet = Ultra(O=GUESS, I=ses, f=ACK, n=(1300, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # send response - who wins
    packet = Ultra(O=RESPONSE, o="You win/You loss", I=ses, f=PUSH, n=(1400, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1

    # ack
    packet = Ultra(O=RESPONSE, I=ses, f=ACK, n=(1500, ack_n))
    debugger(packet)
    ack_n = int(packet.flags_id[0]) + 1


if __name__ == "__main__":
    main()