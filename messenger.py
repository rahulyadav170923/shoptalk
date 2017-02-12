import json
from config import CONFIG
from fbmq import Attachment, Template, QuickReply, NotificationType
from fbpage import page
from api import getdata
from data import shirts, electronics, footwear, offers, previous_orders
from sentiment import sentiment_result

USER_SEQ = {}

start = "Hello! Ask me anything or choose from the menu in the bottom left"
greeting = "Hi Harish! Welcome to Shoptalk. We bring an amazing shopping experience. You can search for items or talk to us."
page.greeting(greeting)

@page.callback(['START_PAYLOAD'])
def start_callback(payload, event):
    page.send(event.sender_id, start)


page.show_persistent_menu([Template.ButtonPostBack('What are you looking for', 'MENU_PAYLOAD/1'),
                           Template.ButtonPostBack('Current Offers', 'MENU_PAYLOAD/2'),
                           Template.ButtonPostBack('Get the app', 'MENU_PAYLOAD/3'),
                           Template.ButtonPostBack('Contact Custome Care', 'MENU_PAYLOAD/4'),
                           Template.ButtonPostBack('Previous Orders', 'MENU_PAYLOAD/5')
                           ])


@page.callback(['BUY'])
def start_callback(payload, event):
    page.send(event.sender_id, start)


@page.callback(['MENU_PAYLOAD/5'])
def show_previous_orders(payload, event):
  a=[]
  for i in previous_orders:
    a.append(Template.GenericElement(i['title'],
                          subtitle=i['price'],
                          #item_url=i["link"],
                          image_url=i["image_url"],
                          buttons=[
                              Template.ButtonPostBack('Check Receipt', 'RECEIPT'),
                              #Template.ButtonPostBack('Bookmark', "ADDTOBOOKMARK"),
                          ]))
  page.send(event.sender_id, Template.Generic(a))


@page.callback(['MENU_PAYLOAD/2'])
def callback_offers(payload, event):
  a=[]
  for i in offers:
    a.append(Template.GenericElement(i['name'],
                          subtitle=i['price'],
                          item_url=i["link"],
                          image_url=i["image"],
                          buttons=[
                              Template.ButtonWeb("Explore", i["link"]),
                              Template.ButtonWeb("Share", i["link"]),
                              #Template.ButtonPostBack('Bookmark', "ADDTOBOOKMARK"),
                          ]))
  page.send(event.sender_id, Attachment.Image("https://media.giphy.com/media/Ejn6xH5mnmtMI/giphy.gif"))
  page.send(event.sender_id, Template.Generic(a))


@page.callback(['RECEIPT'])
def receipts(payload, event):
  for i in previous_orders:
    element = Template.ReceiptElement(title=i['title'],
                                      subtitle=i['subtitle'],
                                      quantity=i['quantity'],
                                      price=200,
                                      currency="USD",
                                      image_url=i['image_url']
                                      )

    address = Template.ReceiptAddress(street_1=i['street_1'],
                                      street_2=i['street_2'],
                                      city=i['city'],
                                      postal_code=i['postal_code'],
                                      state=i['state'],
                                      country=i['country'])

    summary = Template.ReceiptSummary(subtotal=200,
                                      shipping_cost=5,
                                      total_tax=10,
                                      total_cost=215)
    adjustment = Template.ReceiptAdjustment(name=i['name'], amount=1308)


    page.send(event.sender_id, Template.Receipt(recipient_name=i['receipt_name'],
                                            order_number=i['order_number'],
                                            currency="USD",
                                            payment_method='visa',
                                            timestamp="1428444852",
                                            elements=[element],
                                            address=address,
                                            summary=summary,
                                            adjustments=[adjustment]))


@page.callback(['MENU_PAYLOAD/4'])
def customer_care(payload, event):
  click_menu = payload.split('/')[1]
  buttons = [
  { "type":"phone_number","title":"Call Representative","payload":"01244414888"},
  {'type': 'postback', 'title': 'Share your experience through me', 'payload': 'REVIEW'},
  ]
  page.send(event.sender_id, Template.Buttons("Need Assistance", buttons))


@page.callback(['REVIEW'])
def callback_tshirts(payload, event):
  page.send(event.sender_id, " Please state experience. ")


@page.callback(['TSHIRT'])
def callback_tshirts(payload, event):
  a=[]
  for i in shirts:
    a.append(Template.GenericElement(i['name'],
                          subtitle=i['price'],
                          item_url=i["link"],
                          image_url=i["image"],
                          buttons=[
                              Template.ButtonWeb("Open Web URL", i["link"]),
                              Template.ButtonWeb("Share", i["link"]),
                              #Template.ButtonPostBack('Bookmark', "ADDTOBOOKMARK"),
                              Template.ButtonPostBack('Buy', "BUY")
                          ]))
  page.send(event.sender_id, Template.Generic(a))


@page.callback(['ELECTRONICS'])
def callback_electronics(payload, event):
  a=[]
  for i in electronics:
    a.append(Template.GenericElement(i['name'],
                          subtitle=i['price'],
                          item_url=i["link"],
                          image_url=i["image"],
                          buttons=[
                              Template.ButtonWeb("Open Web URL", i["link"]),
                              Template.ButtonWeb("Share", i["link"]),
                              #Template.ButtonPostBack('Bookmark', "BOOKMARK"),
                              Template.ButtonPostBack('Buy', "BUY")
                          ]))
  page.send(event.sender_id, Template.Generic(a))

