def Terbilang(x):
    angka = {1: 'satu', 2: 'dua', 3: 'tiga', 4: 'empat', 5: 'lima', 6: 'enam', 7: 'tujuh', 8: 'delapan', 9: 'sembilan'}
    b = ' puluh '
    c = ' ratus '
    d = ' ribu '
    e = ' juta '
    f = ' miliyar '
    g = ' triliun '

    y = x
    print y
    n = len(y)
    if n <= 3:
        if n == 1:
            if y == '0':
                return ''
            else:
                return angka[int(y)]
        elif n == 2:
            if y[0] == '1':
                if y[1] == '1':
                    return 'sebelas'
                elif y[0] == '0':
                    x = y[1]
                    return Terbilang(x)
                elif y[1] == '0':
                    return 'sepuluh'
                else:
                    return angka[int(y[1])] + ' belas'
            elif y[0] == '0':
                x = y[1]
                return Terbilang(x)
            else:
                x = y[1]
                return angka[int(y[0])] + b + Terbilang(x)
        else:
            if y[0] == '1':
                x = y[1:]
                return 'seratus ' + Terbilang(x)
            elif y[0] == '0':
                x = y[1:]
                return Terbilang(x)
            else:
                x = y[1:]
                return angka[int(y[0])] + c + Terbilang(x)
    elif 3 < n <= 6:
        p = y[-3:]
        q = y[:-3]
        if q == '1':
            return 'seribu' + Terbilang(p)
        elif q == '000':
            return Terbilang
        return Terbilang(q) + d + Terbilang(p)
    elif 6 < n <= 9:
        r = y[-6:]
        s = y[:-6]
        print r
        print s

        awal = Terbilang(s)
        print awal
        tengah = e
        print e
        akhir  = Terbilang(r)
        print akhir
        return Terbilang(s) + e + Terbilang(r)
    elif 9 < n <= 12:
        t = y[-9:]
        u = y[:-9]
        return Terbilang(u) + f + Terbilang(t)
    else:
        v = y[-12:]
        w = y[:-12]
        return Terbilang(w) + g + Terbilang(v)


a = Terbilang(1620000)
print a