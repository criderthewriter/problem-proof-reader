import chardet
import docx
import json
import re
import string
import textwrap

import targets

# This block initializes dictionaries that will store user-defined words
# and phrases to search for.
user_defined = {
    'User-Defined Words': {},
    'User-Defined Phrases': {},
    }

def sort_dictionary_items(input_dict):
    """Given a dictionary of strings (keys and values), sort the
    dictionary's keys (including tuples, by looking at the tuple's
    first value), then return a new dictionary of the sorted keys and
    values.
    """
    copy = {}
    new_dict = {}
    for key, value in input_dict.items():
        if isinstance(key,tuple):
            key = key[0]
        copy[key] = value
    old = sorted(copy.items())
    for tup in old:
        a = tup[0]
        b = tup[1]
        for key, value in input_dict.items():
            if isinstance(key,tuple) and a in key:
                a = key
                break
        new_dict[a] = b
    return new_dict

# This block sorts different target categories and populates lists of
# categories for later reference.
predefined_cats = []
user_defined_cats = []
all_cats_list = []
for cat, targs in targets.predefined.items():
    targets.predefined[cat] = sort_dictionary_items(targs)
    predefined_cats.append(cat)
for cat, targs in user_defined.items():
    user_defined[cat] = sort_dictionary_items(targs)
    user_defined_cats.append(cat)
all_cats_list = predefined_cats + user_defined_cats

# This block declares toggle settings that can be overwritten by loading
# a .json file. Every category is initially set to 'Yes'.
toggle_settings = {}
for cat in all_cats_list:
    toggle_settings[cat] = 'Yes'

# These variables govern program settings, and several are saved by the
# save_settings() function.
pr_ready_doc = ''
disabled_targs = []
# results_display can be set to 'category' (default) or 'appearance'.
results_display = 'category'
# group_common_targs can be set to 'always', 'ask' (default), or
# 'never'.
group_common_targs = 'ask'

# This line defines punctuation to be filtered out, including Word-
# formatted characters.
punctuation_plus = string.punctuation + '•‘’“”–—… '
# This line defines dashes, including uncommon ones, to be used as word
# breaks.
dashes = ['-','–','—','_','/']
trailing_punct = ''.join(dashes) + ',.…'

# This block defines textwrap zones that will display paragraphs
# differently based on the list item called.
zones = [
    # Zone 1: newline at start, for blocks of text
    textwrap.TextWrapper(initial_indent='\n'),
    # Zone 2: newline at start, details in print_wrapped, for headings
    textwrap.TextWrapper(width=71, initial_indent='\n',
        break_on_hyphens=False, break_long_words=False),
    # Zone 3: every line tabbed, for quoted and example text
    textwrap.TextWrapper(width=62, initial_indent='\t',
        subsequent_indent='\t'),
    # Zone 4: every line two tabs, for deeper formatting
    textwrap.TextWrapper(width=55, initial_indent='\t\t',
        subsequent_indent='\t\t'),
    # Zone 5: every line three tabs, for deepest formatting
    textwrap.TextWrapper(width=48,initial_indent='\t\t\t',
        subsequent_indent='\t\t\t'),
    # Zone 6: first line half-tab, other lines tab; for numbered list
    textwrap.TextWrapper(initial_indent='    ',subsequent_indent='\t'),
    # Zone 7: first line bulleted tab, other lines tab; for bulleted list
    textwrap.TextWrapper(width=62, initial_indent='      • ',
        subsequent_indent='\t'),
    # Zone 8: every line three tabs, first line four spaces, for paragraphs
    textwrap.TextWrapper(width=48,initial_indent='\t\t\t    ',
        subsequent_indent='\t\t\t'),
    # Zone 9: zone 4 alt, with newline at start
    textwrap.TextWrapper(width=55, initial_indent='\n\t\t',
        subsequent_indent='\t\t'),
    # Zone 10: default, rarely used
    textwrap.TextWrapper(),
    # Zone 11: irregular tabbing; for double- or triple-digit numbered list
    textwrap.TextWrapper(width=65,initial_indent='    ',
        subsequent_indent='\t     '),
    # Zone 12: zone 3 alt, with newline at start
    textwrap.TextWrapper(width=62, initial_indent='\n\t',
        subsequent_indent='\t'),
    ]

# These variables keep track of which page the user is being sent to
# next, and where they just were, based on the user's inputs. They are
# kept to avoid having the script's menus and while True: loops nested
# too deeply.
prev_page = ''
current_page = ''

