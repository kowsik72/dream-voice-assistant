# # Price Scrapper 

# #### We'll just take a product and if the price falls below a threshold, we'll set it to send an email to us. You could also do things like writing in a db or storing it to a CSV file.

import requests #used to fetch websites
import smtplib # used to send emails
from bs4 import BeautifulSoup4
import time #To continuously check for price drop



#URL : the link to the product on flipkart
#header: headers for the http request. You can get your user gaent by googleing - "My user agent"1
URL=str(input("Enter the product URL:https://www.flipkart.com/acer-27-inch-full-hd-led-backlit-ips-panel-white-colour-monitor-ha270/p/itmfdfdjvfyzuyws?pid=MONFDFDJ6DG7X6YC&lid=LSTMONFDFDJ6DG7X6YCYZEWNU&marketplace=FLIPKART&store=6bo%2Fg0i%2F9no&srno=b_1_1&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_3_L2_view-all&fm=organic&iid=en_qA25oxQqcb69XliSqaHiAKXp7zoqsJ_njRADL3DJLc3KAkLCrZJpKbn1v2sYgtOL-NeHxedTgb60iNbrwi1Bd_UFjCTyOHoHZs-Z5_PS_w0%3D&ppt=hp&ppn=homepage&ssid=i96h1zi4r40000001706370999098"))
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}



def check_price():
    '''Function called when there is a price check to be made '''
    
    #Loads the HTML ans stores in page
    page = requests.get(URL, headers=headers)
    
    #Enables use to parse the HTMl through html parser
    soup = BeautifulSoup(page.content, 'html.parser')
    1
    #Gets the title of the product by looking for <span> tag in the HTML code with the classname "_35KyD6"
    title = soup.find("span", {"class": "B_NuCI"}).get_text()
    print("Title of the product is:",title)
    
    #Gets the price of the product by looking for <div> tag in the HTML code with the classname "_35KyD6"
    # [1:] is used to truncate the '₹' symbol and replace method to eradicate any commas if present
    price = float(soup.find("div", {"class": "_30jeq3 _16Jk6d"}).get_text()[1:].replace(',',''))
    
    print("Price of the product is: ",price) #prints the price
    x=int(input("Enter the threshold price:"))                   
    if( price < x ): #If the price falls below threshold, send an email
        sendmail()
    else:
        print("We will send you a mail when the price is down")
        y=str(input("Enter mail id:venkat_mylavarapu@srmap.edu.in"))
def sendmail():
    '''Function called when the email needs to be sent '''
    
    # Defines an SMTP client session with the host name, here being, smtp.gmail.com as we will be using Gmail
    # to send our emails. 587 is the port number for Gmail's TLS
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    
    server.starttls() #Put the SMTP connection in TLS mode. All SMTP commands that follow will be encrypted
    
    
    #Your email and app password. Follow the steps in the readme file to get your app password
    server.login('nadellaujwala22@gmail.com', 'wnhd yjps uguu bzsh')
    
    subject = 'Hey! Price fell down' #Subject of the email
    body = 'Check the link ' + URL #Body of the email
    msg = f"Subject: {subject}\n\n{body}" #Aggregation
    y=str(input("Enter your mail id:"))
    server.sendmail('nadellaujwala22@gmail.com', y, msg) #Sending the email
    
    print('Email Sent')
    
    server.quit() #Closing the connection



while(True):
    check_price()
    time.sleep(60*60) #Checks price every 60*60 seconds i.e, every hour