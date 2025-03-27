import adsk.core, adsk.fusion, adsk.cam

# Get the fusion interface
app = adsk.core.Application.get()
ui = app.userInterface

def run(context):
    try:
        # Get the current active product 
        product = app.activeProduct
        # Converts the product into the Fusion 360 design that can be manipulated
        design = adsk.fusion.Design.cast(product)

        # Get the Root Component
        rootComp = design.rootComponent

        # Enables us to sketch
        sketches = rootComp.sketches
        # Get the XY Contruction
        xyPlane = rootComp.xYConstructionPlane
        # Start creating the sketch on the XY plane
        sketch = sketches.add(xyPlane)

        # Drawing the Circle
        Circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), 5 )
        
        # TO CREATE AN EXTRUSION FROM THE SKETCH
        # Retrives the First Profile
        prof = sketch.profiles.item(0)
        # Getting the extrude from the root component
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation) 
        distance = adsk.core.ValueInput.createByReal(30)
        extInput.setDistanceExtent(False, distance)
        extrude = extrudes.add(extInput) 
        # Added the fillet
        cylinderBody = extrude.bodies.item(0)

        for sketch in rootComp.sketches:
            sketch.isVisible = False

        edgeCollection = adsk.core.ObjectCollection.create()

        for i in range(cylinderBody.edges.count):
            edge = cylinderBody.edges.item(i)
            edgeCollection.add(edge)
        
        filletFeature = rootComp.features.filletFeatures
        filletInput = filletFeature.createInput()
        filletRadius = adsk.core.ValueInput.createByReal(2.0)
        filletInput.addConstantRadiusEdgeSet(edgeCollection,filletRadius,True)

        filletFeature.add(filletInput)

        ui.messageBox('Cylinder is Successfully Created!')

    except Exception as e:
        ui.messageBox('Failed: {}'.format(e))
        
