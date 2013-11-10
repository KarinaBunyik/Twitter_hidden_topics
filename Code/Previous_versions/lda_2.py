
#from pymongo import ASCENDING, DESCENDING, Connection
import io
from gensim import corpora, models, similarities
from thtpaths import output_path, internal_data_path, data_path
import thtdb


def stop_list(englishlist_filename, swedishlist_filename):
    stopwords = []
    with io.open(internal_data_path+englishlist_filename, 'r', encoding='utf-8') as englishlist_file:
        for word in englishlist_file:
            stopwords.append(word.strip('\n'))
    with io.open(internal_data_path+swedishlist_filename, 'r', encoding='utf-8') as swedishlist_file:
        for word in swedishlist_file:
            stopwords.append(word.rstrip('\n'))
    return stopwords

def load_docs_to_file(filename):
    output_file = io.open(output_path + filename, 'wb')

    print "documents loading to file..."
    for user in db.collection.find():
        if "text" in user:
            if type(user["text"]) is list:
                if "sentence" in user["text"][0]:
                    if "w" in user["text"][0]["sentence"]:
                        for word in user["text"][0]["sentence"]["w"]:
                            if type(word) is dict:
                                temp = word["val"]+' '
                                output_file.write(temp.encode('utf8'))
                                #output_file.write('%s ' % word["val"])
                        end_line = '\n'#u"\r"
                        #print type( word["val"])
                        output_file.write(end_line.encode('utf8'))
            else:
                if "sentence" in user["text"]:
                    if "w" in user["text"]["sentence"]:
                        pass
            #       for word in user["text"][0]["sentence"]["w"]:
            #           words_list.append(word["val"]) #.encode('UTF-8'))
        #           output_file.write('%s ' % word["val"])
            #words_list = []
    output_file.close()

def lda(filename):

    print "loading documents to memory..."
    documents = []
    #with io.open(output_path + "out_data1.txt", 'r', encoding='utf-8') as input_file:
    with io.open(output_path + filename, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            documents.append(line)

    print "tokenization..."
    # remove common words and tokenize
    #stoplist = set('for a of the and to in och eller en med i inte jag att det den'.split())
    stopset = set(stop_list("english_stoplist.txt", "swedish_stoplist.txt"))
    texts = [[word for word in document.lower().split() if word not in stopset] for document in documents]

    print "removing unique words..."
    # remove words that appear only once
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once] for text in texts]

    print "creating dictionary..."
    dictionary = corpora.Dictionary(texts)
    dictionary.save(data_path+'data.dict')
    print dictionary

    new_doc = "Jag ska jag"
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    print new_vec

    output_file = io.open('token2id.out', 'wb')
    for key in dictionary.token2id:
        #s = key + ": " + val
        output_file.write(key)
        output_file.write(': ')
        output_file.write(str(dictionary.token2id[key]))
        output_file.write('\n')


    #print "dumping texts to file..."
    #output_file2 = io.open(output_path + "out_data2.txt", 'w', encoding='utf-8')
    #output_file2 = io.open(filename+'.out', 'wb')
    #for text in texts:
    #    for word in text:
    #        if word not in tokens_once:
    #            temp = word+' '
    #            output_file2.write(temp.encode('utf8'))
    #    end_line = '\n'
    #    output_file2.write(end_line.encode('utf8'))

    input_file.close()


if __name__ == "__main__":
    db = thtdb.ThtConnection(collectionName='test_1')

    #output_filename = "out_data4.txt"

    #load_docs_to_file("out_data5.txt")

    #load_docs_to_file("out_data3.txt")
    lda("out_data5.txt")
