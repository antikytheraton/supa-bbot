# coding: utf-8
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import json
from example.config import CONFIG
from fbmq import Attachment, Template, QuickReply, NotificationType
from example.fbpage import page
from algorithms.clasificador_eventos import event_filter



USER_SEQ = {}



@page.handle_optin
def received_authentication(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_auth = event.timestamp

    pass_through_param = event.optin.get("ref")

    print("Received authentication for user %s and page %s with pass "
          "through param '%s' at %s" % (sender_id, recipient_id, pass_through_param, time_of_auth))

    page.send(sender_id, "Authentication successful")


@page.handle_echo
def received_echo(event):
    message = event.message
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")
    print("page id : %s , %s" % (page.page_id, page.page_name))
    print("Received echo for message %s and app %s with metadata %s" % (message_id, app_id, metadata))


@page.handle_message
def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_message = event.timestamp
    message = event.message
    print("Received message for user %s and page %s at %s with message:"
          % (sender_id, recipient_id, time_of_message))
    print(message)

    seq = message.get("seq", 0)
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")

    message_text = message.get("text")
    message_attachments = message.get("attachments")
    quick_reply = message.get("quick_reply")

    seq_id = sender_id + ':' + recipient_id
    if USER_SEQ.get(seq_id, -1) >= seq:
        print("Ignore duplicated request")
        return None
    else:
        USER_SEQ[seq_id] = seq

    if quick_reply:
        quick_reply_payload = quick_reply.get('payload')
        print("quick reply for message %s with payload %s" % (message_id, quick_reply_payload))

        # if quick_reply_payload == "ESTADOS":
            

        # elif quick_reply_payload == "CATEGORIAS":
            
        
        # else:
        # page.send(sender_id, "Quick reply tapped")

    if message_text:

        if message_text == 'Categorias':
            page.send(sender_id, "Que evento estas buscando?",
              quick_replies=[QuickReply(title="Conciertos", payload="PICK_COMEDY"),
                             QuickReply(title="Conferencias", payload="PICK_COMEDY"),
                             QuickReply(title="Deportes", payload="PICK_COMEDY"),
                             QuickReply(title="Familiares", payload="PICK_COMEDY"),
                             QuickReply(title="Teatro", payload="PICK_COMEDY"),
                             QuickReply(title="Ferias y Expos", payload="PICK_COMEDY")],
              metadata="DEVELOPER_DEFINED_METADATA")

        elif message_text == 'Estados':
            page.send(sender_id, "A donde quieres ir?",
              quick_replies=[QuickReply(title="CDMX y Edomex", payload="PICK_COMEDY"),
                             QuickReply(title="Hidalgo", payload="PICK_COMEDY"),
                             QuickReply(title="Veracruz", payload="PICK_COMEDY"),
                             QuickReply(title="Puebla", payload="PICK_COMEDY"),
                             QuickReply(title="Guanajuato", payload="PICK_COMEDY"),],
              metadata="DEVELOPER_DEFINED_METADATA")

        else:
            send_message(sender_id, message_text)

    elif message_attachments:
        page.send(sender_id, "Message with attachment received")


@page.handle_delivery
def received_delivery_confirmation(event):
    delivery = event.delivery
    message_ids = delivery.get("mids")
    watermark = delivery.get("watermark")

    if message_ids:
        for message_id in message_ids:
            print("Received delivery confirmation for message ID: %s" % message_id)

    print("All message before %s were delivered." % watermark)


@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload

    print("Received postback for user %s and page %s with payload '%s' at %s"
          % (sender_id, recipient_id, payload, time_of_postback))

    if payload == "HELLO":
        page.send(sender_id, "Que onda?")
        page.send(sender_id, "Disfruta de los mejores eventos con nuestras ofertas :D")
        page.send(sender_id, "Realiza tu busqueda por artista o simplemente escribe el estado en donde vives!")
        page.send(sender_id, "Puedes realizar tu busqueda seleccionando cualquiera de las opciones o escribiendo directamente tu consulta ;p",
              quick_replies=[QuickReply(title="Categorias", payload="CATEGORIAS"),
                             QuickReply(title="Estados", payload="ESTADOS"),],
              metadata="DEVELOPER_DEFINED_METADATA")
        
    else:
        page.send(sender_id, "Postback called")


@page.handle_read
def received_message_read(event):
    watermark = event.read.get("watermark")
    seq = event.read.get("seq")

    print("Received message read event for watermark %s and sequence number %s" % (watermark, seq))


@page.handle_account_linking
def received_account_link(event):
    sender_id = event.sender_id
    status = event.account_linking.get("status")
    auth_code = event.account_linking.get("authorization_code")

    print("Received account link event with for user %s with status %s and auth code %s "
          % (sender_id, status, auth_code))


def send_message(recipient_id, text):
    # If we receive a text message, check to see if it matches any special
    # keywords and send back the corresponding example. Otherwise, just echo
    # the text we received.
    special_keywords = {
        "image": send_image,
        "gif": send_gif,
        "audio": send_audio,
        "video": send_video,
        "file": send_file,
        "button": send_button,
        "generic": send_generic,
        "receipt": send_receipt,
        "quick reply": send_quick_reply,
        "read receipt": send_read_receipt,
        "typing on": send_typing_on,
        "typing off": send_typing_off,
        "account linking": send_account_linking
    }

    if text in special_keywords:
        special_keywords[text](recipient_id)

    # elif mes_filtro(text.lower()) != False:
    #     page.send(recipient_id, str(mes_filtro(text.lower())), callback=send_text_callback, notification_type=NotificationType.REGULAR)

    # elif estado_filter(text.lower()) != False:
    #     page.send(recipient_id, str(estado_filter(text.lower())), callback=send_text_callback, notification_type=NotificationType.REGULAR)

    else:
        evento = text
        eventos = event_filter(evento.upper())
        evento_key = list(eventos.keys())
        evento_val = list(eventos.values())
        evento_tupla = [evento_key, evento_val]
        # print('************************************************')
        # print(evento_tupla)
        # print('\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')
        # print(evento_tupla[0][0])
        # print(evento_tupla[1][0])
        # print(evento_tupla[1][0][1])
        # print('------------------------------------------------')
        # print(evento_tupla[0][1])
        # print(evento_tupla[1][1])
        # print(evento_tupla[1][1][1])
        # print(len(evento_key))
        # print('\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')

        # elements = []

        # print('\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')
        # print(str(elements))
        # print('\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')

        if eventos == False:
            page.send(recipient_id, "Lo siento, no encontre coincidencias :/")

        else:
            if len(evento_key) == 1:
                page.send(recipient_id, Template.Generic([
                    Template.GenericElement(str(evento_tupla[0][0]),
                                        subtitle=str(evento_tupla[1][0][1]),
                                        item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                        image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                        buttons=[
                                            Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                            
                                            
                                        ]),
                ]))

            elif len(evento_key) == 2:
                page.send(recipient_id, Template.Generic([
                    Template.GenericElement(str(evento_tupla[0][0]),
                                        subtitle=str(evento_tupla[1][0][1]),
                                        item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                        image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                        buttons=[
                                            Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                            
                                            
                                        ]),
                    Template.GenericElement(str(evento_tupla[0][1]),
                                        subtitle=str(evento_tupla[1][1][1]),
                                        item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                        image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                        buttons=[
                                            Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                            
                                            
                                        ]),
                ]))

            elif len(evento_key) == 3:
                page.send(recipient_id, Template.Generic([
                    Template.GenericElement(str(evento_tupla[0][0]),
                                        subtitle=str(evento_tupla[1][0][1]),
                                        item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                        image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                        buttons=[
                                            Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                            
                                            
                                        ]),
                    Template.GenericElement(str(evento_tupla[0][1]),
                                        subtitle=str(evento_tupla[1][1][1]),
                                        item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                        image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                        buttons=[
                                            Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                            
                                            
                                        ]),
                    Template.GenericElement(str(evento_tupla[0][2]),
                                        subtitle=str(evento_tupla[1][2][1]),
                                        item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                        image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                        buttons=[
                                            Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                            
                                            
                                        ]),
                ]))

            elif len(evento_key) == 4:
                page.send(recipient_id, Template.Generic([
                Template.GenericElement(str(evento_tupla[0][0]),
                                    subtitle=str(evento_tupla[1][0][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][1]),
                                    subtitle=str(evento_tupla[1][1][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][2]),
                                    subtitle=str(evento_tupla[1][2][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][3]),
                                    subtitle=str(evento_tupla[1][3][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
            ]))

            elif len(evento_key) == 5:
                page.send(recipient_id, Template.Generic([
                Template.GenericElement(str(evento_tupla[0][0]),
                                    subtitle=str(evento_tupla[1][0][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][1]),
                                    subtitle=str(evento_tupla[1][1][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][2]),
                                    subtitle=str(evento_tupla[1][2][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][3]),
                                    subtitle=str(evento_tupla[1][3][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][4]),
                                    subtitle=str(evento_tupla[1][4][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
            ]))

            elif len(evento_key) == 6:
                page.send(recipient_id, Template.Generic([
                Template.GenericElement(str(evento_tupla[0][0]),
                                    subtitle=str(evento_tupla[1][0][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][1]),
                                    subtitle=str(evento_tupla[1][1][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][2]),
                                    subtitle=str(evento_tupla[1][2][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][3]),
                                    subtitle=str(evento_tupla[1][3][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][4]),
                                    subtitle=str(evento_tupla[1][4][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][5]),
                                    subtitle=str(evento_tupla[1][5][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
            ]))

            elif len(evento_key) == 7:
                page.send(recipient_id, Template.Generic([
                Template.GenericElement(str(evento_tupla[0][0]),
                                    subtitle=str(evento_tupla[1][0][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][1]),
                                    subtitle=str(evento_tupla[1][1][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][2]),
                                    subtitle=str(evento_tupla[1][2][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][3]),
                                    subtitle=str(evento_tupla[1][3][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][4]),
                                    subtitle=str(evento_tupla[1][4][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][5]),
                                    subtitle=str(evento_tupla[1][5][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][6]),
                                    subtitle=str(evento_tupla[1][6][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
            ]))

            elif len(evento_key) == 8:
                page.send(recipient_id, Template.Generic([
                Template.GenericElement(str(evento_tupla[0][0]),
                                    subtitle=str(evento_tupla[1][0][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][1]),
                                    subtitle=str(evento_tupla[1][1][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][2]),
                                    subtitle=str(evento_tupla[1][2][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][3]),
                                    subtitle=str(evento_tupla[1][3][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][4]),
                                    subtitle=str(evento_tupla[1][4][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][5]),
                                    subtitle=str(evento_tupla[1][5][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][6]),
                                    subtitle=str(evento_tupla[1][6][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][7]),
                                    subtitle=str(evento_tupla[1][7][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
            ]))

            elif len(evento_key) == 9:
                page.send(recipient_id, Template.Generic([
                Template.GenericElement(str(evento_tupla[0][0]),
                                    subtitle=str(evento_tupla[1][0][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][1]),
                                    subtitle=str(evento_tupla[1][1][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][2]),
                                    subtitle=str(evento_tupla[1][2][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][3]),
                                    subtitle=str(evento_tupla[1][3][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][4]),
                                    subtitle=str(evento_tupla[1][4][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][5]),
                                    subtitle=str(evento_tupla[1][5][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][6]),
                                    subtitle=str(evento_tupla[1][6][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][7]),
                                    subtitle=str(evento_tupla[1][7][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][8]),
                                    subtitle=str(evento_tupla[1][8][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
            ]))

            elif len(evento_key) == 10:
                page.send(recipient_id, Template.Generic([
                Template.GenericElement(str(evento_tupla[0][0]),
                                    subtitle=str(evento_tupla[1][0][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][1]),
                                    subtitle=str(evento_tupla[1][1][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][2]),
                                    subtitle=str(evento_tupla[1][2][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][3]),
                                    subtitle=str(evento_tupla[1][3][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][4]),
                                    subtitle=str(evento_tupla[1][4][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][5]),
                                    subtitle=str(evento_tupla[1][5][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][6]),
                                    subtitle=str(evento_tupla[1][6][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][7]),
                                    subtitle=str(evento_tupla[1][7][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][8]),
                                    subtitle=str(evento_tupla[1][8][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
                Template.GenericElement(str(evento_tupla[0][9]),
                                    subtitle=str(evento_tupla[1][9][1]),
                                    item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                    image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                        
                                        
                                    ]),
            ]))

            else:
                page.send(recipient_id, "No encontre eventos que coincidieran con tu busqueda :/")
                page.send(recipient_id, "Intenta con palabras clave ;)")





def send_text_callback(payload, response):
    print("SEND CALLBACK")


def send_image(recipient):
    page.send(recipient, Attachment.Image("http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg"))


def send_gif(recipient):
    page.send(recipient, Attachment.Image(CONFIG['SERVER_URL'] + "/assets/instagram_logo.gif"))


def send_audio(recipient):
    page.send(recipient, Attachment.Audio(CONFIG['SERVER_URL'] + "/assets/sample.mp3"))


def send_video(recipient):
    page.send(recipient, Attachment.Video(CONFIG['SERVER_URL'] + "/assets/allofus480.mov"))


def send_file(recipient):
    page.send(recipient, Attachment.File(CONFIG['SERVER_URL'] + "/assets/test.txt"))


def send_button(recipient):
    """
    Shortcuts are supported
    page.send(recipient, Template.Buttons("hello", [
        {'type': 'web_url', 'title': 'Open Web URL', 'value': 'http://web.superboletos.com:8001/SuperBoletos/index.do'},
        {'type': 'postback', 'title': 'tigger Postback', 'value': 'DEVELOPED_DEFINED_PAYLOAD'},
        {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+16505551234'},
    ]))
    """
    page.send(recipient, Template.Buttons("hello", [
        Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
        Template.ButtonPostBack("trigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
        
    ]))


@page.callback(['DEVELOPED_DEFINED_PAYLOAD'])
def callback_clicked_button(payload, event):
    print(payload, event)


def send_generic(recipient):
    page.send(recipient, Template.Generic([
        Template.GenericElement("rift",
                                subtitle="Next-generation virtual reality",
                                item_url="http://web.superboletos.com:8001/SuperBoletos/index.do",
                                image_url="http://opinamx.com/wp-content/uploads/2017/02/20217SuperBoletos.jpg",
                                buttons=[
                                    Template.ButtonWeb("Open Web URL", "http://web.superboletos.com:8001/SuperBoletos/index.do"),
                                    
                                    
                                ]),
        Template.GenericElement("touch",
                                subtitle="Your Hands, Now in VR",
                                item_url="https://www.oculus.com/en-us/touch/",
                                image_url=CONFIG['SERVER_URL'] + "/assets/touch.png",
                                buttons=[
                                    {'type': 'web_url', 'title': 'Open Web URL',
                                     'value': 'http://web.superboletos.com:8001/SuperBoletos/index.do'},
                                    {'type': 'postback', 'title': 'tigger Postback',
                                     'value': 'DEVELOPED_DEFINED_PAYLOAD'},
                                    {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+16505551234'},
                                ])
    ]))


def send_receipt(recipient):
    receipt_id = "order1357"
    element = Template.ReceiptElement(title="Oculus Rift",
                                      subtitle="Includes: headset, sensor, remote",
                                      quantity=1,
                                      price=599.00,
                                      currency="USD",
                                      image_url=CONFIG['SERVER_URL'] + "/assets/riftsq.png"
                                      )

    address = Template.ReceiptAddress(street_1="1 Hacker Way",
                                      street_2="",
                                      city="Menlo Park",
                                      postal_code="94025",
                                      state="CA",
                                      country="US")

    summary = Template.ReceiptSummary(subtotal=698.99,
                                      shipping_cost=20.00,
                                      total_tax=57.67,
                                      total_cost=626.66)

    adjustment = Template.ReceiptAdjustment(name="New Customer Discount", amount=-50)

    page.send(recipient, Template.Receipt(recipient_name='Peter Chang',
                                          order_number=receipt_id,
                                          currency='USD',
                                          payment_method='Visa 1234',
                                          timestamp="1428444852",
                                          elements=[element],
                                          address=address,
                                          summary=summary,
                                          adjustments=[adjustment]))


def send_quick_reply(recipient):
    """
    shortcuts are supported
    page.send(recipient, "What's your favorite movie genre?",
                quick_replies=[{'title': 'Action', 'payload': 'PICK_ACTION'},
                               {'title': 'Comedy', 'payload': 'PICK_COMEDY'}, ],
                metadata="DEVELOPER_DEFINED_METADATA")
    """
    page.send(recipient, "What's your favorite movie genre?",
              quick_replies=[QuickReply(title="Action", payload="PICK_ACTION"),
                             QuickReply(title="Comedy", payload="PICK_COMEDY")],
              metadata="DEVELOPER_DEFINED_METADATA")


@page.callback(['PICK_ACTION'])
def callback_picked_genre(payload, event):
    print(payload, event)


def send_read_receipt(recipient):
    page.mark_seen(recipient)


def send_typing_on(recipient):
    page.typing_on(recipient)


def send_typing_off(recipient):
    page.typing_off(recipient)


def send_account_linking(recipient):
    page.send(recipient, Template.AccountLink(text="Welcome. Link your account.",
                                              account_link_url=CONFIG['SERVER_URL'] + "/authorize",
                                              account_unlink_button=True))


def send_text_message(recipient, text):
    page.send(recipient, text, metadata="DEVELOPER_DEFINED_METADATA")