def try_str_to_int(input_str):
    """For a given number saved as a string, attempt to convert the
    string to an integer.
    """
    try:
        input_int = int(input_str)
        return input_int
    except ValueError:
        return input_str

def convert_dict_strings(input_dict):
    """When a dictionary is saved to a json file, any integer keys or
    values are saved as text and then loaded as strings. For a given
    dictionary, convert the strings back to integers.
    """
    dict_copy = {}
    for key, value in input_dict.items():
        key = try_str_to_int(key)
        value = try_str_to_int(value)
        dict_copy[key] = value
    return dict_copy

def convert_list_strings(input_list):
    """When a dictionary is saved to a json file, any integer keys or
    values are saved as text and then loaded as strings. For a given
    dictionary, convert the strings back to integers.
    """
    list_copy = []
    for item in input_list:
        item = try_str_to_int(item)
        list_copy.append(item)
    return list_copy

def convert_tuple_to_str(input_targ):
    """For a given tuple containing strings that are each iterations of
    a proofreading target, combine each string into the tuple into a
    string separated by commas. Only to be used for displaying the
    target attractively to the user.
    """
    if isinstance(input_targ,tuple):
        targ = ', '.join(input_targ)
    else:
        targ = input_targ
    return targ

def convert_list_to_tuple(input_list):
    """When a tuple is saved to a json file, it is saved as a json list
    because json does not handle tuples. For a given list, convert it
    back to a tuple. Currently unused.
    """
    return tuple(input_list)

def save_settings():
    """Save the user's settings, class instances, and other information
    into a json file. Since custom class instances cannot be saved,
    save a dictionary of its attributes instead.
    """
    json_data = {
        'user_defined_targs': user_defined,
        'toggle': toggle_settings,
        'disabled_targs': disabled_targs,
        'display_setting': results_display,
        'group_common_targs': group_common_targs,
        'pr_ready_doc': {},
        }
    if pr_ready_doc:
        json_data['pr_ready_doc'] = {
            'filename': pr_ready_doc.filename,
            'error_status': pr_ready_doc.error_status,
            'all_indexed_paras': pr_ready_doc.all_indexed_paras,
            'search_range_str': pr_ready_doc.search_range_str,
            'search_range_list': pr_ready_doc.search_range_list,
            }
    with open('config.json', 'w') as f:
        json.dump(json_data, f)


def load_settings():
    """Load the user's settings, etc if the appropriate json file is
    detected, and create the json file if it is not detected.
    """
    global user_defined, toggle_settings, pr_ready_doc, results_display,\
        group_common_targs, disabled_targs
    try:
        with open('config.json') as f:
            loaded = json.load(f)
            user_defined = loaded['user_defined_targs']
            toggle_settings = loaded['toggle']
            results_display = loaded['display_setting']
            group_common_targs = loaded['group_common_targs']
            # json saves tuples as lists, so they must be converted
            # back to tuples for consistency.
            list_copy = []
            for targ in loaded['disabled_targs']:
                if isinstance(targ,list):
                    list_copy.append(tuple(targ))
                else:
                    list_copy.append(targ)
            disabled_targs = list_copy
            # If a proofread-ready instance of DocToProofread was saved,
            # save_settings() saved it as a dictionary. If this block
            # finds such a dictionary, it rebuilds it into a
            # DocToProofread instance.
            if loaded['pr_ready_doc']:
                data = loaded['pr_ready_doc']
                pr_ready_doc = DocToProofread(data['filename'])
                pr_ready_doc.error_status = data['error_status']
                pr_ready_doc.all_indexed_paras = \
                    convert_dict_strings(data['all_indexed_paras'])
                pr_ready_doc.search_range_str = data['search_range_str']
                pr_ready_doc.search_range_list = \
                    convert_list_strings(data['search_range_list'])
    except FileNotFoundError:
        save_settings()

def print_wrapped(*para_input):
    """Given a tuple of integer-string pairs, apply word wrapping to the
    string as dictated by its paired integer, calling wrap zones defined
    by textwrap and changing settings if new integer-string pairs are
    also given. Display the results. Input format requires at least a
    zone number, then a string or list of strings, but it can accept
    any number of these pairs if they are separated by commas.
    """
    num_paras = int(len(para_input)/2)
    if num_paras == 1:
        zone_input = para_input[0]
        text_input = para_input[1]
        zone = zones[zone_input -1]
        if isinstance(text_input,str):
            # If the zone number given is 2, the text is presented in a
            # single line surrounded with hyphens so as to create a long
            # horizontal line. The text input provided for that zone
            # should be a string, not a list of strings.
            if zone_input == 2:
                text_input = text_input.center(70,'-')
            print(zone.fill(text=textwrap.dedent(text_input)))
        elif isinstance(text_input,list):
            for item in text_input:
                print(zone.fill(text=textwrap.dedent(item)))
    elif len(para_input) % 2 == 0.0:
        para_input = list(para_input)
        for num in range(num_paras):
            zone_input = para_input.pop(0)
            text_input = para_input.pop(0)
            zone = zones[zone_input -1]
            if isinstance(text_input,str):
                if zone_input == 2:
                    text_input = text_input.center(70,'-')
                print(zone.fill(text=textwrap.dedent(text_input)))
            elif isinstance(text_input,list):
                for item in text_input:
                    print(zone.fill(text=textwrap.dedent(item)))
    else:
        raise Exception("Unexpected argument configuration.")

