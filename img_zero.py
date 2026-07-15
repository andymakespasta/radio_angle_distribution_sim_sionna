import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sionna.rt
import mitsuba as mi
from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, Camera,\
                      PathSolver, RadioMapSolver, subcarrier_frequencies,\
                      ITURadioMaterial, SceneObject

scene = load_scene(filename = None)
scene.frequency = 2400e6 #in Hz, 900e6 is 900MHz, affects material properties.

scene.tx_array = PlanarArray(num_rows=1, num_cols=1, pattern="dipole", polarization="V")
scene.rx_array = PlanarArray(num_rows=4, num_cols=4,
                             vertical_spacing=0.5,  #in wavelengths
                             horizontal_spacing=0.5,
                             pattern="dipole",
                             polarization="V")
tx = Transmitter(name="tx",
                 position=[0,0,0],
                 orientation=(0,-np.pi/2,0),
                 display_radius=0.5)
rx = Receiver(name="rx",
              position=[10,10,10],
              orientation=(0,-np.pi/2,0),
              display_radius=0.3)

scene.add(tx)
scene.add(rx)

p_solver  = PathSolver()
paths = p_solver(scene=scene,
                 max_depth=5,
                 los=True,
                 specular_reflection=True,
                 diffuse_reflection=False,
                 refraction=True,
                 synthetic_array=False,
                 seed=41)

cfr = paths.cfr(scene.frequency)


print(paths.a[0][:,:,0,0,0])
print(cfr[0][0,:,0,0,0,0])
print("----------")
print(paths.a[1][:,:,0,0,0])
print(cfr[1][0,:,0,0,0,0])
print("----------")
print(np.square(paths.a[1][:,:,0,0,0]) + np.square(paths.a[0][:,:,0,0,0]))
print(np.square(cfr[0][0,:,0,0,0,0]) + np.square(cfr[1][0,:,0,0,0,0]))


# a_non_synthetic = a_non_synthetic*np.exp(-1j*2.*np.pi*(tau_non_synthetic-tau_synthetic)*wavelength)



