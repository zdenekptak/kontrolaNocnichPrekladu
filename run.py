from preklad import Preklady

configCesta = "C:/Users/zdenek.ptak/Repository/Kontrola_prekladu/souborykekontrole.json"
config = "C:/Users/zdenek.ptak/Repository/Kontrola_prekladu/config.json"
emailZprava = Preklady.kontrola(configCesta)
Preklady.posliEmail(config, emailZprava)