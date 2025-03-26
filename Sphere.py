import adsk.core, adsk.fusion, adsk.cam

app = adsk.core.Application.get()
ui = app.userInterface

def run(context):
    try:
       product = app.activeProduct
       design = adsk.fusion.Design.cast(product)
       rootComp = design.rootComponent

       sketches = rootComp.sketches
       xzPlane = rootComp.xZConstructionPlane
       sketch = sketches.add(xzPlane)
       
       radius = 10.0

       sphere = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), radius)
       
       axisLine = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(-radius,0,0), adsk.core.Point3D.create(radius,0,0))

       prof = sketch.profiles.item(0)

       revolves = rootComp.features.revolveFeatures
       revInput = revolves.createInput(prof, axisLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
       angle = adsk.core.ValueInput.createByReal(360)
       revInput.setAngleExtent(False,angle)

       revolves.add(revInput)

       ui.messageBox("Sphere was created successfully")

    except Exception as e:
        ui.messageBox('Failed: {}'.format(e))
