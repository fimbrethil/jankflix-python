import re
def get_after(string, after_this):
    return string[string.index(after_this) + len(after_this):]

def get_before(string, before_this):
    return string[:string.index(before_this)]

def decode_packed_javascript(packed):
    pack = get_after(packed, "return p}('")
    for index in range(len(pack)):
        if pack[index] == "'" and pack[index-1] != "\\":
            p_ack_break = index
            break
    
    base62 = list('0123456789abcdefghijklmnopqrstuvwxyz')
    base62.append("10")
    base62.append("11")
    p = pack[:p_ack_break].replace("\\'","'")
    ack = pack[p_ack_break:]
    ack = ack.replace("'","")
    ack_split = ack.split(",")
    ack_split.remove("")
    a = ack_split[0]
    c = int(ack_split[1])
    k = ack_split[2]
    k = get_before(k, ".split")
    k_arr = k.split("|")
    while c:
        c = c-1
        if k_arr[c] != "":
            exp = re.compile(r'\b%s\b' % base62[c])
            p = exp.sub(k_arr[c],p)
    return p
            
    
