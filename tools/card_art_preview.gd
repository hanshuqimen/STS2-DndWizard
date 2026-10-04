extends SceneTree
func _initialize():
    var root = OS.get_cmdline_user_args()[0]
    var cards = JSON.parse_string(FileAccess.get_file_as_string(root + "/cards.json"))
    var manifest = []
    for page in range(ceili(cards.size() / 16.0)):
        var sheet = Image.create(1024, 768, false, Image.FORMAT_RGB8)
        sheet.fill(Color("101726"))
        for i in range(16):
            if page * 16 + i >= cards.size():
                break
            var card = cards[page * 16 + i]
            var source = root + "/DndWizard/images/cards/" + card.Id + ".png"
            var art = Image.load_from_file(source)
            if art == null or art.get_width() != 512 or art.get_height() != 384:
                push_error("Bad card art: " + source)
                quit(1)
                return
            art.resize(256, 192, Image.INTERPOLATE_LANCZOS)
            art.convert(Image.FORMAT_RGB8)
            sheet.blit_rect(art, Rect2i(0, 0, 256, 192), Vector2i((i % 4) * 256, (i / 4) * 192))
            manifest.append({"id":card.Id,"page":page+1,"row":i/4+1,"column":i%4+1,"size":[512,384],"path":source})
        sheet.save_png(root + "/test-results/card-art-page-" + str(page+1) + ".png")
    var file = FileAccess.open(root + "/test-results/card-art-qa.json", FileAccess.WRITE)
    file.store_string(JSON.stringify(manifest, "  "))
    print(str(cards.size()) + " independent card textures verified; contact sheets written.")
    quit()
