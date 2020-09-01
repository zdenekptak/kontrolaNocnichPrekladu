from preklad import Preklady

config = "C:/Users/zdenek.ptak/Repository/Kontrola_prekladu/config.json"
vysledky = Preklady.kontrola()
Preklady.ulozeniVysledku(vysledky)
Preklady.posliEmail(config,
                    vysledky,
                   )
