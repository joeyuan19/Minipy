Minipy
========

#### Description

Python script to minify JS, CSS, and other code files eventually

---

#### Usage

Minification can be done by running the python script in the following fashion:

	python minifyJS.py fileOneToMinify.js fileTwoToMinify.js folderOneToMinify

The program will out put a file: `original_file_name.min.js`  
Minified files will be outputted to the same directory they are originally found.

---

#### To do

- [ ] Add Examples  
- [-] Implement JS
	- [+] Remove Comments
	- [+] Remove Empty Lines
	- [+] Reduce Code on one Line
	- [-] Ensure Semicolons
		- [ ] Switch to regex switch to avoid adding to if statements and for loops
	- [ ] Refactor Variable Names
		- [ ] Issue of Compatibility With Associated HTML Files
- [ ] Implement CSS
	- [ ] Remove Comments
	- [ ] Reduce Code on one Line
- [ ] Implement HTML
	- [ ] Reduce Coce to one Line
- [ ] Implement Project Wide Minification

---

#### Contributions

Contact me if you would like to contribute to this project or have suggestions.



