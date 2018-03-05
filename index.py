import os
import subprocess
from multiprocessing import Process, Pipe

def get_process_dir_abs_path():
    process_dir_rel_path = os.path.dirname(__file__)

    return os.path.abspath(process_dir_rel_path)


def check_filetype(filetype):
    def check(filename):
        return filetype in filename

    return check


def get_picture_names_list_form_dir(source_path):
    file_names_list = os.listdir(source_path)
    filtered_jpg_files = filter(check_filetype('.jpg'), file_names_list)

    return list(filtered_jpg_files)


def save_picture(sources_dir_path, picture_name):
    config = {
        'action': '-resize',
        'size_param': '200'
    }

    picture_path = os.path.join(sources_dir_path, picture_name)

    source_pic_name = picture_name.split('.')
    output_pic_name = ''.join([source_pic_name[0], config['action'], config['size_param'], '.', source_pic_name[1]])
    # result_file_path = os.path.join(os.path.dirname(__file__), 'Result', output_pic_name)

    cmd = ['convert', config['action'], config['size_param'], picture_path, output_pic_name]

    subprocess.run(cmd)


def multiprocess_convert_pictures(sources_dir_path, picture_names_list):
    process_list = list()

    for picture_name in picture_names_list:
        process = Process(target=save_picture, args=(sources_dir_path, picture_name))

        process_list += [process]

    for process in process_list:
        process.start()
        process.join()


if __name__ == '__main__':
    process_dir_abs_path = get_process_dir_abs_path()

    sources_dir_name = 'Source'
    sources_dir_path = os.path.join(process_dir_abs_path, sources_dir_name)

    picture_names_list = get_picture_names_list_form_dir(sources_dir_path)

    multiprocess_convert_pictures(sources_dir_path, picture_names_list)
