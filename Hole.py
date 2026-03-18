import adsk.core, adsk.fusion, adsk.cam

app = adsk.core.Application.get()
ui = app.userInterface


def create_hole(rootComp, holePoint, holeDiameter, holeDepth):
    try:
        targetBody = rootComp.bRepBodies.item(0)
        faces = targetBody.faces
        face = None
        # Find the closest face to the given point
        minDistance = float('inf')
        for i in range(faces.count):
            tempFace = faces.item(i)
            tempPoint = tempFace.pointOnFace
            distance = tempPoint.distanceTo(holePoint)
            if distance < minDistance:
                face = tempFace
                minDistance = distance

        sketches = rootComp.sketches
        sketch = sketches.add(face)

        sketchPoints = sketch.sketchPoints
        sketchPoint = sketchPoints.add(holePoint)
        holePoints = adsk.core.ObjectCollection.create()
        holePoints.add(sketchPoint)
        holeFeats = rootComp.features.holeFeatures
        holeInput = holeFeats.createSimpleInput(adsk.core.ValueInput.createByReal(holeDiameter))

        holeInput.setPositionBySketchPoints(holePoints)
        holeInput.setDistanceExtent(adsk.core.ValueInput.createByReal(holeDepth))
        holeFeats.add(holeInput)
        ui.messageBox('Hole created successfully!')

    except Exception as e:
        ui.messageBox(f'Failed to create hole: {str(e)}')


def run(context):
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent

        sketches = rootComp.sketches
        xzPlane = rootComp.xZConstructionPlane
        sketch = sketches.add(xzPlane)

        length = 10.0
        width = 10.0
        height = 3.0

        square = sketch.sketchCurves.sketchLines.addCenterPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(length / 2, width / 2, 0)
        )

        prof = sketch.profiles.item(0)

        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(height)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)

        holePoint = adsk.core.Point3D.create(0, 0,0) 
        holeDiameter = 5.0 
        holeDepth = 3.0  

        create_hole(rootComp, holePoint, holeDiameter, holeDepth)

    except Exception as e:
        ui.messageBox('Failed: {}'.format(e))

