#!/usr/bin/env python3

import os
import pickle
from generate_list import SimplePerson
from email.message import EmailMessage
from email.generator import BytesGenerator
from email.policy import EmailPolicy
from subprocess import Popen, PIPE

domain = 'zrounba.fr'
sender_name = 'Le Père Joël'
sender_email = 'pere.joel+donotreply@'+domain
mail_subject_fmt = 'Père Noël hétérogène'
mail_body_fmt = '''Bonjour {gifter.name},

Pour Noël, tu as été sélectionné(e) pour envoyer un cadeau à {gifted.name} !

Ses coordonnées sont les suivantes:
    - {gifted.name}
    - {gifted.address}
    - {gifted.tel}
    - {gifted.email}

Dans l'idée, il faudrait de préférence un cadeau personnel, fait à la main ou à
moins de 10€ (comme ça, tu dois forcément y mettre un peu du tien ou ce sera un
cadeau nul !).

Essaie de t'y prendre un peu en amont pour le livrer à temps !

Bisous et en te souhaitant un Noyeux Joël,
Le Père Joël'''

def main(do_it=False):
    with open('results.pkl', 'rb') as f:
        results = pickle.load(f)

    if not do_it:
        print('This only send data if you give it --ok')
        print('Would send the following mails:')
        print('')

    n = len(results)
    i = 0
    for result in results:
        gifter = result[0]
        gifted = result[1]

        #mail_body = mail_body_fmt.format(gifter=result[0], gifted=result[1])
        #mail_from = f'{sender_email}'
        #mail_to = f'{gifter.email}'
        mail_from = f'{sender_name} <{sender_email}>'
        mail_to = f'{gifter.name} <{gifter.email}>'
        mail_subject = mail_subject_fmt.format()
        mail_body = mail_body_fmt.format(gifter=gifter, gifted=gifted)

        msg = EmailMessage()
        msg['From'] = mail_from
        msg['To'] = mail_to
        msg['Subject'] = mail_subject
        msg.set_payload(mail_body, charset='utf-8')
        
        if do_it:
            #p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
            #p.communicate(msg.as_bytes())
            
            p = Popen(['sendmail', '-F', '-oi', gifter.email], stdin=PIPE)
            g = BytesGenerator(p.stdin, policy=msg.policy.clone(linesep='\r\n'))
            g.flatten(msg)
            p.stdin.close()
            rc = p.wait()

            i += 1
            print(f'{i}/{n} mails sent.')
        else:
            # because utf8 is 8b and transport is 7b, mail is normally encoded in base64
            # this is just a way to add the un-encoded text to the message before printing
            # trying to send it will give errors
            msg.set_payload(mail_body)
            print('-'*78)
            print(msg)
            print('-'*78)

    if do_it:
        if i != n:
            print('Not all mails were sent.')
        os.remove('results.pkl')


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == '--ok':
        main(do_it=True)
    else:
        main()
