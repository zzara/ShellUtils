import socket
host = input('Enter the host: ')
addr = socket.gethostbyname(host)
octOne, octTwo, octTri, octFur = [int(n) for n in addr.split('.')]
xOne = octOne * (256**3)
xTwo = octTwo * (256**2)
xTri = octTri * (256)
xFur = octFur
xAll = xOne + xTwo + xTri + xFur
print(f"Decimal address: http://{xAll}/")
print(f"IP address: http://{addr}/")
print(f"Domain: http://{host}/")
