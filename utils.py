import numpy as np
import matplotlib.pyplot as plt
from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, Camera,\
                      PathSolver, RadioMapSolver, subcarrier_frequencies

# creates array of coordinates
def rx_pos_space_filling(x_min, x_max, y_min, y_max, z_min, z_max, step=0.5):
  array_size = int(np.ceil((x_max-x_min)/step)) * int(np.ceil((y_max-y_min)/step)) * int(np.ceil((z_max-z_min)/step))
  out = np.empty((array_size, 3), dtype=np.float64)
  count = 0
  for x in np.arange(x_min, x_max, step).tolist():
    for y in np.arange(y_min, y_max, step).tolist():
      for z in np.arange(z_min, z_max, step).tolist():
        out[counter] = [x,y,z]
        count +=1
  if count != array_size:
    print(f"utils rx_pos_space_filling error: {count} != {array_size}")
  return count, out

#creates array of random points
def rx_pos_random(x_min, x_max, y_min, y_max, z_min, z_max, array_size=1000):
  out = np.empty((array_size, 3), dtype=np.float64)
  for i in range(array_size):
    out[i] = [np.random.uniform(x_min, x_max),
              np.random.uniform(y_min, y_max),
              np.random.uniform(z_min, z_max)]
  return out

def unit_sph_to_cart(theta, phi):
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return [x, y, z]

def draw_cir(paths, rx_num, ant_num):
  #stolen from sionna-rt tutorial https://nvlabs.github.io/sionna/rt/tutorials/Introduction.html
    a, tau = paths.cir(normalize_delays=True, out_type="numpy")
    # Shape: [num_rx, num_rx_ant, num_tx, num_tx_ant, num_paths]
    t = tau[rx_num, ant_num, 0,0,:]/1e-9 # Scale to ns
    # Shape: [num_rx, num_rx_ant, num_tx, num_tx_ant, num_paths, num_time_steps]
    cr = a[rx_num, ant_num, 0,0,:,0]
    a_abs = np.abs(cr)
    a_max = np.max(a_abs)
    print(f"paths: {a_abs.shape}, first path: {cr}")
    plt.figure()
    plt.title("Channel impulse response")
    plt.stem(t, a_abs)
    plt.xlabel(r"$\tau$ [ns]")
    plt.ylabel(r"$|a|$");
    plt.show()

if __name__ == "__main__":
  arr = rx_pos_space_filling(-1,1,-1,1,-1,1,step=0.5)
  arr2 = rx_pos_random(-1,1,-1,1,-10,10, array_size=10)
  arr = rx_pos_space_filling(-1,1.1,-1,1.1,-10,10.1,step=0.5)  
