import smtplib

def send_email(
    reciever_e="pawn88@live.com",
    subject="Test Subject",
    body="Test Body",
    server_e="pawn88@live.com",
    server_p="Westside99", 
    host_addr='hotmail'):

    provider = {'hotmail':('smtp.live.com',587),
                'google':('smtp.gmail.com',587)}

    with smtplib.SMTP(provider[host_addr][0], provider[host_addr][1]) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(server_e, server_p)

        msg = f"Subject:{subject}\n\n{body}"

        smtp.sendmail(server_e, reciever_e, msg)

if __name__ == "__main__":
    send_email()