@page.callback(['FOOTWEAR'])
def callback_footwear(payload, event):
  a=[]
  for i in footwear:
    a.append(Template.GenericElement(i['name'],
                          subtitle=i['price'],
                          item_url=i["link"],
                          image_url=i["image"],
                          buttons=[
                              Template.ButtonWeb("Open Web URL", i["link"]),
                              Template.ButtonWeb("Share", i["link"]),
                              #Template.ButtonPostBack('Bookmark', "ADDTOBOOKMARK"),
                              Template.ButtonPostBack('Buy', "BUY")
                          ]))
  page.send(event.sender_id, Template.Generic(a))


@page.callback(['MENU_PAYLOAD/1'])
def choose_category(payload, event):
  click_menu = payload.split('/')[1]
  buttons = [
  {'type': 'postback', 'title': 'T-Shirts', 'payload': 'TSHIRT'},
  {'type': 'postback', 'title': 'Electronics', 'payload': 'ELECTRONICS'},
  {'type': 'postback', 'title': 'Footwear', 'payload': 'FOOTWEAR'}
  ]
  page.send(event.sender_id, Template.Buttons("Please choose a category", buttons))


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
    result = getdata(message_text)
    print(result)
    if result['action'] == "show_items":
        show_items(result,sender_id)
    elif result['action'] == "install_android_app":
        install_android_app(result,sender_id)
    elif result['action'] == "install_ios_app":
        install_ios_app(result,sender_id)
    elif result['action'] == "install_windows_app":
        install_windows_app(result,sender_id)
    elif result['action'] == "greetings":
        greetings(result,sender_id)
    elif result['action'] == "show_shirts":
        show_shirts(result,sender_id)
    elif result['action'] == "show_electronics":
        show_electronics(result,sender_id)
    elif result['action'] == "show_shoes":
        show_shoes(result,sender_id)
    elif result['action'] == "special_offers":
        special_offers(result,sender_id)
    elif result['action'] == "show_review":
        show_review(result,sender_id)


def parse_array(array,sender_id):
    for i in array:
        if "imageUrl" in i.keys():
            page.send(sender_id, Attachment.Image(i['imageUrl']))
        elif "speech" in i.keys():
            page.send(sender_id, str(i['speech']))


def show_items(result,sender_id):
    parse_array(result['messages'],sender_id)


def install_android_app(result,sender_id):
    parse_array(result['messages'],sender_id)


def install_ios_app(result,sender_id):
    parse_array(result['messages'],sender_id)


def install_windows_app(result,sender_id):
    parse_array(result['messages'],sender_id)


def greetings(result,sender_id):
    parse_array(result['messages'],sender_id)


def show_review(result,sender_id):
    a = sentiment_result(result['messages'][0]['speech'])
    if a == 'negative':
      page.send(sender_id, " We are sorry about the inconvenience . Our Custome care will reach out to you shortly .")
    else:
      page.send(sender_id, " We are glad to have your positive feedback . Keep shoptalking . ")


def show_shoes(result,sender_id):
  a=[]
  for i in footwear:
    a.append(Template.GenericElement(i['name'],
                          subtitle=i['price'],
                          item_url=i["link"],
                          image_url=i["image"],
                          buttons=[
                              Template.ButtonWeb("Open Web URL", i["link"]),
                              Template.ButtonWeb("Share", i["link"]),
                              #Template.ButtonPostBack('Bookmark', "BOOKMARK"),
                              Template.ButtonPostBack('Buy', "BUY")
                          ]))
  page.send(sender_id, Template.Generic(a))


def show_shirts(result,sender_id):
  a=[]
  for i in shirts:
    a.append(Template.GenericElement(i['name'],
                          subtitle=i['price'],
                          item_url=i["link"],
                          image_url=i["image"],
                          buttons=[
                              Template.ButtonWeb("Open Web URL", i["link"]),
                              Template.ButtonWeb("Share", i["link"]),
                              #Template.ButtonPostBack('Bookmark', "ADDTOBOOKMARK"),
                              Template.ButtonPostBack('Buy', "BUY")
                          ]))
  page.send(sender_id, Template.Generic(a))


def show_electronics(result,sender_id):
  a=[]
  for i in electronics:
    print(i)
    a.append(Template.GenericElement(i['name'],
                          subtitle=i['price'],
                          item_url=i["link"],
                          image_url=i["image"],
                          buttons=[
                              Template.ButtonWeb("Open Web URL", i["link"]),
                              Template.ButtonWeb("Share", i["link"]),
                              #Template.ButtonPostBack('Bookmark', "BOOKMARK"),
                              Template.ButtonPostBack('Buy', "BUY")
                          ]))
  page.send(sender_id, Template.Generic(a))


def special_offers(result,sender_id):
  a=[]
  for i in offers:
    a.append(Template.GenericElement(i['name'],
                          subtitle=i['price'],
                          item_url=i["link"],
                          image_url=i["image"],
                          buttons=[
                              Template.ButtonWeb("Explore", i["link"]),
                              Template.ButtonWeb("Share", i["link"]),
                              #Template.ButtonPostBack('Bookmark', "ADDTOBOOKMARK"),
                          ]))
  page.send(sender_id, Attachment.Image("https://media.giphy.com/media/Ejn6xH5mnmtMI/giphy.gif"))
  page.send(sender_id, Template.Generic(a))

