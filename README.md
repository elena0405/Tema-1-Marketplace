# Tema-1-Marketplace
Tema 1 Arhitectura Sistemelor de Calcul

Nume: Ionescu Elena
Grupa: 336CA


Tema 1 - Marketplace

1. Explicatie pentru solutia aleasa

Organizare

	In cadrul aceste teme, in constructorul clasei Marketplace, am creat o lista in care voi 
retine produsele publicate de fiecare producator tot sub forma de liste, in care indexarea se face 
in functie de id-ul producatorului. De aemenea, pentru a retine produsele care au fost 
achizitionate, dar nu cumparate, mai creez o lista, taken_products, ale carei elemente vor fi tot 
liste ce contin produsele achizitionate de la fiecare producator, unde indexarea se face in 
functie de id-ul producatorului. Tot in cadrul constructorului Marketplace, am o lista de liste, 
ce reprezinta cosurile cu produse. Am folosit un lock pe operatiile care nu sunt atomice din cod si 
la afisare, pentru a nu se intercala elementele afisate. Operatiile de sincronizare au fost facute 
in cadrul metodelor in clasa Marketplace. In clasele Producer si Consumer, am implementat metodele
respective.

	Consider ca aceasta tema a fost utila, deoarece am inteles mai bine cum functioneaza elementele
de sincronizare in Python si m-am familiarizat cu sintaxa aplicatiei.
	Consider ca implementarea este buna. Nu este cea mai eficienta implementare, dar faptul ca
folosesc lock-ul doar acolo unde este necesar salveaza mult timp din executia programului.


Implementare

	In cadrul temei, am implementat intregul enunt.
	Legat de dificultatile de implementare, pot spune ca mi-a luat putin timp sa ma gandesc cum
sa organizez datele. 
	Mi s-a parut interesant ca nu este nevoie sa fac lock in python pentru a face anumite operatii
pe liste (acest lucru era mentionat si in laborator, dar am trecut cu vederea la momentul respectiv).


Resurse utilizate

https://www.techiedelight.com/remove-all-items-from-list-python/
https://appdividend.com/2020/01/21/python-list-contains-how-to-check-if-item-exists-in-list/
https://ocw.cs.pub.ro/courses/asc/laboratoare/02
https://ocw.cs.pub.ro/courses/asc/laboratoare/01
https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
