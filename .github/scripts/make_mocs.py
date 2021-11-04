import os.path

DIRECTORIES_TO_EXCLUDE = ['meta-notes', 'venv']  # Directories beginning '.' are also excluded


def make_moc_for_files(directory, files):
    output = ''
    for file in files:
        if not include_file(directory, file):
            continue
        output += make_line_for_file(directory, file)
    return output


def make_line_for_file(directory, file):
    link_name, extension = os.path.splitext(file)
    if extension != '.md':
        link_name += extension
    return make_link_line(directory, link_name)


def strip_parent_directories_from_directory(directory):
    # Ugly hack because all directory names start with '../../'
    result = directory.replace('../', '')
    if result == '..': # Even more horrible hack for files in root of repo
        result = ''
    return result


def make_link_line(directory, link_name):
    adjusted_direcory = strip_parent_directories_from_directory(directory)
    if len(adjusted_direcory) > 0:
        adjusted_direcory += '/'
    result = f'-  [[{adjusted_direcory}{link_name}|{link_name}]]\n'
    print(f'directory={directory}\nadjusted_direcory={adjusted_direcory}\nlink_name={link_name}\n=> {result}')
    return result


def include_directory(d):
    if d[0] == '.':
        return False
    return d not in DIRECTORIES_TO_EXCLUDE


def include_file(directory, file):
    if file_is_moc_for_directory(directory, file):
        return False
    return file[0] != '.'


def file_is_moc_for_directory(directory, file):
    is_moc_for_directory = file == moc_file_name_for_directory(directory)
    return is_moc_for_directory


def filter_directories(dirs):
    dirs[:] = [d for d in dirs if include_directory(d)]


def make_moc_for_sub_directories(directory, sub_directories):
    output = ''
    for sub_directory in sub_directories:
        if not include_directory(sub_directory):
            continue
        output += make_line_for_sub_directory(directory, sub_directory)
    return output


def moc_name_for_sub_directory(sub_directory):
    name = sub_directory
    if name == '..':
        name = 'hub'
    return '🗂️ ' + name


def moc_file_name_for_directory(root):
    directory_name = os.path.basename(root)
    return moc_name_for_sub_directory(directory_name) + ".md"


def moc_file_path_for_directory(root):
    moc_file_basename = moc_file_name_for_directory(root)
    moc_file_path = os.path.join(root, moc_file_basename)
    return moc_file_path


def make_line_for_sub_directory(directory, sub_directory):
    path = directory + '/' + sub_directory
    file = moc_name_for_sub_directory(sub_directory)
    return make_link_line(path, file)


def index_content_for_directory(root, dirs, files):
    result = ''
    result += '%% Zoottelkeeper: Beginning of the autogenerated index file list  %%\n'
    result += make_moc_for_sub_directories(root, sorted(dirs))
    result += make_moc_for_files(root, sorted(files))
    result += '%% Zoottelkeeper: End of the autogenerated index file list  %%\n'
    return result
