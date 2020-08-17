from . import poland
from qgis.core import QgsProject, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsGeometry, QgsRectangle


def isLayerInPoland(obrysLayer):
    """sprawdza czy geometria obrysu jest poprawna"""
    # definicja transformacji układu
    layerCrs = obrysLayer.sourceCrs()  # z warstwy
    crs4326 = QgsCoordinateReferenceSystem(4326)  # WGS84
    transform = QgsCoordinateTransform(layerCrs, crs4326, QgsProject.instance())

    feat = next(obrysLayer.getFeatures())
    geom_obrysLayer = feat.geometry()
    geom_obrysLayer.transform(transform)
    geom_poland = QgsGeometry.fromWkt(poland.wkt)
    return geom_obrysLayer.within(geom_poland)