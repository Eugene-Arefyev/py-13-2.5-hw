from multiprocessing import Process
import subprocess
import os


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
    filtered_jpeg_files = filter(check_filetype('.jpeg'), file_names_list)
    filtered_png_files = filter(check_filetype('.png'), file_names_list)

    return [*list(filtered_jpg_files), *list(filtered_jpeg_files), *list(filtered_png_files)]


def make_dir(dir_name):
    new_dir_abs_path = os.path.join(get_process_dir_abs_path(), dir_name)

    if not os.path.exists(new_dir_abs_path):
        os.mkdir(dir_name)


def split_file_name_and_format(filename_with_format):
    filename_data = filename_with_format.split('.')
    return {'name': filename_data[0], 'format': filename_data[1]}


def join_args_to_string(*args):
    return ''.join([*args])


def convert_picture(sources_dir_path, source_picture_name):
    convert_config = {
        'action': '-resize',
        'size_param': '200'
    }
    result_dir_name = 'Result'
    make_dir(result_dir_name)

    source_picture_path = os.path.join(sources_dir_path, source_picture_name)
    source_pic_name_data = split_file_name_and_format(source_picture_name)

    output_pic_name = join_args_to_string(
        source_pic_name_data['name'],
        convert_config['action'],
        convert_config['size_param'],
        '.',
        source_pic_name_data['format']
    )
    output_pic_path = os.path.join(result_dir_name, output_pic_name)

    cmd = [
        'convert',
        convert_config['action'],
        convert_config['size_param'],
        source_picture_path,
        output_pic_path
    ]

    subprocess.run(cmd)


def create_multiprocess_convert(sources_dir_path, picture_names_list):
    process_list = list()

    for picture_name in picture_names_list:
        process = Process(target=convert_picture, args=(sources_dir_path, picture_name))
        process_list += [process]

    for process in process_list:
        process.start()
        process.join()


def core():
    sources_dir_name = 'Source'
    sources_dir_path = os.path.join(get_process_dir_abs_path(), sources_dir_name)

    picture_names_list = get_picture_names_list_form_dir(sources_dir_path)

    create_multiprocess_convert(sources_dir_path, picture_names_list)


if __name__ == '__main__':
    core()
