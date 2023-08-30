from  src.engine import *

window = Window()
model = Model("french_bulldog.obj")

def main_loop(self):
    global model
    self.render_model(model)
window.add_loop(main_loop)
window.run()


