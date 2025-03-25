import adsk.core, adsk.fusion, adsk.cam
# type: ignore
# Get the Fusion 360 application
app = adsk.core.Application.get()
ui = app.userInterface

def run(context):
    try:
        # Get the active product (design)
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        
        # Get the root component of the design
        rootComp = design.rootComponent
        
        # Create a new sketch on the XY plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        
        # Draw a rectangle
        lines = sketch.sketchCurves.sketchLines
        rect = lines.addCenterPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(5, 5, 0))
        
        # Create an extrusion from the sketch
        prof = sketch.profiles.item(0)
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(10)
        extInput.setDistanceExtent(False, distance)
        extrude = extrudes.add(extInput)
        
        ui.messageBox('Box created successfully!')

    except Exception as e:
        ui.messageBox('Failed: {}'.format(e))
