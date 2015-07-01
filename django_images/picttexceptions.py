class DjangoImagesException(Exception):
    pass


class ImageSizeError(DjangoImagesException):
    """
    Raised when the supplied image does not
    fit the intial size requirements
    """
    def __init__(self, actual_size, required_size):
        self.message = 'Votre image est trop petite. Taille de l\'image : %sx%s, Taille minimun requise : %sx%s' % (actual_size[0], actual_size[1], required_size[0], required_size[1])
        self.actual_size = actual_size
        self.required_size = required_size

    def __str__(self):
        return repr(self.message)


class URLError(DjangoImagesException):
    """
    Raised when the supplied image does not
    fit the intial size requirements
    """
    def __init__(self, message):
        self.message = 'message'

    def __str__(self):
        return repr(self.message)
