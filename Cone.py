import adsk.core, adsk.fusion, adsk.cam

app = adsk.core.Application.get()
ui = app.userInterface

def run(context):
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        
        baseRadius = 10.0  
        height = 20.0  

        sketches = rootComp.sketches
        yzPlane = rootComp.yZConstructionPlane
        sketch = sketches.add(yzPlane)
        
        lines = sketch.sketchCurves.sketchLines
        point1 = adsk.core.Point3D.create(0, 0, 0)
        point2 = adsk.core.Point3D.create(0, height, 0)  
        point3 = adsk.core.Point3D.create(0, 0, baseRadius)  
        
        line1 = lines.addByTwoPoints(point1, point2)
        line2 = lines.addByTwoPoints(point2, point3)
        line3 = lines.addByTwoPoints(point3, point1)  
        
        prof = sketch.profiles.item(0)
    
        revolves = rootComp.features.revolveFeatures
        revInput = revolves.createInput(prof, line1,adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        angle = adsk.core.ValueInput.createByReal(360) 
        revInput.setAngleExtent(False, angle)
        
        revolves.add(revInput)
        
        ui.messageBox('Cone is created successfully')

    except Exception as e:
        ui.messageBox('Failed: {}'.format(e))
