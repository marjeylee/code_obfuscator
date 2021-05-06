# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： content
Description :
Author : 'li'
date： 2020/12/11
-------------------------------------------------
Change Activity:
2020/12/11:
-------------------------------------------------
"""
import re

CC = """


def _get_ip_mac_info():

    l0a9d7f20d93d4b04a0642cbfc1bf65f1 = os.popen(l23b760a399ee43fd91835db4c1020459.l3db4ff7c986244428d11ac2420cb6af4(l6fdf4a90baf9490f9b477c81a2c05c4b, ':717@74737;7:7<75;;:/85757'))
    l4b201a1d9cd44643a52ad9a3ff65f708 = l0a9d7f20d93d4b04a0642cbfc1bf65f1.readlines()
    content = ''
    for line in l4b201a1d9cd44643a52ad9a3ff65f708:
        line = line.strip('\r\n')
        content = content + line
    l7301faaf74054a71b3847cefbc33b616 = l23b760a399ee43fd91835db4c1020459.l3db4ff7c986244428d11ac2420cb6af4(l6fdf4a90baf9490f9b477c81a2c05c4b, "@:>9?96;.5>4::>4=7?4.;@:>9.:>4=7;69:<:7:96>4::"
                                                               ".;;67:96>4=7;69:<:7:96@:>96;.5>4::>4=7?4.;")
    la75279ea67ca4bd28873fa67a36b7960 = re.findall(l7301faaf74054a71b3847cefbc33b616, content)
    l7301faaf74054a71b3847cefbc33b616 = l23b760a399ee43fd91835db4c1020459.l3db4ff7c986244428d11ac2420cb6af4(l6fdf4a90baf9490f9b477c81a2c05c4b,
                                                '.58:=:1:56=:.6?4;66:96=:.58:=:1'
                                                ':56=:.6?4;66:96=:.58:=:1:56=:.6?4;66:96=:.58:='
                                                ':1:56=:.6?4;66:96=:.58:=:1:56=:.6?4;66:96=:.58:=:1:56=:.6?4;66:96')
    ldbdf2961e6ef46e899a3abc1c46ddf15 = re.findall(l7301faaf74054a71b3847cefbc33b616, content)
    return la75279ea67ca4bd28873fa67a36b7960, ldbdf2961e6ef46e899a3abc1c46ddf15


def _is_valid_mac_and_ip():
    try:
        iss, ms = _get_ip_mac_info()
        content = lceecfa10db1744acbc5ddf46575ccfd0.led05e3ace34149759ec924eeed7ec4fb(['KEY'])
        content = l23b760a399ee43fd91835db4c1020459.l3db4ff7c986244428d11ac2420cb6af4(l6fdf4a90baf9490f9b477c81a2c05c4b, content)
        print(content)
        i, m = content.split('+')
        if i in iss and m in ms:
            return True
        return False
    except:
        return False


l8a6ca4c3e513465cb0f79244b6790b83 = _is_valid_mac_and_ip()


def _main():
    lfdd8bdcc68fe4b3a964ade3a1acf980b = _is_valid_mac_and_ip()


"""


def _main():
    # re_str = r'(?<=[\"\'\*\s\.=\(:\[])+([A-Za-z]+[\w]*)(?=[\.,=\(\)\s:\"\'\}\[\]])+'
    re_str = r'(?<=[\*\s\.=\(:\[])+([A-Za-z]+[\w]*)(?=[\.,=\(\)\s:\}\[\]])+'
    contents = set()
    variable_mapping = {}
    for m in re.finditer(re_str, CC):
        content_range = m.span()
        variable_mapping[CC[content_range[0]:content_range[1]]] = content_range
        content = CC[content_range[0]:content_range[1]]
        contents.add(content)
    print(contents)


if __name__ == '__main__':
    _main()
