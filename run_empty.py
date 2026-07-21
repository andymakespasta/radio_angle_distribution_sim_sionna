import os
import matplotlib.pyplot as plt
import numpy as np
import utils
import bartlett

from PIL import Image
import sionna.rt
import mitsuba as mi
from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, Camera,\
                      PathSolver, RadioMapSolver, subcarrier_frequencies,\
                      ITURadioMaterial, SceneObject

print(f"Running with Mitsuba: {mi.variant()}")

scene_name = "Empty_simple"

# TODO: check for existing data.
# TODO: parameterize
# TODO: save / hash parameters used.

scene = load_scene(filename = None)
scene.frequency = 2400e6 #in Hz, 900e6 is 900MHz, affects material properties.
print(f"wavelength: f{scene.wavelength}")

scene.tx_array = PlanarArray(num_rows=1, num_cols=1, pattern="dipole", polarization="V")
tx = Transmitter(name="tx",
                 position=[0,0,0],
                 orientation=(0,0,0),
                 # orientation=(0,-np.pi/2,0),
                 display_radius=0.5)
scene.add(tx)

scene.rx_array = PlanarArray(num_rows=8, num_cols=8,
                             vertical_spacing=0.125,  #in wavelengths
                             horizontal_spacing=0.125,
                             pattern="dipole",
                             polarization="V")

# rx_num, rx_pos = utils.rx_pos_space_filling(-10,10, -10,10, -10,10, step=2)
rx_num = 2
rx_pos = [[10,0,0], [0,10,0]]
for i in range(rx_num):
    rx = Receiver(name=f"rx_{i}",
                  position=rx_pos[i],
                  orientation=(0,-np.pi/2,0),
                  # orientation=(0,-np.pi,0),
                  display_radius=0.3)
    scene.add(rx)

p_solver  = PathSolver()
paths = p_solver(scene=scene,
                 max_depth=3,
                 los=True,
                 specular_reflection=True,
                 diffuse_reflection=False,
                 refraction=True,
                 synthetic_array=False,
                 seed=0)

cr = paths.cfr(scene.frequency,
                normalize_delays=False,
                normalize=False,
                out_type='numpy')
cr = cr[:,:,0,0,0,0]

rx_antenna_pos = np.reshape(np.array(paths.targets).transpose(), (rx_num, -1, 3))

save_directory = "output/"+scene_name
try:
    os.mkdir(save_directory)
except FileExistsError:
    print(save_directory + " exists")
except:
    print("mkdir:", e)

cam = Camera(position=[-30,30,15], look_at=[0,0,0])
scene.render_to_file(camera=cam,
                     filename=save_directory+"/scene.png",
                     resolution=[1280,720]);

np.save(save_directory+"/channel_response.npy", cr)
np.save(save_directory+"/rx_antenna_pos.npy", rx_antenna_pos)

preview_img = np.asarray(Image.open(save_directory+"/scene.png"))
img_plt = plt.imshow(preview_img)
plt.show()

for i in range(rx_num):
    center, angle_dist = bartlett.angle_dist_from_cr_bartlett(rx_antenna_pos[i,:,:], cr[i,:], scene.wavelength)
    np.save(save_directory + f"/angle_dist_{i}", angle_dist)
    plt.imshow(angle_dist.swapaxes(0, 1), cmap='inferno')
    plt.savefig(save_directory + f"/{i}.png")
    plt.show()