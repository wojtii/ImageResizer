import click
import cv2
import os
# build project by running: pyinstaller resizer.py -F
extensions3l = ['jpg', 'png', 'bmp', 'tif']
extensions4l = ['jpeg', 'tiff']
curr_path = os.getcwd()
default_folder = 'resized'


def validate_extension(ext):
    if ext in extensions3l or ext in extensions4l:
        return True
    return False


def change_img_ext(img_name, ext):
    l = img_name.split('.')
    l[-1] = '.' + ext
    return ''.join(l)


def get_all_images(path):
    ls = os.listdir(path)
    return [file for file in ls if file[-3:] in extensions3l or file[-4:] in extensions4l]


def resize(img_name, path, result_folder, k=None, width=None, height=None, ext=None):
    img_path = os.path.join(path, img_name)
    img = cv2.imread(img_path)
    if k is None:
        res = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    else:
        res = cv2.resize(img, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC)
    folder = os.path.join(path, result_folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if ext is None:
        folder = os.path.join(folder, img_name)
    else:
        folder = os.path.join(folder, change_img_ext(img_name, ext))
    cv2.imwrite(folder, res)


def exe(k=None, width=None, height=None, path=None, folder=None, ext=None):
    if path is None:
        path = curr_path
    if folder is None:
        folder = default_folder
    image_names = get_all_images(path)
    if not image_names:
        print('No images found in folder: {}'.format(path))
        return
    for file in image_names:
        resize(file, path, folder, k=k, width=width, height=height, ext=ext)



@click.command()
@click.option('--fsize', is_flag=True, help='Add this flag to set resizing mode to fixed size')
@click.option('--path', is_flag=True, help='Add this flag to choose path')
@click.option('--folder', is_flag=True, help='Add this flag to choose result folder')
@click.option('--ext', is_flag=True, help='Add this flag to change result extension')
def main(fsize, path, folder, ext):
    if path:
        path = click.prompt('Please specify path', type=str)
        if not os.path.exists(path):
            print("Path does not exists")
            return
    else:
        path = None
    if folder:
        folder = click.prompt('Please specify result folder', type=str)
    else:
        folder = None
    if ext:
        ext = click.prompt('Please specify an extension', type=str)
        if not validate_extension(ext):
            print('Not supported extension')
            return
    else:
        ext = None
    if fsize:
        width = click.prompt('Please enter a valid image width', type=int)
        height = click.prompt('Please enter a valid image height', type=int)
        exe(width=width, height=height, path=path, folder=folder, ext=ext)
    else:
        k = click.prompt('Please enter an image coefficient', type=float)
        if k <= 0:
            print('Invalid parameter')
            return
        exe(k=k, path=path, folder=folder, ext=ext)


if __name__ == '__main__':
    main()
