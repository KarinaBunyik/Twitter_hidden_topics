from lxml import etree

attributes = ("hashtags")
context = etree.iterparse("twitter-pldebatt.xml", tag="text", events=("start", "end"))

d = []

context = iter(context)
for event, element in context:
    if element.tag == "text":   
    #for name, value in element.items():
        d.append(element.attrib)
        #if child.attrib.get("name") in attributes:
            #print next(c for c in child).text
    #element.clear()

print hashtags
