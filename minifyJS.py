import sys
import re
import os

def remove_comments(content):
	buf = ''
	L = len(content)
	line_comment = False
	multi_line_comment = False
	i = 0
	while i < L:
		if content[i] == '/':
			if i+1 < L and content[i+1] == '/':
				line_comment = True
				i += 1
			if i+1 < L and content[i+1] == '*':
				multi_line_comment = True
				i += 1
		if not line_comment and not multi_line_comment:
			buf += content[i]
		if multi_line_comment and content[i] == '*':
			if i+1 < L and content[i+1] == '/':
				multi_line_comment = False
				i += 1
		if line_comment and content[i] == '\n':
			line_comment = False
		i += 1
	return buf

def assert_semicolons(content):
	content = re.sub(r'([\n]{1})$','',content,flags=re.MULTILINE)
	content = re.sub(r'([^;|,|{])$','\g<1>;',content,flags=re.MULTILINE)
	return content

def remove_whitespace(content):
	content = content.replace('\n','').replace('\t','') # remove tabs and newlines
	content = re.sub(r'\s{2,}','',content) # remove instances of more than two spaces
	i = 0
	L = len(content)
	space_found = False
	in_string = False
	buf = ''
	while i < L:
		space_found = False
		if content[i] == u'\"' or content[i] == u'\'':
			in_string = not in_string
		if not in_string and content[i] == ' ':
			space_found = True
			if len(buf)-len('var') > -1 and buf[-len('var'):] == 'var':
				space_found = False
				"""
				if len(buf)-len('var')-1 > 0:
					if buf[-len('var')-1] != ';' and buf[-len('var')-1] != '{' and buf[-len('var')-1] != '}':
						space_found = True
						"""
			elif len(buf)-len('function') > -1 and buf[-len('function'):] == 'function':
				space_found = False
				"""
				if len(buf)-len('function')-1 > 0:
					if buf[-len('function')-1] != ';' and buf[-len('function')-1] != '{' and buf[-len('function')-1] != '}':
						space_found = True
						"""
			elif len(buf)-len('return') > -1 and buf[-len('return'):] == 'return':
				space_found = False
				if len(buf)-len('return')-1 > 0:
					if buf[-len('return')-1] != ';' and buf[-len('return')-1] != '{' and buf[-len('return')-1] != '}':
						space_found = True
		if not space_found:
			buf += content[i]
		i += 1
	return buf

def minify_js_file(content,v=False):
	if v: print "CONTENT AT START:\n",content
	content = remove_comments(content)
	content = assert_semicolons(content)
	content = remove_whitespace(content)
	if v: print "CONTENT AT END:\n",content
	return content
	
def process_file(file_name,dir_name=""):
	if ".js" not in file_name or ".min.js" in file_name:
		return
	with open(os.path.join(dir_name,file_name),'r') as f:
		original_size = os.stat(f.name).st_size
		content = ''.join(i.strip()+'\n' for i in f)
	minified_file_name = re.sub('.js$','.min.js',file_name)
	content = minify_js_file(content,debug)
	with open(os.path.join(dir_name,minified_file_name),'w') as f:
		f.write(content)
		f.flush()
		minified_size = os.stat(f.name).st_size
		print os.path.join(dir_name,file_name)," -> ",os.path.join(dir_name,minified_file_name),
		print "\n\tOriginal Size:",original_size,
		print "\n\tMinified Size:",minified_size,
		print "\n\tReduced size by: ",str(100*(1.0-(minified_size/float(original_size)))) + "%"

def process_dir(dir_name):
	for file_name in os.listdir(dir_name):
		if os.path.isfile(file_name):
			process_file(file_name,dir_name)

if __name__ == "__main__":
	debug = False
	if len(sys.argv) <= 1:
		print "No argument provided.  Usage: python minifyJS.py firstFileToMinify.js secondFileToMinify.js ...";
		sys.exit(1)
	for file_name in sys.argv:
		if file_name != __file__:
			if os.path.isfile(file_name):
				process_file(file_name)
			if os.path.isdir(file_name):
				process_dir(file_name)

