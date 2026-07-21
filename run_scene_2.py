import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sionna.rt
import mitsuba as mi
from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, Camera,\
                      PathSolver, RadioMapSolver, subcarrier_frequencies,\
                      ITURadioMaterial, SceneObject


print(f"Mitsuba variant: {mi.variant()}")


# Change this
scene_name = "Empty_simple"
rx_pos = np.random.normal(-3, 3, (10000, 3))
# a = vector.array({"x": np.arange(-3,3,0.5), "y": np.arange(-3,3,0.5), "z": np.arange(-3,3,0.5)})


scene = load_scene(filename = None)
scene.frequency = 2400e6 #in Hz, 900e6 is 900MHz, affects material properties.

# pattern="tr38901"
scene.tx_array = PlanarArray(num_rows=1, num_cols=1, pattern="dipole", polarization="V")
scene.rx_array = PlanarArray(num_rows=8, num_cols=8,
                             vertical_spacing=0.5,  #in wavelengths
                             horizontal_spacing=0.5,
                             pattern="dipole",
                             polarization="V")

tx = Transmitter(name="tx",
                 position=[0,0,0],
                 orientation=(0,-np.pi/2,0),
                 display_radius=0.5)
scene.add(tx)

# Place scene objects here:
# reflector = SceneObject(fname=sionna.rt.scene.reflector, 
#                         name=f"reflector",
#                         radio_material=ITURadioMaterial(name="reflector-mat", itu_type="metal", thickness=0.01, color=(0.48, 0.49, 0.49)))

# reflector = SceneObject(fname=sionna.rt.scene.sphere,
#                 name="sphere",
#                 radio_material=ITURadioMaterial(name="sphere-material",
#                                                 itu_type="metal",
#                                                 thickness=0.01))

# scene.edit(add=reflector)
# reflector.position = mi.Point3f(0,0,-1)
# reflector.look_at(mi.Point3f(0,0,0))



rx_num = 0
for x in range(-50,51,50):
    for y in range(-50,51,50):
        for z in range(-50,51,50):
            rx = Receiver(name=f"rx_{rx_num}",
                            position=[x/10,y/10,z/10],
                            orientation=(0,-np.pi/2,0),
                            display_radius=0.3)
            scene.add(rx)
            print(f"rx_{rx_num}: {x}_{y}_{z}")
            if rx_num == 0:
                print(rx.position)
                print(rx.orientation)
            rx_num = rx_num + 1

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

# save the outputs

# scene preview
save_directory = "output/"+scene_name
try:
    os.mkdir(save_directory)
except FileExistsError:
    print(save_directory + " exists")
except:
    print("mkdir:", e)

np.save(save_directory+"/cr_real", np.array(paths.a[0][:,:,0,0,0]))
np.save(save_directory+"/cr_img", np.array(paths.a[1][:,:,0,0,0]))

cam = Camera(position=[-20,20,15], look_at=[0,0,0])
scene.render_to_file(camera=cam,
                     filename=save_directory+"/scene.png",
                     resolution=[650,500]);
preview_img = np.asarray(Image.open(save_directory+"/scene.png"))
img_plt = plt.imshow(preview_img)
plt.show()

# frequencies = subcarrier_frequencies(1024, 30e3), creates a list from scene frequency as center frequency
# cfr = paths.cfr(frequencies=[scene.frequency.item()],
#                    normalize=False,
#                    normalize_delays=False,
#                    out_type="numpy")

#position of transmitter antennae and rx antennae
#use this to check orientation is correct.
# paths.sources
# paths.targets
# paths.targets.to_numpy()

#real and imaginary components of channel response.
print(paths.a[0][:,:,0,0,0])
print("----------")
print(paths.a[1][:,:,0,0,0])


# paths.targets 
#is there a guarantee for which matches up with which channel response?

# array ordering is a little different between mitsuba and numpy
rx_pos = np.reshape(np.array(paths.targets).transpose(), (rx_num, -1, 3))
np.save(save_directory+"/rx_pos", rx_pos)

# scene.targets()

#sample of objects interacted with:
# paths.objects[:,:5,:5,0,0,0]





