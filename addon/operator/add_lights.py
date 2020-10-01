import bpy

class gem_op_AddLights(bpy.types.Operator):
    """ Add a ring of lights to the scene! """

    bl_idname = "gem.add_lights"
    bl_label = "Add Lights"
    bl_options = { 'REGISTER', 'UNDO' }

    from bpy.props import IntProperty, FloatProperty
    radius: FloatProperty(name="Radius", default=1, min=1, max=100)
    height: FloatProperty(name="Height", default=1, min=0, max=10)
    count: IntProperty(name="Light Count", default=3, min=3, max=50)
    energy: IntProperty(name="Light Energy", default=1000, min=500, max=2500)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'radius')
        layout.prop(self, 'height')
        layout.prop(self, 'count')
        layout.prop(self, 'energy')

    def execute(self, context):
        import math

        lights = []

        for i in range(self.count):
            light = bpy.data.lights.new('Point', 'POINT')
            obj = bpy.data.objects.new("LightObject", light)

            angle = i * math.pi * 2 / self.count

            location = (
                math.cos(angle) * self.radius,
                math.sin(angle) * self.radius,
                self.height,
            )

            obj.location = location
            obj.data.energy = self.energy
            lights.append(obj)

        parent = bpy.data.collections["Lights"]
        empty = bpy.data.objects.new('Light Ring Empty', None)
        empty.location = (0, 0, 0)
        parent.objects.link(empty)

        for obj in lights:
            parent.objects.link(obj)
            obj.parent = empty


        return { 'FINISHED' }
