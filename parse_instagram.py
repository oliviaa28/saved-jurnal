import json 
from datetime import datetime

def fix_text(text):
    '''
    from the instagram export, the text is broken -> the emojis/ " / ' are ecoded wrong
    for example:  \u00e2\u0080\u0099 should be ', but it s not
    (bc they aew wirtten in utf-8 encoding, but every byte is saved as a separate character) 

    this function fixes the text from the posts
    '''
    try:
        encodedText= text.encode("latin-1")
        repairedText = encodedText.decode("utf-8")
        return repairedText
    except (UnicodeEncodeError,UnicodeDecodeError) :
        return text


def parse_post(item):
    post = {"url": None ,
            "caption": None }
    
    for i in item["label_values"]:
        if "label" in i:
            if i["label"] == "URL":
                post["url"] = i["value"]
            elif  i["label"] == "Subtitrare":
                post["caption"] = fix_text(i["value"])

    return post
        

def main():

    try:
        with open("saved_posts.json", "r", encoding='utf-8' ) as file:
            data = json.load(file)


    except FileNotFoundError:
        print ("error: file not found ")

    for item in data[:3]:
        print(parse_post(item))

if __name__ == "__main__":
    main()
