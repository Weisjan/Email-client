from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QPushButton, QTextEdit, QLabel, QLineEdit
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import imaplib
import email
import re
from datetime import datetime, timedelta
import configparser

class EmailClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Email Client")
        self.setGeometry(100, 100, 600, 400)

        # Wczytaj dane z pliku konfiguracyjnego
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.email = self.config['Email']['email']
        self.password = self.config['Email']['password']

        # layout głównego okna
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # layout przycisków
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        # przyciski
        self.read_button = QPushButton("Odczytaj e-maile")
        self.read_button.clicked.connect(self.read_emails)
        button_layout.addWidget(self.read_button)

        self.send_button = QPushButton("Wyślij e-mail")
        self.send_button.clicked.connect(self.send_email)
        button_layout.addWidget(self.send_button)

        # layout obszaru tekstowego
        text_layout = QHBoxLayout()
        main_layout.addLayout(text_layout)

        # obszar tekstowy z e-mailami
        self.email_text = QTextEdit()
        self.email_text.setReadOnly(True)
        text_layout.addWidget(self.email_text)

        # layout pól formularza
        form_layout = QVBoxLayout()
        text_layout.addLayout(form_layout)

        # pola formularza
        form_layout.addWidget(QLabel("Do:"))
        self.to_field = QLineEdit()
        form_layout.addWidget(self.to_field)

        form_layout.addWidget(QLabel("Temat:"))
        self.subject_field = QLineEdit()
        form_layout.addWidget(self.subject_field)

        form_layout.addWidget(QLabel("Treść:"))
        self.body_field = QTextEdit()
        form_layout.addWidget(self.body_field)

        # pole tekstowe dla słowa kluczowego
        form_layout.addWidget(QLabel("Filtruj maile po słowie kluczowym:"))
        self.keyword_field = QLineEdit()
        form_layout.addWidget(self.keyword_field)

        self.last_seen = datetime.now()  # zapisujemy czas ostatniej aktywności

    def check_autoresponder(self):
        # sprawdzamy, czy adresat jest nieobecny
        now = datetime.now()
        if (now - self.last_seen) > timedelta(seconds=60):
            # jeśli minęło więcej niż 60 sekund, wysyłamy autoresponder
            self.send_autoresponder()

    def send_autoresponder(self):
        try:
            # tworzymy odpowiedź autorespondera
            message = MIMEMultipart()
            message['From'] = self.email
            message['To'] = self.last_email_from  # adres ostatniego nadawcy
            message['Subject'] = 'Automatyczna odpowiedz: Nieobecny'
            body = 'Jestem aktualnie nieobecny. Odpowiem na Twoją wiadomość jak najszybciej.'
            message.attach(MIMEText(body, 'plain'))

            # wysyłamy odpowiedź autorespondera
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.login(self.email, self.password)
                smtp_server.send_message(message)

            QMessageBox.information(self, "Wysłano autoresponder!", "Odpowiedź autorespondera została pomyślnie wysłana.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wysłać autorespondera: {str(e)}")

    def read_emails(self):
        self.email_text.clear()
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.email, self.password)
            mail.select('inbox')
            status, data = mail.search(None, 'ALL')

            mail_ids = data[0].split()[-10:]
            keyword = self.keyword_field.text().strip()
            autoresponder_sent = False

            for i in mail_ids:
                status, data = mail.fetch(i, '(RFC822)')
                for response_part in data:
                    if not isinstance(response_part, tuple):
                        continue

                    # Tworzymy obiekt wiadomości
                    message = email.message_from_bytes(response_part[1])

                    # Dekodowanie nagłówków
                    mail_from_raw = decode_header(message['From'])[0]
                    mail_from = mail_from_raw[0].decode(mail_from_raw[1]) if isinstance(mail_from_raw[0], bytes) else mail_from_raw[0]

                    subject_raw = decode_header(message['Subject'])[0]
                    mail_subject = subject_raw[0].decode(subject_raw[1]) if isinstance(subject_raw[0], bytes) else subject_raw[0]

                    # Treść wiadomości
                    if message.is_multipart():
                        mail_content = ''
                        for part in message.walk():
                            if part.get_content_type() == 'text/plain':
                                mail_content += part.get_payload(decode=True).decode()
                    else:
                        mail_content = message.get_payload(decode=True).decode()

                    self.last_email_from = mail_from  # do autorespondera

                    # Filtrowanie i wyświetlanie
                    if not keyword or re.search(keyword, mail_content, re.IGNORECASE):
                        self.email_text.append(f'From: {mail_from}')
                        self.email_text.append(f'Subject: {mail_subject}')
                        self.email_text.append(f'Content: {mail_content}')
                        self.email_text.append('-' * 40)

                    # Autoresponder tylko dla ostatniego maila
                    if i == mail_ids[-1] and 'nieobecny' not in mail_content.lower() and not autoresponder_sent:
                        self.check_autoresponder()
                        autoresponder_sent = True

            self.last_seen = datetime.now()
            mail.logout()

        except imaplib.IMAP4.error as e:
            QMessageBox.critical(self, "Błąd", f"Błąd IMAP: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił problem: {str(e)}")


    def send_email(self):
        try:
            # pobieramy dane z pól formularza
            to = self.to_field.text()
            subject = self.subject_field.text()
            body = self.body_field.toPlainText()

            # wysyłamy e-mail
            message = MIMEMultipart()
            message['From'] = self.email
            message['To'] = to
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.login(self.email, self.password)
                smtp_server.send_message(message)

            QMessageBox.information(self, "Wysłano maila!", "Wiadomość została pomyślnie wysłana.")

            # czyszczenie pól formularza po wysłaniu e-maila
            self.to_field.setText("")
            self.subject_field.setText("")
            self.body_field.setText("")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wysłać e-maila: {str(e)}")


if __name__ == "__main__":
    app = QApplication([])
    email_client = EmailClient()
    email_client.show()
    app.exec_()
