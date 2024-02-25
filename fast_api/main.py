from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple

from shapely import unary_union
from shapely.geometry import Polygon, Point
from utils import reproject, de_epsg_selector

app = FastAPI()


class PolygonBoundary(BaseModel):
    type: str
    coordinates: List[List[Tuple[float, float]]]


class Feature(BaseModel):
    type: str
    geometry: PolygonBoundary


class MarketShareRequest(BaseModel):
    city_boundary: Feature
    points: List[Tuple[float, float]]


@app.post("/market-share/")
async def calculate_market_share(request: MarketShareRequest):
    buffer_radius = 500

    # Re-projecting the city boundary to utm
    city_boundary_data = request.city_boundary.geometry.coordinates
    city_boundary = Polygon(city_boundary_data[0])
    city_boundary_epsg = de_epsg_selector(city_boundary_data)
    city_boundary_reprojected = reproject(city_boundary, city_boundary_epsg)

    points_data = request.points
    buffer_geoms = []
    for point in points_data:
        # Re-projecting the points to utm
        epsg_point = de_epsg_selector(point)
        point_geom = Point(point)
        point_geom_reprojected = reproject(point_geom, epsg_point)

        # Check whether the points are inside the boundary or not
        if city_boundary_reprojected.intersects(point_geom_reprojected):
            buffer_geom = point_geom_reprojected.buffer(buffer_radius)
            buffer_geoms.append(buffer_geom)

    # Dissolve all the buffer geometries into a single geometry
    dissolved_buffer = unary_union(buffer_geoms)

    total_buffer_area = dissolved_buffer.area
    total_city_area = city_boundary_reprojected.area

    market_share = (total_buffer_area / total_city_area) * 100

    return {"market_share": round(market_share, 2)}
