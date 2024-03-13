from bardapi import BardCookies
import datetime

cookie_dict = {
    "__Secure-1PSID": "fAgINmR4clgCqEFH94N9n9JeegI4naRyDXyoB6iOGb38fl9HhIBPHZ2JQ4LN8K0XcT4Uuw.",
    "__Secure-1PSIDTS": "sidts-CjIBPVxjSgefthsmEsL7ksbok4ARCg0jyPzZYl6i4jGUpfRNdd4tukOXaGRB0zfdgBD1rhAA",
    "__Secure-1PSIDCC": "ABTWhQFHk-AacRcZEoFbNARQjZ9TNw4cp9Vk7trlNKn9rlbQ045MYm1Y8GCzsRvSjgtVit_WN2Cb"
}

bard = BardCookies(cookie_dict=cookie_dict)

while True:
    print("enter text")
    query = input()
    reply = bard.get_answer(query)['content']
    print(reply)
