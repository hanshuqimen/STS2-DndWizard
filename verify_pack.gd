extends SceneTree
func _initialize():
    var args = OS.get_cmdline_user_args()
    if not ProjectSettings.load_resource_pack(args[0]):
        quit(1)
        return
    var failures = 0
    var jobs = JSON.parse_string(FileAccess.get_file_as_string(args[1]))
    var texture_paths = ["res://DndWizard/images/wizard.png"]
    for job in jobs:
        var normalized = job.output.replace("\\", "/")
        texture_paths.append("res://DndWizard/images/" + normalized.split("/images/")[1])
    for path in texture_paths:
        var tex = load(path)
        if tex == null or tex.get_width() <= 0: failures += 1
    for scene in ["wizard", "select", "icon"]:
        var resource = load("res://DndWizard/scenes/" + scene + ".tscn")
        if resource == null: failures += 1
        else:
            var node = resource.instantiate()
            node.free()
    print("PACK_TEXTURES=", texture_paths.size(), " PACK_SCENES=3 PACK_LOAD_FAILURES=", failures)
    if args.size() > 2:
        var report = FileAccess.open(args[2], FileAccess.WRITE)
        report.store_string(JSON.stringify({"scope":"standalone Godot resource check; no game process", "textures":texture_paths.size(), "scenes":3, "failures":failures}, "  "))
    quit(0 if failures == 0 else 2)
