import os
import matplotlib.pyplot as plt
import numpy as np

scene_name = "Empty_simple"
save_directory = "output/"+scene_name

# np.save(save_directory+"/cr_real", np.array(paths.a[0][:,:,0,0,0]))
# np.save(save_directory+"/cr_img", np.array(paths.a[1][:,:,0,0,0]))

real = np.load(save_directory+"/cr_real.npy")
img = np.load(save_directory+"/cr_img.npy")
