import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sionna.rt
import mitsuba as mi
from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, Camera,\
                      PathSolver, RadioMapSolver, subcarrier_frequencies
print(f"Mitsuba variant: {mi.variant()}")


# Change this
scene_name = "Empty_simple"
rx_pos = np.random.normal(-3, 3, (10000, 3))
# a = vector.array({"x": np.arange(-3,3,0.5), "y": np.arange(-3,3,0.5), "z": np.arange(-3,3,0.5)})


scene = load_scene(filename = None)
scene.frequency = 900e6 #in Hz, 900e6 is 900MHz, affects material properties.

# pattern="tr38901"
scene.tx_array = PlanarArray(num_rows=1, num_cols=1, pattern="dipole", polarization="cross")
scene.rx_array = PlanarArray(num_rows=8, num_cols=8,
                             vertical_spacing=0.5,  #in wavelengths
                             horizontal_spacing=0.5,
                             pattern="dipole",
                             polarization="cross")

tx = Transmitter(name="tx",
                 position=[0,0,0],
                 display_radius=0.5)
scene.add(tx)

# Place scene objects here:

# main loop, iterating over rx positions
# for x in np.linspace(-5,5,3).tolist():
#   for y in np.linspace(-5,5,3).tolist():
#     for z in np.linspace(-5,5,3).tolist():

#       rx = Receiver(name=f"rx_{x*10}_{y*10}_{z*10}",
#                        position=[x,y,z],
#                        display_radius=0.2)
#       scene.add(rx)

for x in range(-50,50,25):
    for y in range(-50,50,25):
        for z in range(-50,50,25):
            print(f"rx_{x}_{y}_{z}")
            rx = Receiver(name=f"rx_{x}_{y}_{z}",
                            position=[x/10,y/10,z/10],
                            display_radius=0.1)
            scene.add(rx)

p_solver  = PathSolver()

# Compute propagation paths
paths = p_solver(scene=scene,
                 max_depth=5,
                 los=True,
                 specular_reflection=True,
                 diffuse_reflection=False,
                 refraction=True,
                 synthetic_array=False,
                 seed=41)

# scene preview
cam = Camera(position=[-20,20,15], look_at=[0,0,0]) #TODO: set camera position.

save_directory = "output/"+scene_name
try:
    os.mkdir(save_directory)
except OSError as e:
    print("mkdir:", e)

scene.render_to_file(camera=cam,
                     filename=save_directory+"/scene.png",
                     resolution=[650,500]);
preview_img = np.asarray(Image.open(save_directory+"/scene.png"))
img_plt = plt.imshow(preview_img)
plt.show()




# frequencies = subcarrier_frequencies(1024, 30e3), creates a list from scene frequency as center frequency


cfr = paths.cfr(frequencies=[scene.frequency],
                   normalize=False,
                   normalize_delays=False,
                   out_type="numpy")
