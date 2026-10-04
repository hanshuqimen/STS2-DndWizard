extends SceneTree
func _initialize():
    var args = OS.get_cmdline_user_args()
    var jobs = JSON.parse_string(FileAccess.get_file_as_string(args[0]))
    for job in jobs:
        var image = Image.new()
        var err = image.load(job.source) if job.get("raster", false) else image.load_svg_from_string(FileAccess.get_file_as_string(job.source))
        if err != OK:
            push_error("Failed SVG: " + job.source)
            quit(1)
            return
        if job.get("raster", false):
            image.resize(512, 384, Image.INTERPOLATE_LANCZOS)
        if image.save_png(job.output) != OK:
            quit(2)
            return
    print("Prepared ", jobs.size(), " card illustrations and SVG icons.")
    quit()
