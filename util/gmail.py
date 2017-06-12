import smtplib
import json


class Gmail:
    def __init__(self):
        # Load email credentials
        self.credentials = json.load(open('credentials/email_credentials.json'))

    def notify(self, listing, recipients, u_of_t_address):
        """
            Sends the email through the gmail account
        Args:
            listing: (Listing) the listing to notify about

        Returns:
            None

        """
        # TODO: should notify of success or failure

        msg = "\r\n".join([
            "From: " + self.credentials['username'],
            "To: " + '\,'.join(recipients),
            "Subject: New 2 Bedroom Found: " + listing.get_title(),
            "",
            "Viability Score: " + str(listing.get_viability(u_of_t_address)),
            "Commute Time: " + str(listing.get_commute_time(u_of_t_address)),
            "Price: " + str(listing.get_cost()),
            "URL: " + listing.url
        ])
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.credentials['username'], self.credentials['password'])
        server.sendmail(self.credentials['username'], recipients, msg)
        server.quit()