def define_new_target(targ, description):
    """Add a user-defined target and a matching description to the
    appropriate dictionary, then sort the dictionary's keys, rebuild it
    into a dictionary, and save it to a .json file.
    """
    global user_defined
    targ_copy = targ
    for cha in dashes:
        if cha in targ_copy:
            targ_copy = targ_copy.replace(cha, cha+' ')
    if len(targ_copy.split()) == 1:
        category = 'User-Defined Words'
    else:
        category = 'User-Defined Phrases'
    user_defined[category][targ] = description
    user_defined[category] = sort_dictionary_items(user_defined[category])
    save_settings()

def update_page(pages):
    global prev_page, current_page
    """Update variables that send the user to a different page of the
    program and remember the last page visited.
    """
    prev_page = current_page
    current_page = pages


class DocToProofread:
    """A class to contain a document that has been split apart for
    proofreading, along with the user-defined parameters necessary to
    begin proofreading.
    """
    def __init__(self, filename):
        """Initialize attributes to describe a file to be proofread.
        Attributes are formatted so the document's text data is only
        saved in one place.
        """
        self.filename = filename
        self.error_status = 'okay'
        self.all_indexed_paras = {}
        self.search_range_str = ''
        self.search_range_list = []

    @staticmethod
    def read_docx(filename):
        """Designate a .docx file to search for target words/phrases,
        and output all of its text in a usable format.
        """
        book = docx.Document(filename)
        all_paras = book.paragraphs
        all_paras_filtered = []
        # This block filters out blank paragraphs.
        for para in all_paras:
            if para.text != '':
                all_paras_filtered.append(para)
        all_indexed_paras = {}
        para_index = -1
        # Returns a dictionary of (index):(string of paragraph text)
        # pairs.
        for para in all_paras_filtered:
            para_index += 1
            all_indexed_paras[para_index] = para.text
        return all_indexed_paras

    @staticmethod
    def read_txt(filename):
        """Designate a .txt file to search for target words/phrases,
        determine its encoding, and output all of its text in a usable
        format.
        """
        with open(filename, mode='rb') as f:
            rawdata = f.read()
            result = chardet.detect(rawdata)
            charenc = result['encoding']
        with open(filename, encoding=charenc) as f:
            all_text = f.read()
        unfiltered_paras = all_text.split('\n')
        all_paras_filtered = []
        # This block filters out blank paragraphs.
        for para in unfiltered_paras:
            if para:
                all_paras_filtered.append(para)
        all_indexed_paras = {}
        para_index = -1
        # Returns a dictionary of (index):(string of paragraph text)
        # pairs.
        for para in all_paras_filtered:
            para_index += 1
            all_indexed_paras[para_index] = para
        return all_indexed_paras

    def read_file(self):
        """Examine a filename for validity then perform the appropriate
        reading method based on file type, and return a dictionary of
        the file's indexed paragraphs.
        """
        self.error_status = 'okay'
        filename_raw = fr'{self.filename}'
        file_in_subfolder = f"files_to_proofread/{filename_raw}"
        if filename_raw.endswith('.docx'):
            file_type = 'docx'
        elif filename_raw.endswith('.txt'):
            file_type = 'txt'
        else:
            self.error_status = 'error_1'
            return None
        if file_type == 'txt':
            try:
                paras = self.read_txt(filename_raw)
            except:
                try:
                    paras = self.read_txt(file_in_subfolder)
                except:
                    self.error_status = 'error_2'
                    return None
        elif file_type == 'docx':
            try:
                paras = self.read_docx(filename_raw)
            except:
                try:
                    paras = self.read_docx(file_in_subfolder)
                except:
                    self.error_status = 'error_2'
                    return None
        if not paras:
            self.error_status = 'error_14'
            return None
        self.all_indexed_paras = paras
        return self.all_indexed_paras

    @staticmethod
    def get_paragraph_count(indexed_paras):
        """For any dictionary of indexed text paragraphs, return the
        number of paragraphs.
        """
        para_count = 0
        for para in indexed_paras:
            para_count += 1
        return para_count

    @classmethod
    def get_para_samples(cls, indexed_paras):
        """For any dictionary of indexed paragraphs, return dictionaries
        of the first paragraph, last paragraph, and entire text while
        retaining the original paragraph numbers.
        """
        num_paras_in_range = cls.get_paragraph_count(indexed_paras)
        first_para = {}
        last_para = {}
        all_text = {}
        para_counter = 0
        for para_index, para in indexed_paras.items():
            para_counter += 1
            if para_counter == 1:
                first_para[para_index] = para
            if para_counter == num_paras_in_range:
                last_para[para_index] = para
            all_text[para_index] = para
        return first_para, last_para, all_text

    def test_search_range(self, search_range):
        """For a user-inputed search range, test its boundaries and
        ensure it will be valid when used to select a range of indexed
        paragraphs from a dictionary, then save as attributes both
        the original search range and a version containing a list of
        paragraph indexes in the range. In case of an invalid input,
        save the error code so the user knows what to change.
        """
        self.error_status = 'okay'
        num_paras = self.get_paragraph_count(self.all_indexed_paras)
        search_range = search_range.lower()
        # search_range should accept "1-5" but also "start-6", "8-end",
        # etc. Each value should be a paragraph by number, not by index.
        if search_range == 'all' or search_range == 'start-end':
            self.search_range_str = search_range
            self.search_range_list = list(range(0,num_paras))
            return self.search_range_str
        try:
        # This checks to see if the range input is a single integer.
            lone_para = int(search_range)
        except:
            pass
        else:
            if 0 < lone_para <= num_paras:
                self.search_range_str = search_range
                self.search_range_list = [lone_para -1]
                return self.search_range_str
            else:
                self.error_status = 'error_4'
                return None
        if not re.search('.-.',search_range):
            self.error_status = 'error_5'
            return None
        split_range = search_range.split('-')
        # This block makes sure exactly two values were given.
        if len(split_range) != 2:
            self.error_status = 'error_6'
            return None
        # This block checks that the first value is "start" or a
        # positive integer.
        if split_range[0] == 'start':
            p_num_start = 1
        else:
            try:
                p_num_start = int(split_range[0])
            except:
                self.error_status = 'error_7'
                return None
        if not p_num_start > 0:
            self.error_status = 'error_7'
            return None
        # This block checks that the second value is "end" or a positive
        # integer.
        if split_range[1] == 'end':
            p_num_end = num_paras
        else:
            try:
                p_num_end = int(split_range[1])
            except:
                self.error_status = 'error_8'
                return None
        if not p_num_end > 0:
            self.error_status = 'error_8'
            return None
        # This block checks that the "end" value is greater than the
        # "start" value, and that the values are both within the
        # expected range, and finally saves the confirmed range as
        # a class attribute.
        if p_num_end < p_num_start:
            self.error_status = 'error_9'
            return None
        elif p_num_start > num_paras:
            self.error_status = 'error_10'
            return None
        elif p_num_end > num_paras:
            self.error_status = 'error_11'
            return None
        elif p_num_start == p_num_end:
            self.search_range_str = search_range
            self.search_range_list = [p_num_start -1]
            return self.search_range_str
        else:
            self.search_range_str = search_range
            self.search_range_list = list(range(p_num_start -1, p_num_end))
            return self.search_range_str

    def get_paras_in_range(self):
        """For a dictionary of indexed paragraphs and a prior-approved
        search range, return a dictionary of only the paragraphs in the
        range.
        """
        self.error_status = 'okay'
        paras_in_range = {}
        for p_index, para in self.all_indexed_paras.items():
            if p_index in self.search_range_list:
                paras_in_range[p_index] = para
        if not paras_in_range:
            self.error_status = 'error_12'
            return None
        else:
            return paras_in_range

    def split_paragraphs(self,indexed_paras):
        """For any dictionary of indexed paragraphs, return a list of
        paragraphs where each item is a dictionary containing paragraph
        contents and details.
        """
        self.error_status = 'okay'
        split_paras_in_range = []
        # This block finds any hyphens, dashes, or underscores in a
        # paragraph, then adds a space behind them so split() can break
        # the hyphenated words apart cleanly.
        for p_index, para in indexed_paras.items():
            for cha in dashes:
                if cha in para:
                    para = para.replace(cha, cha+' ')
            split_para = para.split()
            w_index = -1
            # This takes a word count of every paragraph.
            for word in split_para:
                w_index += 1
            detailed_para = {
            'index': p_index,
            'highest_index': w_index,
            'text_str': para,
            'split_text': split_para,
            }
            split_paras_in_range.append(detailed_para)
        if not split_paras_in_range:
            self.error_status = 'error_13'
            return None
        else:
            return split_paras_in_range

    @staticmethod
    def search_text_for_target_words(list_of_paras, targ_words):
        """Receive a list of dictionaries representing paragraphs,
        search each paragraph for target words, compile each instance
        in a dictionary with relevant information, and return a list of
        those dictionaries.
        """
        matched_words = []
        found_match = False
        # This goes over each paragraph's dictionary and relabels its
        # key-value pairs.
        for para in list_of_paras:
            para_index = para['index']
            para_wc = para['highest_index']
            para_text = para['text_str']
            para_split = para['split_text']
            # This strips each word of punctuation then compares it to
            # every word in the target list. If a word matches, a
            # dictionary of its information is saved.
            w_index = -1
            for word in para_split:
                w_index += 1
                word_stripped = word.lower().strip(punctuation_plus)
                # All target categories are looped through, as are all
                # targets in each category.
                for category, targs in targ_words.items():
                    for t_word, description in targs.items():
                    # Words with iterations (like verb forms) have been
                    # stored so that each dictionary key is a tuple of
                    # all iterations.
                        if isinstance(t_word, tuple):
                            for item in t_word:
                                if word_stripped == item or word_stripped == \
                                item+'s':
                                    found_match = True
                                    break
                        # Words with no iterations are stored so that
                        # each dictionary key is a string of the word.
                        else:
                            if word_stripped == t_word or word_stripped == \
                            t_word+'s':
                                found_match = True
                        if found_match:
                            matched_item = {
                            'para_index': para_index,
                            'para_word_count': para_wc,
                            'split_para_text': para_split,
                            'type': 'word',
                            'targ': t_word,
                            'word_index': w_index,
                            'category': category,
                            'description': description,
                            }
                            matched_words.append(matched_item)
                            found_match = False
                            break
        return matched_words

    @staticmethod
    def search_text_for_target_phrases(list_of_paras, targ_phrases):
        """Receive a list of dictionaries representing paragraphs,
        search each paragraph for target phrases, compile each instance
        in a dictionary with relevant information, and return a list of
        those dictionaries.
        """
        matched_phrases = []
        # This goes over each paragraph's dictionary and relabels its
        # key-value pairs.
        for para in list_of_paras:
            para_index = para['index']
            para_wc = para['highest_index']
            para_text = para['text_str']
            para_split = para['split_text']
            # This looks at every target phrase and takes its word
            # count, then goes over the paragraph word by word and
            # builds a sequence of words the same length as the target.
            for category, targs in targ_phrases.items():
                # For every target phrase, if the phrase is stored as a
                # tuple of different phrase iterations, each iteration
                # is considered.
                for t_phrase, description in targs.items():
                    if isinstance(t_phrase, tuple):
                        for tp_iter in t_phrase:
                            phrase_length = len(tp_iter.split())
                            w_index = -1
                            # This block detects the last word it should
                            # use to startbuilding a sequence; sequences
                            # that would extend past the length of the
                            # paragraph are not created.
                            for word in para_split:
                                w_index += 1
                                seq_last_index = w_index + phrase_length -1
                                # If a sequence is approved, this block
                                # takes a slice of words starting at the
                                # current word's index and equal in
                                # length to the target phrase.
                                if seq_last_index <= para_wc:
                                    x = \
                                    para_split[w_index:seq_last_index +1]
                                    sequence = ' '.join(x)
                                    sequence = sequence.strip(punctuation_plus)
                                else:
                                    sequence = ''
                                # If the resulting sequence matches the
                                # target phrase, the match's information
                                # is stored.
                                if sequence.lower() == tp_iter:
                                    matched_item = {
                                    'para_index': para_index,
                                    'para_word_count': para_wc,
                                    'split_para_text': para_split,
                                    'type': 'phrase',
                                    'targ': t_phrase,
                                    'targ_iter': tp_iter,
                                    'word_index': w_index,
                                    'last_word_index': seq_last_index,
                                    'category': category,
                                    'description': description,
                                    }
                                    matched_phrases.append(matched_item)
                    # The phrase search is performed on non-tuple
                    # entries as well as tuples of phrase iterations.
                    else:
                        phrase_length = len(t_phrase.split())
                        w_index = -1
                        for word in para_split:
                            w_index += 1
                            seq_last_index = w_index + phrase_length -1
                            if seq_last_index<=para_wc:
                                x = para_split[w_index:seq_last_index +1]
                                sequence = ' '.join(x)
                                sequence = sequence.strip(punctuation_plus)
                            else:
                                sequence = ''
                            if sequence.lower() == t_phrase:
                                matched_item = {
                                'para_index': para_index,
                                'para_word_count': para_wc,
                                'split_para_text': para_split,
                                'type': 'phrase',
                                'targ': t_phrase,
                                'word_index': w_index,
                                'last_word_index': seq_last_index,
                                'category': category,
                                'description': description,
                                }
                                matched_phrases.append(matched_item)
        return matched_phrases


