def encrypt(O00OO000O0OO0000O, OOOOO00OOO0OOOO0O):
    O000O000OO0O000O0 = bytearray(str(OOOOO00OOO0OOOO0O).encode("utf-8"))
    O0000O0O00OOO000O = len(O000O000OO0O000O0)
    O0000O0OOOO00000O = bytearray(O0000O0O00OOO000O * 2)
    OOO0O0OOO00O00OOO = 0  # line:6
    for OOO0O0O0000OOO0O0 in range(0, O0000O0O00OOO000O):
        O0O0OO0O0000O0O0O = O000O000OO0O000O0[OOO0O0O0000OOO0O0]
        O0O00OO0OOOO0OOOO = O0O0OO0O0000O0O0O ^ O00OO000O0OO0000O
        O000OOO0OO000000O = O0O00OO0OOOO0OOOO % 19
        OO00OOOO000000000 = O0O00OO0OOOO0OOOO // 19  # line:11
        O000OOO0OO000000O = O000OOO0OO000000O + 46  # line:12
        OO00OOOO000000000 = OO00OOOO000000000 + 46  # line:13
        O0000O0OOOO00000O[OOO0O0OOO00O00OOO] = O000OOO0OO000000O
        O0000O0OOOO00000O[OOO0O0OOO00O00OOO + 1] = OO00OOOO000000000  # line:15
        OOO0O0OOO00O00OOO = OOO0O0OOO00O00OOO + 2  # line:16
    return O0000O0OOOO00000O.decode("utf-8")  # line:17


def decrypt(O00000O0OOOO000O0, O000000OOOOOOOOOO):  # line:20
    OOOO0O00O00O00O0O = bytearray(str(O000000OOOOOOOOOO).encode("utf-8"))  # line:21
    OO000O0O00O00O000 = len(OOOO0O00O00O00O0O)  # line:22
    if OO000O0O00O00O000 % 2 != 0:  # line:23
        return ""  # line:24
    OO000O0O00O00O000 = OO000O0O00O00O000 // 2  # line:25
    O0O000000OOOOO000 = bytearray(OO000O0O00O00O000)  # line:26
    OO00OOOO00OOOOO00 = 0  # line:27
    for OOOO000OO0O000O00 in range(0, OO000O0O00O00O000):  # line:28
        OOOOO000OO0000000 = OOOO0O00O00O00O0O[OO00OOOO00OOOOO00]  # line:29
        OO00O00OO0OO00O00 = OOOO0O00O00O00O0O[OO00OOOO00OOOOO00 + 1]  # line:30
        OO00OOOO00OOOOO00 = OO00OOOO00OOOOO00 + 2  # line:31
        OOOOO000OO0000000 = OOOOO000OO0000000 - 46  # line:32
        OO00O00OO0OO00O00 = OO00O00OO0OO00O00 - 46  # line:33
        O000OOO0OO00OO00O = OO00O00OO0OO00O00 * 19 + OOOOO000OO0000000  # line:34
        OO000OOOOOOOOO0OO = O000OOO0OO00OO00O ^ O00000O0OOOO000O0  # line:35
        O0O000000OOOOO000[OOOO000OO0O000O00] = OO000OOOOOOOOO0OO  # line:36
    return O0O000000OOOOO000.decode("utf-8")  # line:37


a = 'passworsdad!232$%@#$133%12321321344.213.5.65.2'  # line:40
b = encrypt(222, a)  # line:41
print(b)  # line:42
c = decrypt(222, b)  # line:43
print(a == c)  # line:44