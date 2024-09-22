# Mapping formats to media types (for assets)
import pystac

__all__ = [
    'format_to_media_type',
    'cat_keywords',
]

format_to_media_type = {
    "geotiff": pystac.MediaType.GEOTIFF,
    "flatgeobuf": pystac.MediaType.FLATGEOBUF,
    "netcdf": "application/x-netcdf",
    "geopackage": pystac.MediaType.GEOPACKAGE,
    "shapefile": "application/x-shapefile",
    "geodatabase": "application/x-filegdb",
    "csv": "text/csv",
    "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "geoparquet": pystac.MediaType.PARQUET,
    "grib": "application/grib",
    "grib2": "application/grib2",
    "txt": pystac.MediaType.TEXT,
    "pbf": "application/x-protobuf",
    "ascii": "text/plain",
}

# Categories for keywords
cat_keywords = {
    "risk_data_type": ["hazard", "exposure", "vulnerability"],
    "subcategory": [
        "coastal flood",
        "fluvial flood",
        "pluvial flood",
        "drought",
        "snowstorm/blizzard",
        "heat wave",
        "cold wave",
        "tropical cyclone",
        "extratropical cyclone",
        "wildfire",
        "multi hazard",
        "population number",
        "demographics",
        "socioeconomic status",
        "adaptive capacity",
        "population vulnerability",
        "building footprints",
        "building characteristics",
        "infrastructure footprints",
        "infrastructure characteristics",
        "urban/built-up footprints",
        "urban/built-up characteristics",
        "land use/land cover footprints",
        "land use/land cover characteristics",
    ],
    "spatial_scale": ["(near-)global", "regional", "national", "subnational"],
    "reference_period": ["historical", "future", "historical & future"],
    "code": ["code available"],
}
