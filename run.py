from preklad import Preklady

souboryKeKonrole = "C:/Helios/Repository/kontrolaNocnichPrekladu/souborykekontrole.json"
config = "C:/Helios/Repository/kontrolaNocnichPrekladu/configtest.json"
attachment_locations = ["C:/Helios/Repository/kontrolaNocnichPrekladu/log.txt",
                        "C:/Helios/Repository/kontrolaNocnichPrekladu/test.txt"]
preklady = Preklady()
emailZprava = preklady.vsechnyVerzeKontrola(souboryKeKonrole)[0]
predmet = preklady.vsechnyVerzeKontrola(souboryKeKonrole)[1]

if predmet == True:
    preklady.posliEmail(config, emailZprava, predmet, attachment_locations)
else:
    preklady.posliEmail(config, emailZprava, predmet, attachment_locations)
