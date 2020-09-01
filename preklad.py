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
    
    def kontrola():
        helios = {"HeO2-Beta" : "N:\HeliosIQ\Beta\Helios.exe", 
                  "HeO2-RC" : "N:\HeliosIQ\RC\Helios.exe", 
                  "HeO3-Beta" : "N:\HeliosIQ\HeO3_Beta\Helios.exe", 
                  "HeO3-RC" : "N:\HeliosIQ\HeO3_RC\Helios.exe"
                 }
        vysledek = []
        for h, cesta in helios.items():
            nowDate = datetime.now() # current date and time
            datumDnesniDen = int(nowDate.strftime("%d"))

            datumSouboru = time.ctime(os.path.getmtime(cesta))
    #         print(f"Poslední změna {h} proběhla: {datumSouboru}")

            datumVytvoreniSouboru = time.ctime(os.path.getctime(cesta))
    #         print(f"Souboru vutvoren: \n {datumVytvoreniSouboru}")

            datumSouboruDen = [int(s) for s in datumSouboru.split() if s.isdigit()][0]
            if datumSouboruDen == datumDnesniDen:
                vyslZprava = (f"{h} je OK")
                vysledek.append(vyslZprava)
            else:
                vyslZprava = (f"{h} překlad neproběhl!!!")
                vysledek.append(vyslZprava)
        vysledek =  vysledek[0] + '\n' + vysledek[1] + '\n' + vysledek[2] + '\n' + vysledek[3]
        return vysledek

    def ulozeniVysledku(vysledky):
        with open('probehlpreklad.txt', 'w') as filehandle:
            for listitem in vysledky:
                filehandle.write('%s\n' % listitem)

    def posliEmail(config_soubor,
                   textZpravy,
                   predmet = 'Noční překlady',
                   attachment_location = ''):
        
        with open(config_soubor) as json_file:
            
            config = json.load(json_file)
            
            odesilatel = config["odesilatel"]
            prijemci = config["prijemci"]
            heslo = config["heslo"]


        msg = MIMEMultipart()
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
