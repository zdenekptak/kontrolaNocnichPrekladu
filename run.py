from preklad import Preklady

configCesta = "C:/Users/zdenek.ptak/Repository/Kontrola_prekladu/souborykekontrole.json"
config = "C:/Users/zdenek.ptak/Repository/Kontrola_prekladu/config.json"
preklady = Preklady()
emailZprava = preklady.vsechnyVerzeKontrola(configCesta)[0]
predmet = preklady.vsechnyVerzeKontrola(configCesta)[1]

if predmet == True:
    preklady.posliEmail(config, emailZprava, predmet)
else:
    preklady.posliEmail(config, emailZprava, predmet)
