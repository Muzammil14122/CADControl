import adsk.core, adsk.fusion, adsk.cam

app = adsk.core.Application.get()
ui = app.userInterface
design = app.activeProduct
rootComp = design.rootComponent

def run(context):
    try:
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        rectLines = sketch.sketchCurves.sketchLines
        rectLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(10, 10, 0)
        )

        prof = sketch.profiles.item(0)
        extrudes = rootComp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(10)
        extrudeInput.setDistanceExtent(False, distance)
        extrude = extrudes.add(extrudeInput)

        boxBody = extrude.bodies.item(0)

        for sketch in rootComp.sketches:
            sketch.isVisible = False

        edgeCollection = adsk.core.ObjectCollection.create()

        for i in range(boxBody.edges.count):
            edge = boxBody.edges.item(i)
            edgeCollection.add(edge)

        if edgeCollection.count == 0:
            raise Exception('Check extrusion or edge selection.')

        filletFeature = rootComp.features.filletFeatures
        filletInput = filletFeature.createInput()
        filletRadius = adsk.core.ValueInput.createByReal(2.0)
        filletInput.addConstantRadiusEdgeSet(edgeCollection, filletRadius, True)

        # Apply the fillet
        filletFeature.add(filletInput)

        ui.messageBox('Fillet applied successfully')


    except Exception as e:
        ui.messageBox(f'Failed: {str(e)}')

