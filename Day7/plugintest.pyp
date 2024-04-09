import c4d


# Define the plugin class
class pluginTest(c4d.plugins.ObjectData):
    def __init__(self):
        super(pluginTest, self).__init__()

    def Init(self, node):
        return True

    def GetVirtualObjects(self, op, hierarchyhelp):
        return None

    def GetDDescription(self, node, description, flags):
        return True

# Register the plugin 
def main():
    c4d.plugins.RegisterObjectPlugin(id=123456, str="pluginTest", g=pluginTest)
    if __name__ == "__main__":
        main()