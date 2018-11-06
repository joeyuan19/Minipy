import sys
import re
import math
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Minipy - JS and code minification
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Project Outline
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# To Do List
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# [ ] Project wide refactoring
#	[ ] HTML, JS, CSS refactor together
#	[ ] Multiple Java class files together
# [ ] Javascript
# 	[ ] Assert JS
#		[ ] Assert semicolon endlines
# 	[ ] Minify JS
#		[ ] Remove non-essential whitespace
#		[ ] Place all code on a single line
#		[ ] Remove Comments
# [ ] CSS
#	[ ] Remove Comments
# [ ] Java
#	[ ] Remove Comments
# [ ] Python
#	[ ] Remove Comments
# [ ] HTML
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #




# remove comments from a JS file
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

# Assert that semicolons exist in the appropriate places
def assert_JS(content):
	# Assert Semicolons
	content = re.sub(r'([\n]{1})$','',content,flags=re.MULTILINE)
	content = re.sub(r'([^;|,|{])$','\g<1>;',content,flags=re.MULTILINE)
	# Assert 'var' before variables
	return content

# Remove the white space from a JS file
def remove_whitespace(content):
	content = content.replace('\n','').replace('\t','') # remove tabs and newlines
	content = re.sub(r'\s{2,}','',content) # remove instances of more than two spaces
	i = 0
	L = len(content)
	space_found = False
	in_string = False
	buf = ''
	js_kws = ('new','var','function','return')
	js_flags = (';','{','}','(',')','[',']','=')
	while i < L:
		space_found = False
		if content[i] == u'\"' or content[i] == u'\'':
			in_string = not in_string
		if not in_string and content[i] == ' ':
			space_found = True
			for js_kw in js_kws:
				if len(buf)-len(js_kw) > -1 and buf[-len(js_kw):] == js_kw:
					space_found = False
					if len(buf)-len(js_kw)-1 > 0:
						if buf[-len(js_kw)-1] not in js_flags:
							space_found = True
		if not space_found:
			buf += content[i]
		i += 1
	return buf

# Refactor content to simplest names
def refactor_js(content):
	buf = ""
	var_buf = ""
	L = len(content)
	i = 0
	js_kwds = ['var','function']
	while i < L:
		
		i += 1
	variables = re.findall(r'var (\w+)[ ,=;]',content)
	functions = re.findall(r'function (\w+)[ \(]',content)
	temp = []
	for var in variables:
		if ',' in var:
			for i in var.split(','):
				if i not in temp:
					temp.append(i)
		else:
			if var not in temp:
				temp.append(var)
	variables = [i for i in temp]
	itr = 0
	for i in range(len(variables)):
		while generate_var_name(itr) in variables:
			itr += 1
		print variables[i], generate_var_name(itr)
		content = re.sub(r'(var )' + variables[i] + '([=;,])','\g<1>' + generate_var_name(itr) + '\g<2>',content)
		content = re.sub(r'(,)' + variables[i] + '([,;])','\g<1>' + generate_var_name(itr) + '\g<2>',content)
		content = re.sub(r'([\(,])' + functions[i].strip() + '([,\)])','\g<1>' + generate_var_name(itr) + '\g<2>',content)
		itr += 1
	for i in range(len(functions)):
		while generate_var_name(itr) in functions:
			itr += 1
		content = re.sub(r'(function )' + functions[i] + '([\(])','\g<1>' + generate_var_name[itr] + 'g<2>',content)
		content = re.sub(r'([\(,])' + functions[i].strip() + '([,\)])','\g<1>'+ generate_var_name[itr] + '\g<2>',content)
	return content

def log26(n):
	if n > 0:
		return math.log(n)/math.log(26)
	else:
		return False

def generate_var_name(n):
	if n >= 0:
		alpha_offset = 97
		x = int(log26(n))
		var_name = ""
		while x > 0:
			var_name += chr((alpha_offset-1)+n/(26**x))
			n = n % (26**x)
			x = int(log26(n))
		var_name += chr(alpha_offset+n)
		return var_name
	else:
		return None

# Perform minification of a JS file
def minify_js_file(content):
	if flags['debug']: print "CONTENT AFTER COMMENT REMOVAL:\n",content
	content = assert_JS(content)
	if flags['verbose'] or flags['debug']: print "CONTENT AT START:\n",content,'\n'
	content = remove_comments(content)
	if flags['debug']: print "CONTENT AFTER SEMICOLON ASSERTION:\n",content
	content = remove_whitespace(content)
	if flags['debug']: print "CONTENT AFTER WHITESPACE REMOVAL:\n",content
	content = refactor_js(content)
	if flags['debug']: print "CONTENT AFTER REFACTOR:\n",content,'\n'
	if flags['verbose'] or flags['debug']: print "CONTENT AT END:\n",content
	return content

# Method to process a single file
def process_file(filename,dir_name=""):
	if ".js" not in filename or ".min.js" in filename:
		return
	with open(os.path.join(dir_name,filename),'r') as f:
		original_size = os.stat(f.name).st_size
		content = ''.join(i.strip()+'\n' for i in f)
	minified_filename = re.sub('.js$','.min.js',filename)
	content = minify_js_file(content)
	with open(os.path.join(dir_name,minified_filename),'w') as f:
		f.write(content)
		f.flush()
		minified_size = os.stat(f.name).st_size
		print os.path.join(dir_name,filename)," -> ",os.path.join(dir_name,minified_filename),
		print "\n\tOriginal Size:",original_size,
		print "\n\tMinified Size:",minified_size,
		print "\n\tReduced size by: ",str(100*(1.0-(minified_size/float(original_size)))) + "%"

# Method to handle a directory of files
def process_dir(dir_name):
	for filename in os.listdir(dir_name):
		if os.path.isfile(filename):
			process_file(filename,dir_name)

# Method to handle flags
def mark_flag(flag):
		if flag == 'verbose' or flag == 'v':
			flags['verbose'] = True
		elif flag == 'help' or flag == 'h':
			flags['help'] = True
		elif flag == 'project' or flag == 'p':
			flags['project'] = True
		elif flag == 'debug' or flag == 'd':
			flags['debug'] = True

def print_help():
	print 'Welcome to minipy!\nThis is a script to minify code files, removing unnecessary characters and reducing the file size\n'
	print
	print "\t",usage_msg
	print 
	print "\t-h, --help\t\tShow this message"
	print "\t-v, --verbose\t\tShow more information"
	print "\t-d, --debug\t\tShow more information than verbose"
	print "\t-p, -project\t\tFiles listed are part of the same project and\n\t\t\t\tshould minify across entrie project"

usage_msg =	"Usage: python mini.py --flag -flag(s) firstFileToMinify.js secondFileToMinify.js ..."; 
flags = {
	'verbose':False,
	'debug':False,
	'project':False,
	'help':False,
}

if __name__ == "__main__":
	filenames = []
	for arg in sys.argv:
		if arg[0] == '-' and arg[1] == '-':
			arg = arg.replace('-','')
			mark_flag(arg)
		if arg[0] == '-':
			arg = arg.replace('-','')
			for i in arg:
				mark_flag(i)
		else:
			filenames.append(arg)
	if flags['help']:
		print_help()
		sys.exit(1)
	if len(filenames) <= 1:
		print "No argument provided.",usage_msg 
		print "For more information run: python mini.py --help"
		sys.exit(1)
	for filename in filenames:
		if filename != __file__:
			if os.path.isfile(filename):
				process_file(filename)
			if os.path.isdir(filename):
				process_dir(filename)

