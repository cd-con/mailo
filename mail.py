import imaplib
import email
import os
from email.header import decode_header


class IMAP:
    """
    Class for mailing using IMAP protocol

    :param server IMAP server address
    :param login user login, such as "email@emailng.com"
    :param password user password
    """

    def __init__(self, server, login, password):
        self.mail = imaplib.IMAP4_SSL(server)
        self.mail.login(login, password)

    def _clean_(self, text):
        # чистый текст для создания папки
        return "".join(c if c.isalnum() else "_" for c in text)

    def getMails(self, folder):
        status, messages = self.mail.select("INBOX")
        N = 25
        messages = int(messages[0])

        result = []

        for i in range(messages, messages - N, -1):
            res, msg = self.mail.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)
                    From, encoding = decode_header(msg.get("From"))[0]

                    if isinstance(From, bytes):
                        if encoding is not None:
                            From = From.decode(encoding)
                        else:
                            print("ERR: ENCODING IS NOT DEFINED!")
                            break

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                pass  # body
                            elif "attachment" in content_disposition:
                                filename = part.get_filename()
                                if filename:
                                    folder_name = self._clean_(subject)
                                    try:
                                        if not os.path.isdir(folder_name):
                                            os.mkdir(f"cache/files/{folder_name}")
                                    except:
                                        print("File path already exsists")
                                    filepath = os.path.join(f"cache/emails/{folder_name}", filename)
                                    try:
                                        open(filepath, "wb").write(part.get_payload(decode=True))
                                    except:
                                        print("File already exsists")
                    else:
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            pass  # body
                    if content_type == "text/html":
                        folder_name = self._clean_(subject)
                        try:
                            if not os.path.isdir(folder_name):
                                os.mkdir(f"cache/emails/{folder_name}")
                        except:
                            print("File path already exsists")
                        filename = "index.html"
                        filepath = os.path.join(f"cache/emails/{folder_name}", filename)
                        # write the file
                        try:
                            open(filepath, "w").write(body)
                        except:
                            print("File already exsists")
                        body = f"!HTML {filepath}"

                    if body is not None:
                        result.append([i, subject, From, body])
                    else:
                        result.append([i, subject, From, "Пусто"])
        return result
