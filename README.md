# Email Client

Ten skrypt implementuje klienta e-mailowego. Umożliwia odczytywanie i wysyłanie e-maili z konta Gmail, a także automatyczne odpowiadanie na e-maile, gdy użytkownik jest nieobecny.

## Wymagania

* Python 3.10
* PyQt5
* configparser
* imaplib
* smtplib
* email

## Instalacja

1. Sklonuj repozytorium:
    ```
    git clone https://github.com/Weisjan/Email-client.git
    ```

2. Uzupełnij plik `config.ini`
    - email i hasło/token

## Struktura plików

```
Email-Client
├── config.ini
├── Client.py
└── Readme.md
```

| No | File Name | Details |
|----|------------|---------|
| 1  | config.ini | Plik konfiguracyjny zawierający dane logowania do konta e-mail |
| 2  | Client.py | Główny skrypt aplikacji |
| 3  | Readme.md | Plik Readme |

## Opis działania

Skrypt `Client.py` służy do obsługi e-maili przy użyciu GUI stworzonego w PyQt5.

1. **Konfiguracja**: Skrypt wczytuje konfigurację z pliku `config.ini`, który zawiera informacje o e-mailu i haśle do konta Gmail.
2. **Interfejs użytkownika**: Tworzony jest interfejs użytkownika z przyciskami do odczytywania i wysyłania e-maili, obszarem tekstowym do wyświetlania e-maili oraz formularzem do wysyłania nowych wiadomości.
3. **Odczytywanie e-maili**: Po kliknięciu przycisku "Odczytaj e-maile" aplikacja łączy się z serwerem IMAP Gmaila, pobiera i wyświetla ostatnie 10 e-maili. Użytkownik może filtrować e-maile według słowa kluczowego.
4. **Wysyłanie e-maili**: Po wypełnieniu formularza i kliknięciu przycisku "Wyślij e-mail" aplikacja wysyła wiadomość e-mail za pomocą serwera SMTP Gmaila.
5. **Autoresponder**: Jeśli użytkownik jest nieobecny przez więcej niż 60 sekund, aplikacja automatycznie odpowiada na ostatnio otrzymanego e-maila z informacją o nieobecności.

## Uwagi

- W przypadku błędów połączenia podczas odczytywania lub wysyłania e-maili, aplikacja wyświetli odpowiednie komunikaty błędów.
- Skrypt automatycznie sprawdza czas ostatniej aktywności użytkownika i wysyła autoresponder w przypadku dłuższej nieaktywności.

## Autor

[Jan Weis](https://github.com/Weisjan)
