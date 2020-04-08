import smtplib

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

THE_ADDRESS = 'THE_ADDRESS@example.comm'
PASSWORD = 'mypassword'
your_port_here = 'the_port'

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """ 
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def notifyByEmail(email_list):
    message_template = read_template('assets/message.txt')

    try:
        # set up the SMTP server
        s = smtplib.SMTP(host='your_host_address_here', port=your_port_here)
        s.starttls()
        s.login(THE_ADDRESS, PASSWORD)

        # For each contact, send the email:
        for resp in email_list:
            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=email['name'])

            # setup the parameters of the message
            msg['From']=THE_ADDRESS
            msg['To']= resp['email']
            msg['Subject']="Notification from WFP"
            
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            
            #print massage
            print(msg)

            # send the message via the server set up earlier.
            s.send_message(msg)
            print ('email sent')
            del msg
        # Terminate the SMTP session and close the connection
        s.quit()
    except:
        print ('error sending mail')
    
        
    
    

