from napari.types import ImageData, SurfaceData
from itertools import product
from magicgui import magic_factory

@magic_factory
def image_to_surface(image:ImageData, z_multiplier: float = 1.0) -> SurfaceData:

    import numpy as np
    from scipy import spatial

    x = np.arange(image.shape[0])
    y = np.arange(image.shape[1])
    points = np.stack(list(product(x, y)))
    z = np.array([image[pt[0], pt[1]] for pt in points]).flatten() * z_multiplier

    tri = spatial.Delaunay(points)

    points_mesh = np.zeros((points.shape[0], 3))
    points_mesh[:, 1:] = points
    points_mesh[:, 0] = -z

    return (points_mesh, tri.simplices)

if __name__ == '__main__':
    import tifffile as tf
    import napari

    image = tf.imread(r'C:\Users\johamuel\Desktop\output_NASADEM.tif')
    surf = image_to_surface(image, z_multiplier=0.25)

    viewer = napari.Viewer()
    viewer.add_surface(surf)
    viewer.
