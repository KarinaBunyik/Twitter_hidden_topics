#import formattingForMallet
import subprocess
from thtpaths import script_path, internal_path, output_path

def averageCommonTopics():
	pass
'''
data_dir = 'malletTwitterLDAOctober_all'
model_name = 'june_no_username.mallet'
inference_name = 'inferencer_june_no_username.mallet'
inference_out_name = 'inference_june_no_username.out'
evaluator_name = 'eval_june_no_username.mallet'
probs_name = 'probs_june_no_username.out'
doc_probs_name = 'doc_probs_june_no_username.out'
topic_no = '10'
topic_word_no = '10'
iteration_no = '300'
topic_key_name = 'topic-keys-LDA-june-nouser.txt'
doc_topic_name = 'doc-topics-LDA-june-nouser.txt'
'''
data_dir = 'malletTwitterLDAOctober_test'
model_name = 'october_test.mallet'
inference_name = 'inferencer_october_test.mallet'
inference_out_name = 'inference_october_test.out'
evaluator_name = 'eval_october_test.mallet'
probs_name = 'probs_october_test.out'
doc_probs_name = 'doc_probs_october_test.out'
topic_no = '50'
topic_word_no = '10'
iteration_no = '1000'
topic_key_name = 'topic-keys-LDA-october-test.txt'
doc_topic_name = 'doc-topics-LDA-october-test.txt'


swedish_stoplist_wpath = internal_path+'swedish_stoplist.txt'
script_name_wpath = script_path+'run_twitter_mallet.sh'
data_dir_wpath = internal_path+data_dir
model_name_wpath = internal_path+model_name
inference_name_wpath = internal_path+inference_name
inference_out_name_wpath = output_path+inference_out_name
evaluator_name_wpath = internal_path+evaluator_name
probs_name_wpath = output_path+probs_name
doc_probs_name_wpath = output_path+doc_probs_name
topic_key_name_wpath = output_path+topic_key_name
doc_topic_name_wpath = output_path+doc_topic_name

def commandString():
	command_string=(script_name_wpath+' '+
    			data_dir_wpath+' '+
				model_name_wpath+' '+
				swedish_stoplist_wpath+' '+
				topic_key_name_wpath+' '+
				doc_topic_name_wpath+' '+
				topic_no+' '+
				topic_word_no+' '+
				iteration_no+' '+
				inference_name_wpath+' '+
				inference_out_name_wpath+' '+
				evaluator_name_wpath+' '+
				probs_name_wpath+' '+
				doc_probs_name_wpath)
	return command_string

'''
command_string=(script_name_wpath+' '+
    			data_dir_wpath+' '+
				model_name_wpath+' '+
				swedish_stoplist_wpath+' '+
				topic_key_name_wpath+' '+
				doc_topic_name_wpath+' '+
				topic_no+' '+
				topic_word_no+' '+
				iteration_no+' '+
				inference_name_wpath+' '+
				inference_out_name_wpath+' '+
				evaluator_name_wpath+' '+
				probs_name_wpath+' '+
				doc_probs_name_wpath)
'''
#avg_iteration_no = 2
#for i in range(avg_iteration_no):
command_string = commandString()
proc = subprocess.Popen([command_string], shell=True, stdout=subprocess.PIPE)
#averageCommonTopics(topic_key_name_wpath+'avg')

