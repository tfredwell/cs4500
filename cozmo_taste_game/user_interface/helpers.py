import wx


def scale_image(bitmap: wx.Bitmap, width, height=None) -> wx.Bitmap:
    image = bitmap.ConvertToImage()
    if height is None:
        height = width
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    return wx.Bitmap(image)


def load_image(image_file_name, width=None, height=None):
    from os import path
    resource_path = path.abspath(path.join(path.dirname(__file__), image_file_name))

    image = wx.Bitmap(resource_path, wx.BITMAP_TYPE_ANY)

    size = width or height
    if size is not None:
        width = size or width
        height = size or height
        image = scale_image(image, width, height)
    return image


def del_items(number, *args):
    for i in range(0, number):
        del args[i]
    return args
