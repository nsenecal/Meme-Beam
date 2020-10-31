from flexx import flx


class Jank(flx.Widget):

    def init(self):
        with flx.VBox(flex=0):
            with flx.VBox(flex = 0):
                src = "https://www.designyourway.net/blog/wp-content/uploads/2019/05/iPad-Pro-wallpaper-54-700x700.jpg"
                self.img = flx.ImageWidget(flex=0, stretch=False,source=src)
                self.img.set_minsize(500, 500)
                self.img.set_maxsize(500, 500)
            with flx.HBox(flex=1):
                self.b1 = flx.Button(text="Yes")
                self.void = flx.Label()
                self.b2 = flx.Button(text="No")
                self.b1.set_maxsize(40, 40)
                self.b2.set_maxsize(40, 40)
                self.void.set_maxsize(420, 40)

    @flx.reaction("b1.pointer_click")
    def b1_clicked(self, *events):
        print("yes")
        self.img.set_source("https://img.memecdn.com/ravioli-ravioli-don-amp-039-t-lewd-the-wendy--lini_o_7165003.jpg")

    @flx.reaction("b2.pointer_click")
    def b2_clicked(self, *events):
        print("no")


if __name__ == '__main__':
    m = flx.launch(Jank, "app", title="Meme-Beam", size=(510, 540))
    flx.run()
