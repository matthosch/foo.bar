def answer(m, f):
    mach = long(m)
    facula = long(f)
    count = 0
    while mach > 0 and facula > 0:
        if facula - mach == mach or mach - facula == facula and count > 0:
            return "impossible"
        #print count, mach, facula
        if facula > mach:  
            count += facula/mach
            facula = facula - mach * (facula/mach)       
        else:
            count += mach/facula
            mach = mach - facula * (mach/facula)
    return str(count - 1)

print answer("4", "7")

print answer("2", "4")
