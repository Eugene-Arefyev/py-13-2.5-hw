import os
import subprocess

def get_process_dir_abs_path():
    process_dir_rel_path = os.path.dirname(__file__)
    process_dir_abs_path = os.path.abspath(process_dir_rel_path)

    return process_dir_abs_path


def check_filetype(filetype):
    def check(filename):
        return filetype in filename

    return check


def get_picture_names_list_form_dir(source_path):
    file_names_list = os.listdir(source_path)
    filtered_jpg_files = filter(check_filetype('.jpg'), file_names_list)

    return list(filtered_jpg_files)


# def save_picture(picture_path_with_name):
#     def save(pic_data):
#         with open(picture_path_with_name, 'wb') as new_pic:
#             for bin in pic_data:
#                 new_pic.write(bin)
#
#     return save


def convert_pictures(sources_dir_path, picture_names_list):
    config = {
        'flag': '-resize',
        'size_param': '200'
    }

    for picture_name in picture_names_list:
        picture_path = os.path.join(sources_dir_path, picture_name)
        source_pic_name = picture_name.split('.')
        output_pic_name = ''.join([source_pic_name[0], config['flag'], config['size_param'], '.', source_pic_name[1]])
        result_file_path = os.path.join('Result', output_pic_name)

        subprocess.run(['convert', picture_path, config['flag'], config['size_param'], result_file_path])

        # with open(picture_path) as pic:
        #     subprocess.run(['convert.exe', ])

# e = subprocess.run(['python', 'process_example.py'])
# print('#########')
# print(type(e))
# print(e)
# print('Программа напечатала:')
# print(e.stdout)
# print('Код возврата: ', e.returncode)


if __name__ == '__main__':
    process_dir_abs_path = get_process_dir_abs_path()

    sources_dir_name = 'Source'
    sources_dir_path = os.path.join(process_dir_abs_path, sources_dir_name)

    picture_names_list = get_picture_names_list_form_dir(sources_dir_path)

    convert_pictures(sources_dir_path, picture_names_list)

    # print(picture_names_list)