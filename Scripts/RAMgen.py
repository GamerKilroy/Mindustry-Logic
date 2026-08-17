chars=",!$%'()*/:<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~"
charsf=chars+"0123456789"
clen=len(chars)
print(f"setRate 200")
for v in range(1000):
 i=v*6
 v1=chars[i%clen]+charsf[i//clen]
 i+=1
 v2=chars[i%clen]+charsf[i//clen]
 i+=1
 v3=chars[i%clen]+charsf[i//clen]
 i+=1
 v4=chars[i%clen]+charsf[i//clen]
 i+=1
 v5=chars[i%clen]+charsf[i//clen]
 i+=1
 v6=chars[i%clen]+charsf[i//clen]
 print(f"draw triangle {v1} {v2} {v3} {v4} {v5} {v6}")
print(f"stop")