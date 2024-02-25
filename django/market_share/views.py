from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from market_share.utils import reproject, de_epsg_selector
from market_share.serializers import MarketShareRequestSerializer


class CalculateMarketShare(APIView):
    def post(self, request):
        serializer = MarketShareRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city_boundary_data = serializer.validated_data['city_boundary']['geometry']['coordinates']
        epsg_city = de_epsg_selector(city_boundary_data[0])
        city_boundary = Polygon(city_boundary_data[0])
        city_boundary_reprojected = reproject(city_boundary, epsg_city)

        points_data = serializer.validated_data['points']
        buffer_radius = 500
        buffer_geoms = []
        for point in points_data:
            print(point)
            epsg_point = de_epsg_selector(point[0])
            point_geom = Point(point)
            point_geom_reprojected = reproject(point_geom, epsg_point)

            if city_boundary_reprojected.intersects(point_geom_reprojected):
                buffer_geom = point_geom_reprojected.buffer(buffer_radius)
                buffer_geoms.append(buffer_geom)

        dissolved_buffer = unary_union(buffer_geoms)

        total_buffer_area = dissolved_buffer.area
        total_city_area = city_boundary_reprojected.area

        market_share = (total_buffer_area / total_city_area) * 100

        return Response({"market_share": round(market_share, 2)})
