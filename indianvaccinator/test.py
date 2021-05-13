import yagmail
from configs import config

yag = yagmail.SMTP(config.sender_address, config.sender_pass)
contents = [
    "This is the body, and here is just text http://somedomain/image.png",
    "You can find an audio file attached.", '/local/path/to/song.mp3'
]
yag.send('thoratomkar29@gmail.com', 'subject', contents)