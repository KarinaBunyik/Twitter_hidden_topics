import collections
import io

def fileToList(filename):
        word_list = []
        ifile = io.open(filename, 'r', encoding = 'utf-8')
        for word in ifile:
            word_list.append(word.replace('\n',''))
        ifile.close()
        return word_list

if __name__ == "__main__":

        path_to_files = '/Users/karinabunyik/Desktop/ordlista/'

	file_path_skola = path_to_files + 'skolan.txt'
	file_path_sjukvard = path_to_files + 'sjukvard.txt'
	file_path_jobbochskatt = path_to_files + 'jobbochskatt.txt'
	file_path_klimat = path_to_files + 'klimat.txt'
	file_path_brottochstraff = path_to_files + 'brottochstraff.txt'
	file_path_flyktingar = path_to_files + 'flyktingar.txt'
	file_path_forsvar = path_to_files + 'forsvar.txt'
	file_path_oppnagranser = path_to_files + 'oppnagranser.txt'
	file_path_feminism = path_to_files + 'feminism.txt'
	file_path_eu = path_to_files + 'eu.txt'
	file_path_antirasism = path_to_files + 'antirasism.txt'
	file_path_vinsterivalfarden = path_to_files + 'vinsterivalfarden.txt'

	list_skola = fileToList(file_path_skola)
	list_sjukvard = fileToList(file_path_sjukvard)
	list_jobbochskatt = fileToList(file_path_jobbochskatt)
	list_klimat = fileToList(file_path_klimat)
	list_brottochstraff = fileToList(file_path_brottochstraff)
	list_flyktingar = fileToList(file_path_flyktingar)
	list_forsvar = fileToList(file_path_forsvar)
	list_oppnagranser = fileToList(file_path_oppnagranser)
	list_feminism = fileToList(file_path_feminism)
	list_eu = fileToList(file_path_eu)
	list_antirasism = fileToList(file_path_antirasism)
	list_vinsterivalfarden = fileToList(file_path_vinsterivalfarden)

	print 'skola duplikater: ',  [x for x,y in collections.Counter(list_skola).items() if y>1], '\n'
	print 'sjukvard duplikater: ',  [x for x,y in collections.Counter(list_sjukvard).items() if y>1], '\n'
	print 'jobbochskatt duplikater: ',  [x for x,y in collections.Counter(list_jobbochskatt).items() if y>1], '\n'
	print 'klimat duplikater: ',  [x for x,y in collections.Counter(list_klimat).items() if y>1], '\n'
	print 'brottochstraff duplikater: ',  [x for x,y in collections.Counter(list_brottochstraff).items() if y>1], '\n'
	print 'flyktingar duplikater: ',  [x for x,y in collections.Counter(list_flyktingar).items() if y>1], '\n'
	print 'forsvar duplikater: ',  [x for x,y in collections.Counter(list_forsvar).items() if y>1], '\n'
	print 'oppnagranser duplikater: ',  [x for x,y in collections.Counter(list_oppnagranser).items() if y>1], '\n'
	print 'feminism duplikater: ',  [x for x,y in collections.Counter(list_feminism).items() if y>1], '\n'
	print 'eu duplikater: ',  [x for x,y in collections.Counter(list_eu).items() if y>1], '\n'
	print 'antirasism duplikater: ',  [x for x,y in collections.Counter(list_antirasism).items() if y>1], '\n'
	print 'vinsterivalfarden duplikater: ',  [x for x,y in collections.Counter(list_vinsterivalfarden).items() if y>1], '\n'