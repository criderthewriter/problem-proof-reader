import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter"],
    "include_files": [
        "data",
        "files_to_proofread",
        "readme.md",
        "targets.py",
        "word_reader_1_0_0.py",
        ]
    }

base = None

setup(  name = "ProblemProofReader",
        version = "1.0.0",
        description = "A command line python application that proofreads "\
            ".docx and .txt files for problematic target words and phrases, "\
            "including user-defined targets.",
        options = {"build_exe": build_exe_options},
        executables = [
            Executable("input_script.py", base=base),
            ])
