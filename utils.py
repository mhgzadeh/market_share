import pyproj
from shapely.ops import transform


def de_epsg_selector(coordinates):
    if isinstance(coordinates, list):
        min_lon = min(coord[0] for coord in coordinates)[0]
    else:
        min_lon = coordinates[0]

    return '25832' if 6 <= min_lon < 12 else '25833'


def reproject(shapely_feature, utm_epsg):
    project = pyproj.Transformer.from_crs(
        "EPSG:4326", f"EPSG:{utm_epsg}", always_xy=True
    ).transform
    transformed_feature = transform(project, shapely_feature)

    return transformed_feature