class TargetList():
    """A class to contain a collection of proofreading targets gathered
    from predefined and user-defined values, altered by user
    preferences.
    """
    def __init__(self, categories):
        """Initialize attributes of a constructed list of proofreading
        targets. The categories attribute should be set to either 'all'
        or 'enabled'.
        """
        self.categories = categories
        self.targs = {}

    @staticmethod
    def build_dict_of_all_targs():
        """Return sorted dictionaries of all available targets,
        including user-defined, labelled by category.
        """
        all_targs = {}
        for cat, targs in targets.predefined.items():
            all_targs[cat] = targs
        for cat, targs in user_defined.items():
            all_targs[cat] = targs
        return all_targs

    @staticmethod
    def build_dict_of_enabled_targs():
        """Return a dictionary of targets corresponding to the
        categories that have been enabled, labelled by category, then
        filter out targets that have been added to the disabled target
        list.
        """
        enabled_targs = {}
        enabled_filtered_targs = {}
        for cat, setting in toggle_settings.items():
            if setting == 'Yes':
                if cat in predefined_cats:
                    enabled_targs[cat] = targets.predefined[cat]
                elif cat in user_defined_cats:
                    enabled_targs[cat] = user_defined[cat]
        for cat, targs in enabled_targs.items():
            enabled_filtered_targs[cat] = {}
            for targ, desc in targs.items():
                if targ not in disabled_targs:
                    enabled_filtered_targs[cat][targ] = desc
        return enabled_filtered_targs

    def set_targets(self):
        """Build a dictionary of proofreading targets based on user
        settings and save it as a class attribute.
        """
        if self.categories == 'all':
            targ_dict = self.build_dict_of_all_targs()
        elif self.categories == 'enabled':
            targ_dict = self.build_dict_of_enabled_targs()
        else:
            raise Exception("Incorrect input. The categories string "\
            "provided should be either 'all' for targets in all target "\
            "categories, or 'enabled' for only the targets in user-enabled "\
            "categories.")
        self.targs = targ_dict

    def separate_target_words_and_phrases(self):
        """Receive a dictionary of targets sorted by category, then sort
        them into two different dictionaries based on whether they
        include target words or target phrases.
        """
        targ_words = {}
        targ_phrases = {}
        for cat, targs in self.targs.items():
            if cat.lower().endswith('words'):
                targ_words[cat] = targs
            elif cat.lower().endswith('phrases'):
                targ_phrases[cat] = targs
            else:
                raise Exception("You have an incorrectly named target "\
                "category.")
                return None
        return targ_words, targ_phrases


