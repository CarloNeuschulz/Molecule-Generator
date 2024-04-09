import c4d

class MyPlugin(c4d.plugins.ObjectData):

    def __init__(self):
        super(MyPlugin, self).__init__()

    def Init(self, node):
        return True

    def GetVirtualObjects(self, op, hierarchyhelp):
        return None

    def GetDDescription(self, node, description, flags):
        return True

# Register the plugin
def RegisterPlugin():
    pluginID = 1234567  # Replace with your unique plugin ID
    pluginName = "Plugintest"  # Replace with your plugin name

    # Register the plugin with Cinema 4D
    return c4d.plugins.RegisterObjectPlugin(
        id=pluginID,
        str=pluginName,
        g=MyPlugin,
        description="",
        info=c4d.OBJECT_GENERATOR,
        icon=None
    )

# Main function
if __name__ == "__main__":
    RegisterPlugin()