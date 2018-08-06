#normal test: pytest resizer_test.py, coverage test: pytest --cov=../resizer/ --cov-report term-missing
#cover 99%, missing only if main statement
import resizer
import os
import cv2
import numpy as np
import shutil
from click.testing import CliRunner


def test_change_img_ext():
    assert "abc.jpg" == resizer.change_img_ext("abc.png", "jpg")
    assert "1234.bmp" == resizer.change_img_ext("1234.jpeg", "bmp")
    assert ".tif" == resizer.change_img_ext(".jpg", "tif")


def test_validate_extension():
    assert True == resizer.validate_extension('jpg')
    assert True == resizer.validate_extension('png')
    assert False == resizer.validate_extension('jpgd')
    assert False == resizer.validate_extension('raw')
    assert False == resizer.validate_extension('nef')


def test_get_all_images():
    path = os.getcwd()
    assert 0 < len(resizer.get_all_images(path))
    assert 0 == len(resizer.get_all_images('/'))


def test_exe_and_resize():
    curr_path = os.getcwd()
    img1 = np.zeros((400, 400, 3), np.uint8)
    img2 = np.zeros((1920, 1080, 3), np.uint8)
    img3 = np.zeros((2000, 1500, 1), np.uint8)
    cv2.imwrite(os.path.join(curr_path, 'img1.jpg'), img1)
    cv2.imwrite(os.path.join(curr_path, 'img2.jpg'), img2)
    cv2.imwrite(os.path.join(curr_path, 'img3.jpg'), img3)
    res_path = os.path.join(curr_path, 'resized_test1')
    res_path2 = os.path.join(curr_path, 'resized_test2')
    resizer.exe(k=0.5, folder=res_path, ext='png')
    resizer.exe(width=1920, height=1080, folder=res_path2)
    resizer.exe(width=1920, height=1080, path='/home')

    assert True == os.path.exists(res_path)
    assert [] != os.listdir(res_path)
    img = cv2.imread(os.path.join(res_path, 'img2.png'))
    assert 0 != len(img)

    os.remove('img1.jpg')    
    os.remove('img2.jpg')    
    os.remove('img3.jpg')    
    shutil.rmtree(res_path)
    shutil.rmtree(res_path2)


def test_click_errors():
    runner = CliRunner()

    result = runner.invoke(resizer.main, ['--ext', '--folder'], input='test\nppp')
    assert result.output.endswith('Not supported extension\n')

    result = runner.invoke(resizer.main, ['--path'], input='/33dm3')
    assert result.output.endswith('Path does not exists\n')

    result = runner.invoke(resizer.main, input='-1')
    assert result.output.endswith('Invalid parameter\n')


def test_click():
    runner = CliRunner()

    curr_path = os.getcwd()
    img1 = np.zeros((400, 400, 3), np.uint8)
    cv2.imwrite(os.path.join(curr_path, 'img1.jpg'), img1)    
    result = runner.invoke(resizer.main, ['--fsize', '--folder'], input='rrr\n100\n100')
    assert 'rrr' in os.listdir(curr_path)

    result = runner.invoke(resizer.main, ['--folder'], input='rrrr\n 0.5')
    assert 'rrrr' in os.listdir(curr_path)

    os.remove('img1.jpg')
    shutil.rmtree('rrr')
    shutil.rmtree('rrrr')
