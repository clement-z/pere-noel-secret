#! python3

from generate_list import SimplePerson
from email.mime.text import MIMEText
import pickle

mail_subject_fmt = 'Père noël secret de la bande hétérogène'
mail_body_fmt = '''
Salut {gifter.name},

Pour le Père Noël secret, tu as été sélectionné(e) pour envoyer un cadeau à
{gifted.name} !

Ses coordonnées sont les suivantes:
    {gifted.name}
    {gifted.address}
    {gifted.tel}
    {gifted.email}

Dans l'idée, il faudrait de préférence un cadeau personnel, fait à la main ou à
moins de 10€ (comme ça, tu dois forcément y mettre un peu du tiens ou ce sera
un cadeau nul !). Essaie de t'y prendre un peu en amont pour le livrer à temps !

Bisous et en te souhaitant un joyeux noël,
Python et sendmail
'''

with open('results.pkl', 'rb') as f:
    results = pickle.load(f)

for result in results:
    gifter = result[0]
    gifted = result[1]

    #mail_body = mail_body_fmt.format(gifter=result[0], gifted=result[1])
    mail_body = mail_body_fmt.format(gifter=gifter, gifted=gifted)
    msg = MIMEText(mail_body)
    msg['From'] = 'pere.noel.donotreply@pere.noel.zrounba.fr'
    msg['To'] = gifter.email
    msg['Subject'] = mail_subject_fmt.format()
    print(msg)
    
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(msg.as_bytes())
    status = p.close()
    print('sendmail status:', status)