class ListOfMatches():
    """A class containing a list of matched words and phrases; an
    instance of DocToProofread receives a TargetList instance, then
    proofreads the document for targets on the TargetList.  Any matches
    found are output in an instance of ListOfMatches, which contains
    methods for displaying them based on user preference.
    """
    def __init__(self, matched_words, matched_phrases):
        """Initialize dictionaries of matches that are used as the
        class instance's attributes.
        """
        self.matched_words = matched_words
        self.matched_phrases = matched_phrases
        self.matches_ordered = []

    @staticmethod
    def format_matched_item(match_dict):
        """Take in a dictionary describing a word or phrase that matches
        a target, and return a dictionary of the word or phrase quoted
        from the text, along with relevant information.
        """
        # This block assigns more convenient names to dictionary values.
        targ_type = match_dict['type']
        targ = match_dict['targ']
        word_list = match_dict['split_para_text']
        p_index = match_dict['para_index']
        para_length = match_dict['para_word_count']
        description = match_dict['description']
        category = match_dict['category']
        w_index = match_dict['word_index']
        # Matched phrases have a "first" and a "last" word; for matched
        # words, the match is treated as both the "first" and "last".
        if targ_type == 'word':
            lw_index = w_index
        elif targ_type == 'phrase':
            lw_index = match_dict['last_word_index']
        # This block defines a matched word or phrase and the three
        # words before (be) and after (af) it, to be displayed as if the
        # function were quoting the provided text.
        preface = ''
        if w_index -4 >= 0:
            preface = '…'
        word_3_be = ''
        if w_index -3 >= 0:
            word_3_be = word_list[w_index -3] + ' '
        word_2_be = ''
        if w_index -2 >= 0:
            word_2_be = word_list[w_index -2] + ' '
        word_1_be = ''
        if w_index -1 >= 0:
            word_1_be = word_list[w_index -1] + ' '
        # The matched item is quoted from the text as a slice of words,
        # rejoined.
        if targ_type == 'word':
            matched_item = f"{word_list[w_index]}"
        elif targ_type == 'phrase':
            matched_item = ' '.join(word_list[w_index:lw_index +1])
        word_1_af = ''
        if lw_index +1 <= para_length:
            word_1_af = ' ' + word_list[lw_index +1]
        word_2_af = ''
        if lw_index +2 <= para_length:
            word_2_af = ' ' + word_list[lw_index +2]
        word_3_af = ''
        if lw_index +3 <= para_length:
            word_3_af = ' ' + word_list[lw_index +3]
        # If the text keeps going after word_3_af, its trailing
        # punctuation is stripped and an ellipsis is added.
        ending = ''
        if w_index +4 <= para_length:
            word_3_af = word_3_af.rstrip(trailing_punct)
            ending = '…'
        quote = f"\'{preface}{word_3_be}{word_2_be}{word_1_be}"\
        f"{matched_item}{word_1_af}{word_2_af}{word_3_af}{ending}\'"
        # An earlier block added a space after each dash or hyphen for
        # easy paragraph splitting; this block removes the extra spaces
        # for attractive display.
        for cha in dashes:
            cha_spaced = cha + ' '
            if cha_spaced in quote:
                quote = quote.replace(cha_spaced, cha)
        return p_index, targ, quote, category, description

    def sort_matches(self):
        """Take in lists of dictionaries describing words and phrases
        from text that match targets, and return a single list of
        matches sorted by order of appearance (by paragraph index, then
        by word index).
        """
        all_matches = self.matched_words + self.matched_phrases
        # If no matches were found, this function ends early and returns
        # the empty list.
        if not all_matches:
            return all_matches
        all_matches_ordered = []
        para_word_counts = {}
        counter = 0
        for match in all_matches:
            para_word_counts[match['para_index']] = match['para_word_count']
        highest_p_index = max(para_word_counts.keys())
        for p_index in range(0, highest_p_index +1):
            if p_index in para_word_counts.keys():
                word_count = para_word_counts[p_index]
                for w_index in range(0, word_count +1):
                    for match in all_matches:
                        if match['para_index'] == p_index and \
                        match['word_index'] == w_index:
                            all_matches_ordered.append(match)
        self.matches_ordered = all_matches_ordered
        return all_matches_ordered

    def find_common_matches(self):
        """For a list of dictionaries containing quotes that match
        targets, count each match and, if a target was matched five or
        more times, sort the match dictionary and all dictionaries with
        the same target into a separate list. Return the new list and
        the original (sans the entries that were removed from it).
        """
        list_of_matches = self.matches_ordered[:]
        common_matches = []
        list_indexes_to_remove = []
        targs_checked = []
        index = -1
        for match in list_of_matches:
            index += 1
            # If the current match's target has not yet been checked
            # for commonness, this block makes that check.
            if match['targ'] not in targs_checked:
                matched_targ = match['targ']
                # This block checks a target's appearances to see if
                # it appears more than five times.
                a_count = 0
                for match_2 in list_of_matches:
                    if match_2['targ'] == matched_targ:
                        a_count += 1
                # The target is added to targs_checked whether it is
                # common or not.
                targs_checked.append(matched_targ)
                # If the target is found to be common, the match's info
                # and the target are saved in a new dictionary c_match,
                # which is added to the list common_matches.
                if a_count >= 5:
                    c_match = {}
                    c_match['category'] = match['category']
                    c_match['targ'] = matched_targ
                    if isinstance(matched_targ,tuple):
                        c_match['sort_name'] = matched_targ[0]
                    else:
                        c_match['sort_name'] = matched_targ
                    c_match['description'] = match['description']
                    c_match['instances'] = []
                    c_match['instances'].append(match)
                    common_matches.append(c_match)
                    list_indexes_to_remove.append(index)
            # If the current match's target has already been checked,
            # this block compares it to the targets found to be common,
            # and if the target is represented in that list, the current
            # match is saved as an instance of that target.
            else:
                for c_match in common_matches:
                    if match['targ'] == c_match['targ']:
                        c_match['instances'].append(match)
                        list_indexes_to_remove.append(index)
        # This block deletes from list_of_matches all matches whose
        # targets are common; uncommon matches are left in
        # list_of_matches.
        for index in reversed(list_indexes_to_remove):
            del list_of_matches[index]
        # This block sorts the common matches by their "sort_name", the
        # first word of their target name.
        if common_matches:
            common_matches = sorted(common_matches, key = lambda c_match: \
            c_match['sort_name'])
        return common_matches, list_of_matches

    @classmethod
    def display_common_matches(cls, list_of_common_matches):
        """For a list of common matches found from proofreading a
        document, display each commonly matched target and a quote of
        each of its appearances, sorted by category.
        """
        print_wrapped(2, "Common Targets (5+ Occurrences) Found")
        if list_of_common_matches:
            previous_cat = ''
            for cat in all_cats_list:
                for c_match in list_of_common_matches:
                    if cat == c_match['category']:
                        if previous_cat != cat:
                            print_wrapped(1, cat)
                        targ = c_match['targ']
                        if isinstance(targ,tuple):
                            tuple_str = ''
                            for item in targ:
                                tuple_str += f"\"{item}\"" + ', '
                            print_wrapped(12, tuple_str)
                        else:
                            print_wrapped(12, f"\"{targ}\"")
                        print_wrapped(4, c_match['description'])
                        print()
                        for inst in c_match['instances']:
                            p_index, x, quote, x, description = \
                                cls.format_matched_item(inst)
                            print_wrapped(
                                4, f"Paragraph {p_index +1}",
                                5, quote)
                        previous_cat = cat
        else:
            print_wrapped(12, "(None)")

    @classmethod
    def display_matches_by_category(cls, ordered_matches, common):
        """Take in a list of dictionaries describing words and phrases
        from text that match targets, sort them by cateogry, and display
        each match with relevant information.
        """
        # The boolean input common declares whether the function
        # display_common_matches() was used immediately prior to this
        # function.
        if common:
            print_wrapped(2, "Uncommon Targets Found, By Category")
        else:
            print_wrapped(2, "Targets Found, By Category")
        for cat in all_cats_list:
            print_wrapped(1, cat)
            prev_p_index = ''
            category_present = False
            for match in ordered_matches:
                if cat == match['category']:
                    category_present = True
                    p_index, targ, quote, x, description = \
                        cls.format_matched_item(match)
                    if p_index != prev_p_index:
                        print_wrapped(12, f"Paragraph {p_index +1}")
                    else:
                        print()
                    # Normally I would use convert_tuple_to_str(), but
                    # in this instance, the output targets need to have
                    # quotes around each iteration.
                    if isinstance(targ,tuple):
                        tuple_str = ''
                        for item in targ:
                            tuple_str += f"\"{item}\"" + ', '
                        print_wrapped(4, tuple_str)
                    else:
                        print_wrapped(4, f"\"{targ}\"")
                    print_wrapped(
                        4, quote,
                        5, description)
                    prev_p_index = p_index
            if not category_present:
                print_wrapped(12, "(None)")

    @classmethod
    def display_matches_by_appearance(cls, ordered_matches, common):
        """Take in a list of dictionaries describing words and phrases
        from text that match targets, and display each match with
        relevant information.
        """
        # The boolean input common declares whether the function
        # display_common_matches() was used immediately prior to this
        # function.
        if common:
            print_wrapped(2, "Uncommon Targets Found, By Appearance")
        else:
            print_wrapped(2, "Targets Found, By Appearance")
        prev_p_index = ''
        if not ordered_matches:
                print_wrapped(12, "(None)")
        for match in ordered_matches:
            p_index, targ, quote, category, description = \
                cls.format_matched_item(match)
            if p_index != prev_p_index:
                print_wrapped(1, f"Paragraph {p_index +1}")
            else:
                print()
            print_wrapped(3, quote)
            # Normally I would use convert_tuple_to_str(), but
            # in this instance, the output targets need to have
            # quotes around each iteration.
            if isinstance(targ,tuple):
                tuple_str = ''
                for item in targ:
                    tuple_str += f"\"{item}\"" + ', '
                print_wrapped(4, tuple_str)
            else:
                print_wrapped(4, f"\"{targ}\"")
            print_wrapped(4, category,
            5, description)
            prev_p_index = p_index
