import requests
import staticmaps
import ujson as json
import cairo

def generate_map(coordinates: list):

    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)
    for pair in coordinates:
        pin = staticmaps.create_latlng(float(pair[0]), float(pair[1]))
        context.add_object(staticmaps.Marker(pin, color=staticmaps.GREEN, size=12))

    image = context.render_cairo(800, 500)
    image.write_to_png("static/maps/map.png")
    