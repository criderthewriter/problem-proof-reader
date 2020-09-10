# problem-proof-reader

Hello! This is the ProblemProofReader, my first coding project, aimed at 
serving writers--novelists, columnists, bloggers, but also anyone writing a cover 
letter, a job application, an acceptance speech.  The Reader proofreads .docx and 
.txt files for problematic target words and phrases, including user-defined targets.
	
Part of the project's intent was to make the Reader accessible to writers
who have no coding experience, and the Reader's pages have (hopefully) easy-to-follow 
instructions that walk the user through the proofreading process.

How to install:
	(Installer) Just run the installer, ProblemProofReader-1.0.0-win32.msi (or 
whatever version you have), then run input_script.exe. I've packaged all relevant 
files into the installer and used cx freeze to include valid python files, so the 
user shouldn't need to have python installed.
	(Without Installer) Download the relevant files/folders and put them in the
same directory. Ideally you have python installed, in which case you can run 
input_script.py to operate the program.

Upon activation, the Reader will create a file called config.json and save user 
settings to it, including predefined targets. For internal usage, it will also 
save a compressed copy of the last document selected for proofreading, so you 
may notice its file size jumping.  You can safely delete config.json to clear 
all of the Reader's saved data, as that is the only file the Reader has the power 
to overwrite.  The Reader's menus also have an option for clearing config.json's 
contents. 

For the files you want proofread, you can either provide the Reader with their full 
file path, or you can put a copy of them in the folder files_to_proofread.
	
Note that data files "before you begin.txt" and "credits.txt" are loaded by pages 
within the Reader, so they should not be deleted or moved from the directory where 
input_script.py resides. This readme focuses on installation instructions, but 
"before you begin.txt" includes guidance and recommendations for using the Reader 
while writing and editing, essentially an FAQ.  "credits.txt" contains articles and 
works cited in constructing the Reader's dictionaries of proofreading targets.
