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
            "caption": None , 
            "hashtags": [], 
            "author" : None, 
            "saved_at": None }
    
    for i in item["label_values"]:
        if "label" in i:
            
            if i["label"] == "URL":
                post["url"] = i["value"]
            elif  i["label"] == "Subtitrare":
                post["caption"] = fix_text(i["value"])
        
        elif i["title"] == "Hashtaguri":
            for h in i["dict"]:
                post["hashtags"].append(h["dict"][0]["value"])
        
        elif i["title"] == "Proprietar":
            if i["dict"] != [] :
               for a in i["dict"]:
                   for tag in a["dict"]:
                        if tag["label"] == "Nume de utilizator":
                            post["author"] =tag["value"]

    post["saved_at"] = datetime.fromtimestamp(item["timestamp"])

    return post
        

def main():


    try:
        with open("data/saved_posts.json", "r", encoding='utf-8' ) as file:
            data = json.load(file)


    except FileNotFoundError:
        print ("error: file not found ")

    emptyCaption = 0
    noAuthor =  0
    noHashtag= 0 

    for item in data:
    
       # print(parse_post(item))
        d = parse_post(item)
        if d["caption"] == None :
                    emptyCaption +=1
        if d["author"] == None:
                    noAuthor +=1
        if d["hashtags"] == []:
                    noHashtag +=1
    
    print (" emptyCaption=" ,  emptyCaption, "| noAuthor = ", noAuthor, " | noHashtag=", noHashtag)

if __name__ == "__main__":
    
    main()
