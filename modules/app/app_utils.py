from qgis.core import QgsProject, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsRectangle


def isLayerInPoland(obrysLayer):
    """sprawdza czy geometria obrysu jest poprawna"""
    crs4326 = QgsCoordinateReferenceSystem(4326)  # WGS84
    layerCrs = obrysLayer.sourceCrs()  # z warstwy
    transform = QgsCoordinateTransform(
        layerCrs, crs4326, QgsProject.instance())

    layerExtent = obrysLayer.sourceExtent()
    layerExtent4326 = transform.transform(layerExtent)
    polandExtent4326 = QgsRectangle(
        14.0745211117, 49.0273953314, 24.0299857927, 54.8515359564)
    return polandExtent4326.intersects(layerExtent4326)