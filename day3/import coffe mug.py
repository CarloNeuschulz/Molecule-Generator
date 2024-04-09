import c4d
import maxon
 
doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.
 
def main() -> None:
    repository = maxon.AssetInterface.GetUserPrefsRepository()
    maxon.AssetManagerInterface.LoadAssets(repository, [(maxon.Id("file_946664f43ff5e0c2"), "")])
 
 
if __name__ == '__main__':
    main()