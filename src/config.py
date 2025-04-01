import os

# Configuración para envío de correo
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "user": "robot@fullpay.cl",
    "password": "sameyjbltojmaezo",
    "remitente": "robot@fullpay.cl",
    "recipients": os.getenv('EMAIL_RECIPIENTS', 'szamorano@fullpay.cl').split(',')
    #"recipients": ["fordinola@fullpay.cl", "szamorano@fullpay.cl", "lclarke@fullpay.cl", "cfreire@fullpay.cl", "rarmijo@fullpay.cl"]
}