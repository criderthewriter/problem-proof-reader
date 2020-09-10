import targets
import word_reader_1_0_0 as word
from word_reader_1_0_0 import print_wrapped, update_page

word.load_settings()

# This variable notes a user-defined target which already exists in a
# target list.
targ_repeat = ''
# These flags note whether a temporary change has been made so that it
# will not be overwritten with repeated iterations of a while loop. If
# that change is approved, it is saved to a more persistent variable.
disabled_targs_temp = ''
temp_settings = ''
results_display_temp = ''
group_common_targs_temp = ''
# This flag notes whether the user has successfully loaded a saved
# filename and agreed to proofread it again.
use_prev_file = False
# This flag notes whether the user has agreed to have common search
# matches sorted apart from uncommon matches.
displaying_common = False

update_page('pg_intro')
print_wrapped(
    2, "ProblemProofReader",
    1, """\
        Welcome to the ProblemProofReader, by Andrew Ryan Crider! I'm here to
        help you scan text files for problematic words and phrases. I can pick
        out bits of writing that are clunky, offensive, or otherwise non-ideal,
        and I can suggest replacements, too!""")
update_page('pg_main_menu')

while True:

    while word.current_page == 'pg_main_menu':
        print_wrapped(2, "Main Menu")
        if word.pr_ready_doc:
            done_notice = '(done)'
            not_ready_notice = '(ready)'
        else:
            done_notice = ''
            not_ready_notice = '(not ready)'
        print_wrapped(
            1, ["""\
                How can I help you? Type in the number of the menu option
                you'd like, then press Enter. You can input 'x' at any
                time to go back one screen.""",
            ""],
            6, ["1 - Before you begin...",
                "2 - View or edit the terms I target",
                "",
                f"3 - Select a file to proofread {done_notice}",
                f"4 - Proofread the selected file {not_ready_notice}",
                "",
                "5 - Settings and extras",
                "6 - Quit program."""])
        menu = input().lower()
        if menu == '1':
            update_page('pg_before_begin')
        elif menu == '2':
            update_page('pg_view_edit')
        elif menu == '3':
            update_page('pg_file_select')
        elif menu == '4':
            update_page('pg_proofread_file')
        elif menu == '5':
            update_page('pg_settings_extras')
        elif menu == '6':
            update_page('pg_quit_prompt')
        elif menu == '7':
            update_page('pg_test_function')
        elif menu == 'x':
            update_page('pg_quit_noprompt')
        else:
            print_wrapped(
                1, "I don't understand. Can you please try again, "\
                    " and make sure you only input a number?")

    while word.current_page == 'pg_before_begin':
        print_wrapped(
            2, "Before You Begin...",
            10, "")
        with open('data/before you begin.txt', encoding='utf-8') as f:
            text = f.read()
        text_pages = text.split('\n***\n')
        total_pages = 0
        text_paras_by_page = []
        for page in text_pages:
            total_pages += 1
            split_page = page.split('\n')
            if split_page:
                text_paras_by_page.append(split_page)
        count = 0
        for page in text_paras_by_page:
            count += 1
            # Building the paragraph lists produces several blank
            # paragraphs; this block filters them out as it prints them.
            for para in page:
                if 1 < len(para) < 36:
                    print_wrapped(10, f"{para}")
                elif 1 < len(para):
                    print_wrapped(7, f"{para}")
            if count < total_pages:
                print_wrapped(
                    1, "Press Enter to continue, or input 'x' to go back.")
                menu = input().lower()
                if menu == 'x':
                    break
            else:
                print_wrapped(
                    1, "If you’ve read and understood my statements "\
                        "here, we are ready to begin proofreading your "\
                        "work. Press Enter to return to menu.")
                menu = input().lower()
                if menu == 'x':
                    break
        update_page('pg_main_menu')
        break

    while word.current_page == 'pg_view_edit':
        print_wrapped(
            2, "View and Edit Targets",
            1, ["Here's what you can do with my target words and phrases.",
            ""])
        # This is the first of many menus that will expand based on the
        # number of target categories saved.
        count = 0
        for cat in word.all_cats_list:
            count += 1
            print_wrapped(6, f"{count} - View '{cat}'")
        total_cats = count
        enabled_cats = 0
        for setting in word.toggle_settings.values():
            if setting == 'Yes':
                enabled_cats += 1
        print_wrapped(
            6, ["",
            f"{total_cats +1} - Add a new user-defined target",
            f"{total_cats +2} - Disable a search target "\
                f"({len(word.disabled_targs)} disabled)",
            f"{total_cats +3} - Disable an entire target category "\
                f"({enabled_cats} of {total_cats} enabled)",
            "",
            f"{total_cats +4} - View all available targets",
            f"{total_cats +5} - View only the enabled targets",
            "",
            f"{total_cats +6} - Go back"])
        menu = input().lower()
        # The program attempts to change the user's input into an
        # integer so it can match values in a range.
        menu = word.try_str_to_int(menu)
        if menu in range(1, total_cats +1):
            heading_1 = word.all_cats_list[menu -1]
            if menu == total_cats -1 or menu == total_cats:
                display_content = word.user_defined[heading_1]
            else:
                display_content = targets.predefined[heading_1]
            print_wrapped(2, f"{heading_1}")
            if not display_content:
                print_wrapped(12, "(None listed)")
            for targ, desc in display_content.items():
                print_wrapped(
                    1, f"{word.convert_tuple_to_str(targ)}:",
                    3, f"{desc}")
            print_wrapped(1, "Hit Enter when you're ready to go back.")
            input()
        elif menu == total_cats +1:
            update_page('pg_define_target')
        elif menu == total_cats +2:
            update_page('pg_disable_target')
        elif menu == total_cats +3:
            update_page('pg_toggle_category')
        elif menu == total_cats +4:
            print_wrapped(2, "All Available Targets")
            all_targs = word.TargetList.build_dict_of_all_targs()
            for category, targs in all_targs.items():
                print_wrapped(1, f"{category}")
                if not targs:
                    print_wrapped(12, "(None listed)")
                for targ, desc in targs.items():
                    print_wrapped(
                        12, f"{word.convert_tuple_to_str(targ)}:",
                        4, f"{desc}")
            print_wrapped(1, "Hit Enter when you're ready to go back.")
            input()
        elif menu == total_cats +5:
            print_wrapped(
                2, "Enabled Targets",
                10, "")
            enabled_targets = word.TargetList.build_dict_of_enabled_targs()
            if not enabled_targets:
                print_wrapped(
                    3, "(You disabled all the search categories,  so I have "\
                    "nothing to search for.)")
            for category, targs in enabled_targets.items():
                print_wrapped(1, f"{category}")
                if not targs:
                    print_wrapped(12, "(None listed)")
                for targ, desc in targs.items():
                    print_wrapped(
                        12, f"{word.convert_tuple_to_str(targ)}:",
                        4, f"{desc}")
            print_wrapped(1, "Hit Enter when you're ready to go back.")
            input()
        elif menu == total_cats +6 or menu == 'x':
            update_page('pg_main_menu')
        else:
            print_wrapped(1, "I don't understand. Try again, please?")

    while word.current_page == 'pg_define_target':
        print_wrapped(
            2, "Adding a User-Defined Target",
            1, "A few ground rules:",
            7, ["Please add only one new word or phrase at a time.",
                "But feel free to make your phrase as long as you want!",
            """\
                My search function is case-insensitive. It doesn't matter
                whether you input lower- or uppercase text.""",
            """\
                Apostrophes INSIDE contracted words (like \"can't\") are fine.
                But any leading or trailing punctuation (like the
                hyphens or apostrophe in \"will-o'-the-wisp\") will be ignored
                during my search.""",
            "No repeat entries, please! That'll just make things "\
                "confusing.",
            """\
                If you give me a single word like, say, \"cat\", my search
                will pick up both \"cat\" and \"cats\", because \"cats\" is
                just the word you gave me with an \"s\" at the end; you don't
                also have to tell me to search for \"cats\". But if your word
                has a more complex plural form (like \"party\" and \"parties\",
                or \"woman\" and \"women\"), you'll have to input each word
                if you want me to find all of them. I'm not perfect, but I'll
                do the best I can!"""],
            1, "What word or phrase would you like me to search for?")
        new_wp = input().lower()
        # When a new user-defined target is given, it is checked against
        # all existing targets to ensure it is unique.
        all_targs = word.TargetList.build_dict_of_all_targs()
        for cat, targs in all_targs.items():
            for targ in targs.keys():
                if isinstance(targ,tuple):
                    for item in targ:
                        if new_wp == item:
                            targ_repeat = cat
                else:
                    if new_wp == targ:
                        targ_repeat = cat
        if targ_repeat:
            print_wrapped(
                1, "The text you gave me is already "\
                    "in one of my target lists. Specifically, it's in"\
                    f" \"{targ_repeat}\". Can you try something else?")
            targ_repeat = ''
            continue
        elif new_wp == 'x':
            update_page('pg_view_edit')
            break
        elif len(new_wp) == 1:
            print_wrapped(1, "Input more than a single letter, please!")
            continue
        elif new_wp == '':
            print_wrapped(
                1, "You didn't put in anything. Do you want to "\
                    "cancel and go back? (y/n)")
            menu = input().lower()
            if menu == 'n':
                print_wrapped(
                    1, "Okay. What word or phrase would you "\
                        "like me to search for?")
                new_wp = input().lower()
                if new_wp == '':
                    print_wrapped(
                        1, "Now you're just teasing me. Let's start over.")
                    continue
            elif menu == 'y':
                print_wrapped(1, "Okay. Back it is.")
                update_page('pg_view_edit')
                break
            elif menu == 'x':
                continue
            else:
                print_wrapped(
                    1, "I don't understand. Sorry! Let's start over.")
                continue
        # This block strips the new word's leading and trailing
        # punctuation, then makes sure at least two characters are left.
        elif len(new_wp.lower().strip(word.punctuation_plus)) <= 2:
            print_wrapped(
                1, "That's too short! I'm a proofreader "\
                    "for common mistakes, not a Find tool. Will you input "\
                    "a longer word, please?")
            continue
        else:
            new_wp = word.try_str_to_int(new_wp)
            if isinstance(new_wp,int):
                print_wrapped(
                    1, "That's a number. You want me to speak up every "\
                        f"time I find a {new_wp}?")
                menu = input().lower()
                if menu == 'y':
                    print_wrapped(1, "Okay. Sure.")
                elif menu == 'n':
                    print_wrapped(
                        1, "Alright. Let's start over and try this again.")
                    continue
                elif menu == 'x':
                    continue
                else:
                    print_wrapped(
                        1, "I don't understand. Sorry, but can we start over?")
                    continue
        print_wrapped(
            1, "And what description would you like me to display if I find "\
                "the word or phrase you gave me?")
        new_desc = input()
        if new_desc == 'x' or new_desc =='X':
            continue
        elif new_desc == '':
            print_wrapped(
                1, "You didn't input anything. I can just put in a generic "\
                    "message if you want. What would you prefer?",
                6, ["1 - Save description as \"A user asked me to speak up "\
                    "when I find this!\"",
                "2 - Give a description again",
                "3 - Cancel and go back"])
            menu = input().lower()
            if menu == '1':
                print_wrapped(1, "Okay.")
                new_desc = "A user asked me to speak up when I find "\
                "this!"
            elif menu == '2':
                print_wrapped(
                    1, "Okay. Go ahead and give me your description.")
                new_desc = input()
                if new_desc == '':
                    print_wrapped(
                        1, "Now you're just teasing me. Let's start over.")
                    continue
            elif menu == '3':
                print_wrapped(1, "Back we go.")
                continue
            elif menu == 'x':
                continue
            else:
                print_wrapped(
                    1, "I don't understand. Sorry! Let's start over.")
                continue
        print_wrapped(
            1, "Your input looks like this:",
            12, "Target to find:",
            4, f"{new_wp}",
            12, "Description I'll display when I find it:",
            4, f"{new_desc}",
            1, "Is that okay? (y/n)")
        menu = input().lower()
        if menu == 'y':
            print_wrapped(1, "Excellent. Saving your new target.")
            word.define_new_target(new_wp, new_desc)
            print_wrapped(1, "Now, back to menu.")
            update_page('pg_view_edit')
        elif menu == 'n':
            print_wrapped(
                1, "Oh gosh. Sorry, but we'll need to start over.")
            continue
        elif menu == 'x':
            continue
        else:
            print_wrapped(
                1, "I don't understand. I'm sorry, but we'll need to "\
                    "start over.")
            continue

    while word.current_page == 'pg_disable_target':
        all_targs = word.TargetList.build_dict_of_all_targs()
        print_wrapped(
            2, "Disabling Search Targets",
            1, ["""\
                If you disable a target, I'll remember it exists, but I'll stop
                searching for it when I proofread your documents. Just input
                the category of the targets you want to disable (or re-enable).
                If you want to disable every target in a category, go back to
                "View and Edit Targets" and pick "Disable an entire target
                category" instead.""",
            ""])
        count = 0
        for cat in word.all_cats_list:
            count += 1
            print_wrapped(
                6, f"{count} - Disable targets in '{cat}'")
        total_cats = count
        print_wrapped(
            6, ["",
            f"{total_cats +1} - View all disabled targets "\
                f"({len(word.disabled_targs)} disabled)",
            f"{total_cats +2} - Re-enable all disabled targets",
            "",
            f"{total_cats +3} - Go back"])
        menu = input().lower()
        menu = word.try_str_to_int(menu)
        if menu in range(1, total_cats +1):
            cat = word.all_cats_list[menu -1]
            word.save_settings()
            update_page(f'disable_{cat}')
        elif menu == total_cats +1:
            print_wrapped(2, "All Disabled Targets")
            for cat, targs in all_targs.items():
                # For each category, if no targets from that category
                # are disabled, (None) is displayed instead of the
                # disabled targets.
                disabled_targs_present = False
                print_wrapped(1, f"{cat}")
                for targ, desc in targs.items():
                    if targ in word.disabled_targs:
                        disabled_targs_present = True
                        print_wrapped(
                            12, f"{word.convert_tuple_to_str(targ)}:",
                            4, f"{desc}")
                if not disabled_targs_present:
                    print_wrapped(12, "(None)")
                elif not targs:
                    print_wrapped(12, "(None listed)")
            print_wrapped(1, "Hit Enter when you're ready to go back.")
            input()
        elif menu == total_cats +2:
            print_wrapped(
                1, "Are you sure? This will overwrite any and all "\
                    "targets you've disabled. (y/n)")
            menu = input()
            if menu == 'y':
                word.disabled_targs.clear()
                word.save_settings()
                print_wrapped(1, "All targets re-enabled.")
            elif menu == 'n' or menu == 'x':
                continue
            else:
                print_wrapped(1, "I'm sorry, but I don't understand.")
        elif menu == total_cats +3 or menu == 'x':
            word.save_settings()
            update_page('pg_view_edit')
        else:
            print_wrapped(
                1, "Sorry, I don't understand. Can we try that again, "\
                    "please?")
        # This block brings up an alert when word.disabled_targs has
        # repeat items on it; the repeated items are also displayed. For
        # debugging purposes.
        list_copy_1 = word.disabled_targs[:]
        list_copy_2 = list(set(word.disabled_targs[:]))
        if len(list_copy_1) != len(list_copy_2):
            print_wrapped(
                1,"Error: The disabled targets list has "\
                    f"{len(list_copy_1)} items in it when it should have "\
                    f"{len(list_copy_2)}")
            for item in list_copy_2:
                list_copy_1.remove(item)
            print_wrapped(
                1,"For some reason, the following items appeared as "\
                    "duplicates:")
            for item in list_copy_1:
                print_wrapped(3,item)

    # Instead of being specifically defined like all of the program's
    # other pages, each "Disable (category)" page is constructed
    # identically here, based on how many categories have been defined.
    for cat in word.all_cats_list:
        while word.current_page == f'disable_{cat}':
            if not disabled_targs_temp:
                disabled_targs_temp = word.disabled_targs[:]
            print_wrapped(
                2, f"Disable Targets in {cat}",
                10, "")
            targ_list = []
            count = 0
            if not all_targs[cat]:
                print_wrapped(
                    3, ["(None)",
                    ""],
                    1, "Press Enter to go back.")
                input()
                update_page('pg_disable_target')
                break
            for targ in all_targs[cat].keys():
                count += 1
                targ_list.append(targ)
                if targ in disabled_targs_temp:
                    status = 'X  '
                else:
                    status = '•  '
                print_wrapped(
                    6, f"{status}{count} - {word.convert_tuple_to_str(targ)}")
            total_targs = count
            print_wrapped(
                6, ["",
                f"{total_targs +1} - Re-enable all",
                f"{total_targs +2} - Save and go back",
                f"{total_targs +3} - Go back without saving"])
            menu = input().lower()
            menu = word.try_str_to_int(menu)
            if menu in range(1,total_targs +1):
                if targ_list[menu -1] in disabled_targs_temp:
                    disabled_targs_temp.remove(targ_list[menu -1])
                    print_wrapped(
                        1, f"Re-enabled: "\
                            f"{word.convert_tuple_to_str(targ_list[menu -1])}")
                else:
                    disabled_targs_temp.append(targ_list[menu -1])
                    print_wrapped(
                        1, f"Disabled: "\
                            f"{word.convert_tuple_to_str(targ_list[menu -1])}")
            elif menu == total_targs +1:
                if not disabled_targs_temp:
                    print_wrapped(1, "All targets enabled; none to re-enable.")
                else:
                    for targ in targ_list:
                        if targ in disabled_targs_temp:
                            disabled_targs_temp.remove(targ)
                    print_wrapped(1, "All targets in category re-enabled.")
            elif menu == total_targs +2:
                word.disabled_targs = disabled_targs_temp[:]
                disabled_targs_temp = ''
                word.save_settings()
                print_wrapped(1, "Settings saved.")
                update_page('pg_disable_target')
            elif menu == total_targs +3 or menu == 'x':
                disabled_targs_temp = ''
                update_page('pg_disable_target')
            else:
                print_wrapped(
                    1, "I'm afraid I don't understand. Try again, please?")

    while word.current_page == 'pg_toggle_category':
        if not temp_settings:
            temp_settings = word.toggle_settings.copy()
        print_wrapped(
            2, "Categories To Search For",
            1, ["""\
                Here you can dictate which target words and phrases I'll
                search for. If you input a category's number, I'll toggle
                that category between enabled and disabled.""",
            ""])
        count = 0
        for title, setting in temp_settings.items():
            count += 1
            print_wrapped(
                3, f"{count} - {title}".ljust(40) + f"search: {setting}")
        total_cats = count
        print_wrapped(
            3, ["",
            f"{total_cats +1} - Enable all (default)",
            f"{total_cats +2} - Disable all word categories",
            f"{total_cats +3} - Disable all phrase categories",
            "",
            f"{total_cats +4} - Save settings and go back",
            f"{total_cats +5} - Quit without saving"])
        menu = input().lower()
        menu = word.try_str_to_int(menu)
        if menu == 'x':
            temp_settings = ''
            update_page('pg_view_edit')
            break
        elif menu in range(1, total_cats +1):
            cat = word.all_cats_list[menu -1]
            if temp_settings[cat] == 'Yes':
                temp_settings[cat] = 'No'
            elif temp_settings[cat] == 'No':
                temp_settings[cat] = 'Yes'
        elif menu == total_cats +1:
            for cat in temp_settings.keys():
                temp_settings[cat] = 'Yes'
        elif menu == total_cats +2:
            for cat in temp_settings.keys():
                if cat.lower().endswith('words'):
                    temp_settings[cat] = 'No'
        elif menu == total_cats +3:
            for cat in temp_settings.keys():
                if cat.lower().endswith('phrases'):
                    temp_settings[cat] = 'No'
        elif menu == total_cats +4:
            if not 'Yes' in temp_settings.values():
                print_wrapped(
                    1, """\
                        You've disabled all categories, so I won't have
                        anything to search for. Is that what you want?
                        (y/n)""")
                menu = input().lower()
                if menu == 'y':
                    word.toggle_settings = temp_settings.copy()
                    temp_settings = ''
                    word.save_settings()
                    print_wrapped(1, "Alrighty. Settings saved.")
                    update_page('pg_view_edit')
                elif menu == 'n':
                    print_wrapped(1, "I figured.")
                else:
                    print_wrapped(
                        1, "I don't understand. Can we try again?")
            else:
                word.toggle_settings = temp_settings.copy()
                temp_settings = ''
                word.save_settings()
                print_wrapped(1, "Settings saved.")
                update_page('pg_view_edit')
        elif menu == total_cats +5:
            temp_settings = ''
            update_page('pg_view_edit')
        else:
            print_wrapped(
                1, "I don't understand. Try again, please?")

    # Step 1: finding and verifying the file to proofread.
    while word.current_page == 'pg_file_select':
    # When the following process is complete, the resulting class
    # instance pr_ready_doc will be saved to a json file.
        print_wrapped(
            2, "File Selection",
            1, """\
                First, please give me a filename, including the
                extension. If you put it in the folder \"files_to_proofread\",
                you only need to give me the filename, like this:""",
            3, "My Writing.docx",
            1, "If it's in a different folder, you'll need to give me the "\
                "full file path copied from the address bar, like this:",
            3, "D:\\Users\\Me\\Documents\\My Writing.docx, ",
            1, "As a reminder, I can only read .txt and .docx files.")
        # This block checks whether a previously used filename was
        # loaded from the json file and asks for confirmation before
        # that file is chosen again.
        file_input = ''
        use_prev_file = False
        if word.pr_ready_doc:
            print_wrapped(
                1, "You previously told me about this file:",
                3, f"{word.pr_ready_doc.filename}",
                1, "Do you want me to proofread this file? (y/n)")
            menu = input().lower()
            if menu == 'y':
                use_prev_file = True
                file_input = word.pr_ready_doc.filename
            elif menu == 'n':
                print_wrapped(1, "Okay. Let's pick another one.")
            elif menu == 'x':
                update_page('pg_main_menu')
                break
            else:
                print_wrapped(
                    1, "I'm afraid I don't understand. Let's try that again.")
                continue
        if not file_input:
            print_wrapped(
                1, "What file would you like me to proofread? "\
                    "(input 'x' to go back)")
            file_input = input()
            if file_input == 'x' or file_input == 'X':
                update_page('pg_main_menu')
                break
        # This block checks the provided filename and sees if its
        # contents are valid for proofreading, even if the filename has
        # been confirmed previously.
        proofdoc = word.DocToProofread(file_input)
        proofdoc.read_file()
        if proofdoc.error_status == 'error_1':
            print_wrapped(
                3, "Error: Invalid file type or missing "\
                    "extension. I can't work with the input you gave me.")
        elif proofdoc.error_status == 'error_2':
            print_wrapped(
                3, "Error: I can't find the file you inputted. "\
                    "I'm sorry, but can you try again?")
        elif proofdoc.error_status == 'error_14':
            print_wrapped(
                3, "Error: I didn't find any text content in the "\
                    "file you gave me. I'm sorry, but I can't do anything "\
                    "with this file.")
        # proofdoc is not saved to the json file; to save space and
        # avoid repetition, it is only temporary storage for when the
        # program is running.
        elif proofdoc.all_indexed_paras:
            print_wrapped(1, "Okay, good! I was able to read your file.")
            update_page('pg_range_select')
            if not proofdoc.error_status == 'okay':
                print_wrapped(
                    1, "I read your file successfully, but I still "\
                        f"have an error recorded: {proofdoc.error_status}")
        else:
            print_wrapped(
                1, "I hit a nonstandard error while trying to read "\
                    "your file. Sorry, but I'm not sure what the issue is.")
            update_page('pg_main_menu')

    # Step 2: setting and verifying the range of paragraphs to
    # proofread.
    while word.current_page == 'pg_range_select':
        print_wrapped(
            1, """\
                Now I'd like you to set a range of paragraphs from
                your file that you want me to proofread. You probably
                haven't counted how many paragraphs your work contains, but
                don't worry! You'll be able to preview the range before
                you agree to it.""")
        if not proofdoc:
            print_wrapped(
                1, "But you don't have a file selected for "\
                    "proofreading. How did you get here anyway?")
            update_page('pg_file_select')
            break
        range_input = ''
        num_paras = proofdoc.get_paragraph_count(proofdoc.all_indexed_paras)
        print_wrapped(
            1, "Acceptable input formats:",
            7, ["all".ljust(10) + "(I'll search the entire document)",
            "start-end".ljust(10) + "(...the whole document)",
            "1-5".ljust(10) + "(...paragraphs 1, 2, 3, 4, and 5)",
            "12".ljust(10) + "(...paragraph 12)",
            "8-end".ljust(10) + "(...from paragraph 8 to the end)",
            "start-60".ljust(10) + "(...from the beginning up to "\
                "paragraph 60)"],
            1, f"I count {num_paras} paragraphs in your file.")
        if num_paras == 1:
            print_wrapped(
                1, "I only found one paragraph in the document "\
                    "you gave me. Is a range of '1' acceptable? (y/n)")
            menu = input().lower()
            if menu == 'y':
                range_input = '1'
            elif menu == 'n':
                print_wrapped(
                    1, "Then we'll need to re-select your file. "\
                        "Let's go back and do that.")
                update_page('pg_file_select')
                break
            elif menu == 'x':
                update_page('pg_file_select')
                break
        elif use_prev_file and word.pr_ready_doc.search_range_str:
            print_wrapped(
                1, "You previously told me about this range of paragraphs:",
                3, f"{word.pr_ready_doc.search_range_str}",
                1, "Do you want me to proofread the paragraphs in this "\
                    "range? (y/n)")
            menu = input().lower()
            if menu == 'y':
                range_input = word.pr_ready_doc.search_range_str
            elif menu == 'n':
                print_wrapped(1, "Okay. Let's pick a different one.")
            elif menu == 'x':
                update_page('pg_file_select')
                break
            else:
                print_wrapped(
                    1, "I'm afraid I don't understand. Let's try that again.")
                continue
        if not range_input:
            print_wrapped(1,"Which range would you like me to search?")
            range_input = input().lower()
        if range_input == 'x':
            print_wrapped(
                1, "Oh? Okay, going back to re-select your file.")
            update_page('pg_file_select')
            break
        proofdoc.test_search_range(range_input)
        if proofdoc.error_status == 'error_4':
            print_wrapped(
                3, "Error: You specified a paragraph outside the available "\
                    "range.")
            continue
        elif proofdoc.error_status == 'error_5':
            print_wrapped(
                3, "Error: You have to input your range as "\
                    "'#', '#-#', 'start-#', or '#-end'.")
            continue
        elif proofdoc.error_status == 'error_6':
            print_wrapped(
                3, "Error: You gave a range that doesn't "\
                    "fit the requested format.")
            continue
        elif proofdoc.error_status == 'error_7':
            print_wrapped(
                3, "Error: The range's first value has to "\
                    "be either 'start' or a positive integer.")
            continue
        elif proofdoc.error_status == 'error_8':
            print_wrapped(
                3, "Error: The range's second value has to "\
                    "be either 'end' or a positive integer.")
            continue
        elif proofdoc.error_status == 'error_9':
            print_wrapped(3,
                "Error: The first value in your range needs to be less than "\
                    "the second value.")
            continue
        elif proofdoc.error_status == 'error_10':
            print_wrapped(
                3, "Error: You requested a starting value outside"\
                    " your document's range of available paragraphs.")
            continue
        elif proofdoc.error_status == 'error_11':
            print_wrapped(
                3, "Error: You requested an ending value outside "\
                    "your document's range of available paragraphs.")
            continue
        elif proofdoc.error_status != 'okay':
            print_wrapped(
                3, "Error: I'm still having trouble processing that search "\
                    f"range, and I'm not sure why. ({proofdoc.error_status})")
            continue
        elif proofdoc.search_range_list:
            # The presence of search_range_list indicates that the
            # search range was tested and found valid.
            pass
        else:
            print_wrapped(
                1, "I reached a nonstandard error when trying to "\
                    "parse your search range. Sorry about that. It's "\
                    "probably a bug.")
            continue
        paras_in_range = proofdoc.get_paras_in_range()
        if proofdoc.error_status == 'error_12':
            print_wrapped(
                1, "Error: I couldn't find any paragraphs in the "\
                    "range provided. Strange.")
            continue
        if not isinstance(paras_in_range,dict):
            print_wrapped(
                1, "Error: I'm not sure what came out of your file, "\
                    "but it isn't anything I can work with.")
            continue
        split_paras = proofdoc.split_paragraphs(paras_in_range)
        if proofdoc.error_status == 'error_13' or not split_paras:
            print_wrapped(
                1, "Error: I encountered a problem when trying to "\
                    "go through your range's paragraphs word by word.")
            continue
        else:
            print_wrapped(1, "Thank you! That range works fine.")
            update_page('pg_file_confirm')

    # Step 3: viewing and confirming
    while word.current_page == 'pg_file_confirm':
        if not paras_in_range or not split_paras:
            print_wrapped(
                1, "You don't have a confirmed search range for "\
                    "the file you want proofread. I don't know how you "\
                    "got here, but it's probably a bug. Sorry.")
            update_page('pg_range_select')
            break
        first_para, last_para, all_text_in_range = \
        proofdoc.get_para_samples(paras_in_range)
        print_wrapped(
            1, ["So, to confirm:",
            "You want me to proofread this file:"],
            3, f"{proofdoc.filename}",
            1, "In this range:",
            3, f"{proofdoc.search_range_str}",
            1, "This is the first paragraph I'll be checking:")
        for p_index, para in first_para.items():
            print_wrapped(
                3, f"Paragraph {p_index +1}:",
                4,para)
        print_wrapped(
            1, "And this is the last paragraph I'll be checking:")
        for p_index, para in last_para.items():
            print_wrapped(
                3, f"Paragraph {p_index +1}:",
                4,para)
        print_wrapped(
            1, "Is this correct? (y/n) (If you "\
                "want, I can show you all the text in the range you "\
                "gave. Just input 't'.)")
        menu = input().lower()
        if menu == 'n' or menu == 'x':
            print_wrapped(1, "Okay. Let's go back to the last step.")
            update_page('pg_range_select')
            break
        elif menu == 't':
            print_wrapped(
                1, "Here's all the text in the range you gave me:")
            for p_index, para in all_text_in_range.items():
                print_wrapped(
                    3, f"Paragraph {p_index +1}:",
                    4,para)
            continue
        # When file selection is complete, and only then, this block
        # saves a copy of the confirmed file content.
        elif menu == 'y':
            print_wrapped(
                1, ["""\
                    Excellent! Then the next step is to pick
                    \"Proofread the selected file\" on the main menu.
                    Your file has been formatted for proofreading and
                    will be saved until you redo this file selection
                    step, even if you quit the program.""",
                "Returning to the main menu."])
            word.pr_ready_doc = proofdoc
            word.save_settings()
            update_page('pg_main_menu')
        else:
            print_wrapped(
                1, "I don't understand. Let's try that again.")

    # This menu option and the following blocks are for proofreading the
    # selected and confirmed file.
    while word.current_page == 'pg_proofread_file':
        if not word.pr_ready_doc:
            print_wrapped(
                1, """\
                    You don't have a file that's been formatted and prepared
                    for searching yet. You'll need to \"select a file to
                    "proofread\" before you can perform this step.""")
            update_page('pg_main_menu')
            break
        if not 'Yes' in word.toggle_settings.values():
            print_wrapped(
                1, """\
                    You disabled all the target categories, and I don't have
                    anything to search for! I can't proofread your document
                    like this. Hit \"View or edit the terms I target\"
                    and enable at least one category, please.""")
            update_page('pg_main_menu')
            break
        proofdoc = word.pr_ready_doc
        paras_in_range = proofdoc.get_paras_in_range()
        split_paras = proofdoc.split_paragraphs(paras_in_range)
        first_para, last_para, all_text_in_range = \
        proofdoc.get_para_samples(paras_in_range)
        print_wrapped(
            2, "Proofreading the Selected File",
            1, "Alright! Now, the file I have saved for proofreading is this:",
            3, proofdoc.filename,
            1, "The range of paragraphs I'll be proofreading is this:",
            3, f"{proofdoc.search_range_str}",
            1, "The first paragraph in that range is this:")
        for p_index, para in first_para.items():
            print_wrapped(
                3, f"Paragraph {p_index +1}:",
                4,para)
        print_wrapped(
            1, "And the last paragraph in that range is this:")
        for p_index,para in last_para.items():
            print_wrapped(
                3, f"Paragraph {p_index +1}:",
                4,para)
        print_wrapped(
            1, "Also, based on your settings, I'll be looking for targets "\
                "in the following categories:")
        for category, setting in word.toggle_settings.items():
            if setting == 'Yes':
                print_wrapped(3, f"{category}")
        print_wrapped(
            1, "And I'll be ignoring any occurrences of these disabled "\
                "targets:")
        # Any disabled targets in enabled categories are added to the
        # list display_disabled_targs, which is then sorted.
        display_disabled_targs = []
        all_targs = word.TargetList.build_dict_of_all_targs()
        for cat, targs in all_targs.items():
            if word.toggle_settings[cat] == 'Yes':
                for targ in targs:
                    if targ in word.disabled_targs:
                        targ = word.convert_tuple_to_str(targ)
                        display_disabled_targs.append(targ)
        if not display_disabled_targs:
            print_wrapped(3,"(None in enabled categories)")
        else:
            for targ in sorted(display_disabled_targs):
                print_wrapped(3, f"{targ}")
        print_wrapped(
            1, "Is this correct? (y/n) (Or input 't' and "\
                "I can show you all the text in your chosen range)")
        menu = input().lower()
        if menu == 't':
            print_wrapped(
                1, "Here's all the text I'll be "\
                    "proofreading:")
            for para_index, para in all_text_in_range.items():
                print_wrapped(
                    3, f"Paragraph {para_index +1}:",
                    4,para)
            continue
        elif menu == 'x':
            update_page('pg_main_menu')
            break
        elif menu == 'n':
            print_wrapped(
                1, """\
                    In that case, you'll need to redo file selecton and
                    otherwise change settings to suit your needs.
                    Pick \"Proofread the selected file\" again
                    when you're ready.""")
            update_page('pg_main_menu')
            break
        elif menu == 'y':
            pass
        else:
            print_wrapped(1, "I don't understand. Can we try again?")
            continue
        print_wrapped(
            1, "Hit Enter one more time and I'll proofread your document.")
        menu = input().lower()
        if menu == 'x':
            update_page('pg_main_menu')
            break
        print_wrapped(1, "Give me a minute...")
        # This is where the bulk of the program's main functions are
        # launched all at once. First an instance of TargetList is
        # constructed.
        active_targetlist = word.TargetList('enabled')
        active_targetlist.set_targets()
        a, b = active_targetlist.separate_target_words_and_phrases()
        # Then the program searches proofdoc for the targets output by
        # that instance.
        c = proofdoc.search_text_for_target_words(split_paras, a)
        d = proofdoc.search_text_for_target_phrases(split_paras, b)
        # Then the targets found in proofdoc are used to make an
        # instance of ListOfMatches.
        active_matchlist = word.ListOfMatches(c,d)
        active_matchlist.sort_matches()
        update_page('pg_display_results')

    while word.current_page == 'pg_display_results':
        print_wrapped(2, "Results")
        if not active_matchlist:
            print_wrapped(
                1, "Something went wrong. How did you get here without "\
                    "the right values saved? It's probably because of a "\
                    "page navigation bug.")
            update_page('pg_main_menu')
            break
        if word.group_common_targs == 'never':
            match_list = active_matchlist.matches_ordered[:]
        elif word.group_common_targs == 'always':
            displaying_common = True
            common, uncommon = active_matchlist.find_common_matches()
            active_matchlist.display_common_matches(common)
            match_list = uncommon[:]
        # If group_common_targs is set to 'ask' and common matches have
        # been found, this block asks the user for additional input.
        elif word.group_common_targs == 'ask':
            match_list = active_matchlist.matches_ordered[:]
            common, uncommon = active_matchlist.find_common_matches()
            if common:
                print_wrapped(
                    1, """\
                        My search found that a few terms are particularly
                        common, appearing five or more times. Do you want
                        me to group these common targets together for
                        easier viewing? (y/n)""")
                menu = input().lower()
                if menu == 'y':
                    displaying_common = True
                    active_matchlist.display_common_matches(common)
                    match_list = uncommon[:]
                # If the user answers 'no', the variable match_list
                # is not overwritten and no common matches are
                # displayed.
                elif menu == 'n':
                    print_wrapped(1, "Understood.")
                elif menu == 'x':
                    update_page('pg_proofread_file')
                    break
                else:
                    print_wrapped(
                        1, "I don't understand. One more time, please?")
                    continue
        # The variable results_display can be 'category' or
        # 'appearance'.
        if word.results_display == 'category':
            active_matchlist.display_matches_by_category(match_list, \
                displaying_common)
        elif word.results_display == 'appearance':
            active_matchlist.display_matches_by_appearance(match_list, \
                displaying_common)
        print_wrapped(
            1, f"""\
                Hit Enter to return to menu. I can pull up your results again
                later as long as you don't overwrite or delete your formatted
                text. You can also change how I display my results; just pick
                "Settings and extras" on the main menu.""")
        input()
        displaying_common = False
        update_page('pg_main_menu')

    while word.current_page == 'pg_settings_extras':
        print_wrapped(
            2, "Settings and Extras",
            1, ["""\
                For settings related to what words and phrases I search for,
                go to "View or edit the terms I target" instead. For general
                settings, you're in the right place. How can I help?""",
            ""],
            6, ["1 - Change how I display proofreading results",
            "2 - View or delete saved data",
            "",
            "3 - View the credits",
            "",
            "4 - Go back"])
        menu = input().lower()
        if menu == '1':
            update_page('pg_results_settings')
        elif menu == '2':
            update_page('pg_saved_data')
        elif menu == '3':
            print_wrapped(2, "Credits")
            with open('data/credits.txt', encoding='utf-8') as f:
                text = f.read()
            text = text.split('\n')
            print()
            for para in text:
                print_wrapped(7,para)
        elif menu == '4' or menu == 'x':
            update_page('pg_main_menu')
        else:
            print_wrapped(
                1, "I don't understand. Can you try again, please?")

    while word.current_page == 'pg_results_settings':
        if not results_display_temp and not group_common_targs_temp:
            results_display_temp = word.results_display
            group_common_targs_temp = word.group_common_targs
        print_wrapped(
            2, "Results Display Settings",
            1, """\
                I can change how my proofreading results are displayed in
                two different ways:""",
            7, ["""\
                By default, I group results by category first, then by
                order of appearance. I can instead group results only by
                appearance; while I'll still show each target's
                category, it won't be emphasized.""",
            """\
                If I find the same target five or more times, I can group
                each instance so they don't crowd your results.
                My proofreading picks up a few common terms like "very",
                and you might prefer that I group those terms'
                appearances. By default, I ask before doing so."""],
            1, ["""\
                Input a number and I'll toggle that number's entry to the
                next available option.""",
            ""],
            6, ["1 - Sorting method: ".ljust(30)+ results_display_temp,
            "2 - Group common targets: ".ljust(30)+ group_common_targs_temp,
            "",
            "3 - Save and quit",
            "4 - Go back without saving"])
        menu = input().lower()
        if menu == '1':
            if results_display_temp == 'category':
                results_display_temp = 'appearance'
            elif results_display_temp == 'appearance':
                results_display_temp = 'category'
        elif menu == '2':
            if group_common_targs_temp == 'always':
                group_common_targs_temp = 'ask'
            elif group_common_targs_temp == 'ask':
                group_common_targs_temp = 'never'
            elif group_common_targs_temp == 'never':
                group_common_targs_temp = 'always'
        elif menu == '3':
            word.results_display = results_display_temp
            word.group_common_targs = group_common_targs_temp
            results_display_temp = ''
            group_common_targs_temp = ''
            word.save_settings()
            print_wrapped(1, "Settings saved.")
            update_page('pg_settings_extras')
        elif menu == '4' or menu == 'x':
            results_display_temp = ''
            group_common_targs_temp = ''
            update_page('pg_settings_extras')
        else:
            print_wrapped(1, "I don't understand. Try again, please?")

    while word.current_page == 'pg_saved_data':
        print_wrapped(
            2, "View or Delete Saved Data",
            1, ["Some of my data is retained even when you close me. "\
                "Here are the saved options you can view and delete. Please "\
                "read and input your choices carefully!",
            ""],
            6, ["1 - User-Defined Targets",
            "2 - Category Settings",
            "3 - Disabled Targets",
            "4 - Results Display Settings",
            "5 - Current document prepared for proofreading",
            "",
            "6 - Delete all",
            "",
            "7 - Go back"])
        menu = input().lower()
        if menu == '1':
            update_page('pg_delete_ud_targs')
        elif menu == '2':
            update_page('pg_delete_toggle')
        elif menu == '3':
            update_page('pg_delete_disabled_targs')
        elif menu == '4':
            update_page('pg_delete_display')
        elif menu == '5':
            update_page('pg_delete_ready_doc')
        elif menu == '6':
            update_page('pg_delete_all')
        elif menu == '7' or menu == 'x':
            update_page('pg_settings_extras')
        else:
            print_wrapped(
                1, "I don't understand. Could you please try again?")

    while word.current_page == 'pg_delete_ud_targs':
        print_wrapped(2, "View or Delete User-Defined Targets")
        count = 0
        user_defined_targs_list = []
        for category, targs in word.user_defined.items():
            print_wrapped(1, f"{category}")
            if not targs:
                print_wrapped(12, "(None listed)")
            for targ, desc in targs.items():
                user_defined_targs_list.append(targ)
                count += 1
                print_wrapped(
                    6, f"{count} - "\
                        f"{word.convert_tuple_to_str(targ)}:",
                    4, f"{desc}")
        if count == 0:
            print_wrapped(
                1, "I have no user-defined targets saved, so "\
                    "there's nothing to delete. Press Enter to go back.")
            input()
            update_page('pg_saved_data')
            break
        print_wrapped(
            10,"",
            6, [f"{count +1} - Delete all",
            f"{count +2} - Go back"],
            1, "Input the number of the target you want me "\
                "to delete.")
        menu = input().lower()
        menu = word.try_str_to_int(menu)
        if menu in range(1, count +1):
            targ = user_defined_targs_list[menu -1]
            if targ in word.user_defined['User-Defined Words'].keys():
                del word.user_defined['User-Defined Words'][targ]
                # Deleting a user-defined target also involves removing
                # it from the disabled_targs list or any other lists it
                # might have been added to.
                if targ in word.disabled_targs:
                    word.disabled_targs.remove(targ)
                print_wrapped(1, f"'{targ}' deleted.")
                word.save_settings()
                continue
            elif targ in word.user_defined['User-Defined Phrases'].keys():
                del word.user_defined['User-Defined Phrases'][targ]
                if targ in word.disabled_targs:
                    word.disabled_targs.remove(targ)
                print_wrapped(1, f"'{targ}' deleted.")
                word.save_settings()
                continue
            else:
                print_wrapped(
                    1, "I encountered an error and couldn't "\
                        "delete the target. Sorry.")
                continue
        elif menu == count +1:
            print_wrapped(
                1, "You're sure you want me to delete all user-"\
                    "defined proofreading targets? (y/n)")
            menu = input().lower()
            if menu == 'y':
                for cat, targs in word.user_defined.items():
                    for targ in targs.keys():
                        if targ in word.disabled_targs:
                            word.disabled_targs.remove(targ)
                word.user_defined['User-Defined Words'].clear()
                word.user_defined['User-Defined Phrases'].clear()
                print_wrapped(1, "All targets cleared.")
                word.save_settings()
                continue
            elif menu == 'n':
                continue
            elif menu == 'x':
                word.save_settings()
                update_page('pg_saved_data')
                break
            else:
                print_wrapped(
                    1, "Sorry, but I didn't understand that. Can we "\
                        "try again?")
                continue
        elif menu == count +2 or menu == 'x':
            word.save_settings()
            update_page('pg_saved_data')
            break
        else:
            print_wrapped(
                1, "Sorry, but I don't follow. Can we "\
                    "try again?")
            continue

    while word.current_page == 'pg_delete_toggle':
        print_wrapped(
            2, "View or Delete Category Settings",
            1, "Here are your current settings on which target categories "\
                "are enabled or disabled for proofreading:")
        count = 0
        for title, setting in word.toggle_settings.items():
            count += 1
            print_wrapped(3,
                f"{count} - {title}".ljust(40) + f"search: {setting}")
        if not 'No' in word.toggle_settings.values():
            print_wrapped(
                1, "All settings are already set to the default "\
                    "value, 'Yes'. Press Enter to go back.")
            input()
            update_page('pg_saved_data')
            break
        print_wrapped(
            1, "Do you want to restore all category settings to "\
                "their default value of 'Yes'? (y/n)")
        menu = input().lower()
        if menu == 'y':
            for cat in word.toggle_settings.keys():
                word.toggle_settings[cat] = 'Yes'
            word.save_settings()
            print_wrapped(1, "Category settings returned to default.")
            update_page('pg_saved_data')
        elif menu == 'n' or menu == 'x':
            update_page('pg_saved_data')
        else:
            print_wrapped(1, "I didn't understand that. Try again, please?")

    while word.current_page == 'pg_delete_disabled_targs':
        print_wrapped(
            2, "View or Delete List of Disabled Targets",
            1, "Below is the list of targets you've disabled. If you want to "\
                "re-enable specific targets without clearing the whole list, "\
                "you can do that by choosing \"View or edit the terms I "\
                "target\" then \"Disable a search target\" in the main menu.")
        all_targs = word.TargetList.build_dict_of_all_targs()
        count = 0
        for cat, targs in all_targs.items():
            disabled_targs_present = False
            print_wrapped(12, f"{cat}")
            for targ, desc in targs.items():
                if targ in word.disabled_targs:
                    count += 1
                    disabled_targs_present = True
                    print_wrapped(
                        9, f"{word.convert_tuple_to_str(targ)}:",
                        5, f"{desc}")
            if not disabled_targs_present:
                print_wrapped(9,"(None listed)")
        if count == 0:
            print_wrapped(
                1, "You haven't disabled any targets, so I have "\
                    "no disabled targets list to delete. Press Enter to go "\
                    "back.")
            input()
            update_page('pg_saved_data')
            break
        if count != len(word.disabled_targs):
            print_wrapped(
                1, "I encountered an error: my list of disabled "\
                    f"targets has {len(word.disabled_targs)} items in it, "\
                    f"but I was only able to count {count} just now.")
        print_wrapped(
            1, "Do you want to delete this list and re-enabled all "\
                "targets? (y/n)")
        menu = input().lower()
        if menu == 'y':
            print_wrapped(1, "All targets re-enabled.")
            word.disabled_targs = []
            word.save_settings()
            update_page('pg_saved_data')
        elif menu == 'n' or menu == 'x':
            update_page('pg_saved_data')
        else:
            print_wrapped(
                1, "I didn't understand that. One more time, please?")

    while word.current_page == 'pg_delete_display':
        print_wrapped(
            2, "View or Delete Display Settings",
            1, "Here are the display settings I've saved.",
            3, ["1 - Sorting method: ".ljust(30)+ word.results_display,
            "2 - Group common targets: ".ljust(30)+ word.group_common_targs])
        if word.results_display == 'category' \
        and word.group_common_targs == 'ask':
            print_wrapped(
                1, "The display options are already at their "\
                    "default settings. Press Enter to go back.")
            input()
            update_page('pg_saved_data')
            break
        print_wrapped(
            1, "Do you want to return the display settings back to "\
                "their defaults? (y/n)")
        menu = input().lower()
        if menu == 'y':
            word.results_display = 'category'
            word.group_common_targs = 'ask'
            print_wrapped(
                1, "Display options returned to their default "\
                    "settings.")
            word.save_settings()
            update_page('pg_saved_data')
        elif menu == 'n' or menu == 'x':
            update_page('pg_saved_data')
        else:
            print_wrapped(1, "I don't follow. Try again?")

    while word.current_page == 'pg_delete_ready_doc':
        if not word.pr_ready_doc:
            print_wrapped(
                1, "I don't have a file saved for proofreading. In a way, "
                    "my job is already done!",
                1, "Press Enter to go back.")
            input()
            update_page('pg_saved_data')
            break
        proofdoc = word.pr_ready_doc
        paras_in_range = proofdoc.get_paras_in_range()
        split_paras = proofdoc.split_paragraphs(paras_in_range)
        first_para, last_para, all_text_in_range = \
        proofdoc.get_para_samples(paras_in_range)
        print_wrapped(
            2, "View or Delete the Document Saved For Proofreading",
            1, "This is the filename of the document I currently have saved:",
            3, proofdoc.filename,
            1, "This is the range of paragraphs to proofread:",
            3, f"{proofdoc.search_range_str}",
            1, "The first paragraph in that range is this:")
        for p_index, para in first_para.items():
            print_wrapped(3, f"Paragraph {p_index +1}:",
            4,para)
        print_wrapped(1, "And the last paragraph in that range is this:")
        for p_index,para in last_para.items():
            print_wrapped(3, f"Paragraph {p_index +1}:",
            4,para)
        print_wrapped(
            1, "Would you like me to delete this saved document? "\
                "You will need to select a new document and a valid range "\
                "before I can perform proofreading. (y/n)")
        menu = input().lower()
        if menu == 'y':
            word.pr_ready_doc = ''
            word.save_settings()
            print_wrapped(1, "Alright. The document has been deleted.")
            update_page('pg_saved_data')
        elif menu == 'n' or 'x':
            update_page('pg_saved_data')
        else:
            print_wrapped(
                1, "I didn't understand that. One more time, please?")

    while word.current_page == 'pg_delete_all':
        print_wrapped(
            1, ["""\
                Preparing to delete all saved data. You can also clear my saved
                data by deleting the file 'config.json' in my directory while
                I'm not running.""",
            "Would you like to delete all saved data? (y/n)"])
        menu = input().lower()
        if menu == 'y':
            print_wrapped(1, "Are you sure? (y/n)")
            menu = input().lower()
            if menu == 'y':
                word.user_defined['User-Defined Words'] = {}
                word.user_defined['User-Defined Phrases'] = {}
                for cat in word.all_cats_list:
                    word.toggle_settings[cat] = 'Yes'
                word.pr_ready_doc = ''
                word.disabled_targs = []
                word.results_display = 'category'
                word.group_common_targs = 'ask'
                word.save_settings()
                print_wrapped(1, "All saved data deleted.")
                update_page('pg_settings_extras')
            elif menu == 'n' or menu == 'x':
                print_wrapped(1, "Alright. Backing out.")
                update_page('pg_saved_data')
            else:
                print_wrapped(
                    1, "I didn't catch that. We'll need to try "\
                        "again.")
        elif menu == 'n' or 'x':
            update_page('pg_saved_data')
        else:
            print_wrapped(1, "I don't follow. Can you say that again?")

    while word.current_page == 'pg_quit_prompt':
        print_wrapped(1, "You're leaving? (y/n)")
        menu = input().lower()
        if menu == 'y' or menu == 'yes':
            print_wrapped(
                1, "Okay! See you!",
                2, "Goodbye")
            input()
            update_page('pg_quit_noprompt')
        elif menu == 'n' or menu == 'no':
            print_wrapped(1, "Okie doke.")
            update_page('pg_main_menu')
        else:
            print_wrapped(1, "I don't follow. Can you please try again?")

    while word.current_page == 'pg_test_function':
        print("Disabled targs:")
        for item in word.disabled_targs:
            print(f"{type(item)}: {item}")


        update_page('pg_main_menu')

        all_targs = word.TargetList.build_dict_of_all_targs()
        print("Clunky Words:")
        for key, value in all_targs['Clunky Words'].items():
            print(f"{type(key)}: {key}")
            print(f"{type(value)}: {value}")
            print()

    if word.current_page == 'pg_quit_noprompt':
        break
