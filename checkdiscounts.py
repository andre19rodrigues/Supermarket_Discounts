#!/usr/bin/env python
# -*- coding: utf-8 -

import csv
import mechanize
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

br = mechanize.Browser()
br.set_handle_equiv(False)
br.set_handle_robots(False)
br.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64; rv:18.0)Gecko/20100101 Firefox/18.0 (compatible;)'),('Accept', '*/*')]

discountsmessage = ''

def checkdiscount(currentprice, products):

    global discountsmessage
    normalprice = products[1]

    if currentprice < normalprice:
        discountsmessage = discountsmessage + products[0] + '  ->  Before: '+ str(normalprice) + '  Now: '+ str(currentprice) + '  Discount %: ' + \
                  str(round(100 - (currentprice * 100 / normalprice), 2)) + '\n'


with open('products.csv', 'rb') as csvfile:
    products = csv.reader(csvfile)

    for row in products:
        html = br.open(row[2])
        soup = BeautifulSoup(html, 'html.parser')
        a_tags = soup.findAll('div', {'class': 'updListPrice'})

        for a in a_tags:
            price = a.text
            removespace = price.replace(' ', '')
            removeeuro = removespace.replace('€'.decode('utf-8'), '')
            final = removeeuro.replace(',', '.')
            checkdiscount(float(final), row)


with open('discounts.txt', 'r') as content_file:
    content = content_file.read()

if(discountsmessage != '' and discountsmessage != content):

    file = 'discounts.txt'
    f = open(file, 'w+')
    f.write(discountsmessage)
    f.close()

    username = 'email@email.example'
    password = 'pwd'
    to = ['email@email.example']

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = "You"
    msg['Subject'] = 'Discounts'

    msg.attach(MIMEText(discountsmessage, 'plain'))

    try:
                                   #example for gmail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(username, to, text)
        server.close()

        print('Email sent!')
    except:
        print('Error sending email!')