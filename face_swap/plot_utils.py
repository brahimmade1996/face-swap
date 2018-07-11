import numpy as np

import cv2
from IPython.display import clear_output
from IPython.display import display
from PIL import Image


def plot_sample(images_a: list, images_b: list,
                predict_fun_a, predict_fun_b,
                tanh_fix=False, save_to: str=None, nb_test_imgs=14):
    """
    Plot comparison between original and generated images for the two given set of images and prediction functions
    :param images_a: list of images to use for generation
    :param images_b: list of images to use for generation
    :param predict_fun_a: function to generate sample results. Takes list of images and returns list of images
    :param predict_fun_b: function to generate sample results. Takes list of images and returns list of images
    :param tanh_fix: whether to realign prediction values to 0-1 scale before move to 256 RGB schema
    (needed if models output is generated by tanh activation function)
    :param save_to: if given save image to such filepath, otherwise simply display image
    :return:
    """
    # need even number of images to plot
    assert nb_test_imgs % 2 == 0
    test_a = images_a[0:nb_test_imgs]
    test_b = images_b[0:nb_test_imgs]

    figure_a = np.stack([
                        test_a,
                        predict_fun_a(test_a),
                        predict_fun_b(test_a),
                        ], axis=1)
    figure_b = np.stack([
                        test_b,
                        predict_fun_a(test_b),
                        predict_fun_b(test_b),
                        ], axis=1)
    figure = np.concatenate([figure_a, figure_b], axis=0)
    # we split images on two columns for each of the two sets
    figure = figure.reshape((2*2, nb_test_imgs//2) + figure.shape[1:])  # example shape: (4, 7, 3, 64, 64, 3)
    figure = stack_images(figure)

    if tanh_fix:
        figure = np.clip((figure + 1) * 255 / 2, 0, 255).astype('uint8')
    else:
        figure = np.clip(figure * 255, 0, 255).astype('uint8')

    if save_to:
        cv2.imwrite(save_to, figure)
    else:
        figure = cv2.cvtColor(figure, cv2.COLOR_BGR2RGB)
        #plt.imshow(figure)
        #plt.show()
        display(Image.fromarray(figure))
        # crashes in notebooks
        #cv2.imshow('', figure)
        #cv2.waitKey(0)


def stack_images(images):
    """
    Stack given images to a single image
    :param images:
    :return:
    """
    images_shape = np.array(images.shape)
    new_axes = get_transpose_axes(len(images_shape))
    new_shape = [np.prod(images_shape[x]) for x in new_axes]
    return np.transpose(images, axes=np.concatenate(new_axes)).reshape(new_shape)


def get_transpose_axes(num_axis):
    if num_axis % 2 == 0:
        y_axes = list(range(1, num_axis - 1, 2))
        x_axes = list(range(0, num_axis - 1, 2))
    else:
        y_axes = list(range(0, num_axis - 1, 2))
        x_axes = list(range(1, num_axis - 1, 2))
    return y_axes, x_axes, [num_axis - 1]
