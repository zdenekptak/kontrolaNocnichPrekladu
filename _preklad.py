import os
from datetime import datetime
import os.path, time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json

class Preklady:
    def __init__(self):
        pass
    
    def kontrolaVerze(self, verzeHeliosu, souborCesta):
        self.verzeHeliosu = verzeHeliosu
        self.souborCesta = souborCesta
        vysledkyPrekladuSouboru = []
        vysledkyOKKO = []
        for soubor, cesta in self.souborCesta.items():

            nowDate = datetime.now() # current date and time

            datumDnesniDen = int(nowDate.strftime("%d"))

            try:
                modification_time  = os.path.getmtime(cesta)
                datumSouboru = time.ctime(modification_time)
                datumSouboruDen = [int(s) for s in datumSouboru.split() if s.isdigit()][0]    
            except:
                datumSouboruDen = 'neni'

            if datumSouboruDen == datumDnesniDen:
                vyslZprava = (f"{self.verzeHeliosu} {soubor} je OK")
                vysledkyPrekladuSouboru.append([vyslZprava])
                vysledkyOKKO.append(1)
            elif datumSouboruDen == 'neni':
                vyslZprava = (f"{self.verzeHeliosu} soubor {soubor} neni ve složce!!!")
                vysledkyPrekladuSouboru.append([vyslZprava])
                vysledkyOKKO.append(0)
            else:
                vyslZprava = (f"{self.verzeHeliosu} {soubor} překlad neproběhl!!!")
                vysledkyPrekladuSouboru.append([vyslZprava])
                vysledkyOKKO.append(0)
            zprava = ''            
            for v in vysledkyPrekladuSouboru:
                vstring = v[0]
                zprava = zprava + '\n' + vstring 

        return zprava, vysledkyOKKO


    def vsechnyVerzeKontrola(self, configCesty):
        self.configCesty = configCesty

        with open(self.configCesty) as json_file:

            configCesty = json.load(json_file) 
        
        preklady = Preklady()
        
        okko = []
        konecnyVysledky = []
        #print(configCesty)
        for verzeHeliosu, souborCesta in configCesty.items():
            if verzeHeliosu == 'HeO2-Beta':
                heo2beta = preklady.kontrolaVerze(verzeHeliosu, souborCesta)[0]
                konecnyVysledky.append(heo2beta)
                seznamokkoheo2beta = preklady.kontrolaVerze(verzeHeliosu, souborCesta)[1]
                okko.append(seznamokkoheo2beta)
            elif verzeHeliosu == 'HeO2-RC':
                heo2rc = preklady.kontrolaVerze(verzeHeliosu, souborCesta)[0]
                konecnyVysledky.append(heo2rc)
                seznamokkoheo2rc = preklady.kontrolaVerze(verzeHeliosu, souborCesta)[1]
                okko.append(seznamokkoheo2rc)
            elif verzeHeliosu == 'HeO3-Beta':
                heo3beta = preklady.kontrolaVerze(verzeHeliosu, souborCesta)[0]
                konecnyVysledky.append(heo3beta)
                seznamokkoheo3beta = preklady.kontrolaVerze(verzeHeliosu, souborCesta)[1]
                okko.append(seznamokkoheo3beta)
            else:
                heo3rc = preklady.kontrolaVerze(verzeHeliosu, souborCesta)[0]
                konecnyVysledky.append(heo3rc)
                seznamokkoheo3rc = preklady.kontrolaVerze(verzeHeliosu, souborCesta)[1]
                okko.append(seznamokkoheo3rc)
        
        celkoveOKKO = []        
        for i in range(len(okko)):
            celkoveOKKO = celkoveOKKO + okko[i]

        if sum(celkoveOKKO) == len(celkoveOKKO):
            jevseok = True
        else:
            jevseok = False
        
        konecnazprava = ''
        for v in konecnyVysledky:
            vstring = v
            konecnazprava = konecnazprava + '\n' + vstring    
        return konecnazprava, jevseok
          
        

    def posliEmail(self,
                   config_soubor,
                   textZpravy, 
                   predmet,
                   attachment_location = ''):
        
        msg = MIMEMultipart()

        with open(config_soubor) as json_file:
            
            if predmet == True:
                config = json.load(json_file)
                odesilatel = config["odesilatel"]
                prijemci = config["prijemciok"]
                heslo = config["heslo"]
                predmet = "Noční buildy OK"
                msg['X-Priority'] = '3'
            else:
                config = json.load(json_file)
                odesilatel = config["odesilatel"]
                prijemci = config["prijemciko"]
                heslo = config["heslo"]
                predmet = "Noční buildy neproběhly!"
                msg['X-Priority'] = '1'

        msg['From'] = odesilatel
        msg['To'] = ", ".join(prijemci)
        msg['Subject'] = predmet

        msg.attach(MIMEText(textZpravy, 'plain'))

        if attachment_location != '':
            filename = os.path.basename(attachment_location)
            attachment = open(attachment_location, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % filename)
            msg.attach(part)

        try:
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.ehlo()
            server.starttls()
            server.login('zdenek.ptak@assecosol.com', heslo)
            text = msg.as_string()
            server.sendmail(odesilatel, prijemci, text)
            print('email odeslan')
            server.quit()
        except:
            print("SMPT server connection error")
        return True
