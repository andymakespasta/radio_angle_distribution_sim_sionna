import numpy as np

# creates array of coordinates
def rx_pos_space_filling(x_min, x_max, y_min, y_max, z_min, z_max, step=0.5):
  # for x in np.linspace(x_min, x_max, ).tolist():
  #   for y in np.linspace(y_min, y_max, 3).tolist():
  #     for z in np.linspace(z_min, z_max, 3).tolist():
  array_size = int(np.ceil((x_max-x_min)/step)) * int(np.ceil((y_max-y_min)/step)) * int(np.ceil((z_max-z_min)/step))
  out = np.empty((array_size, 3), dtype=np.float64)
  counter = 0
  for x in np.arange(x_min, x_max, step).tolist():
    for y in np.arange(y_min, y_max, step).tolist():
      for z in np.arange(z_min, z_max, step).tolist():
        out[counter] = [x,y,z]
        counter +=1
  print(f"{counter} - {array_size}")
  return out

def rx_pos_random(x_min, x_max, y_min, y_max, z_min, z_max, array_size=1000):
  out = np.empty((array_size, 3), dtype=np.float64)
  for i in range(array_size):
    out[i] = [np.random.uniform(x_min, x_max),
              np.random.uniform(y_min, y_max),
              np.random.uniform(z_min, z_max)]
  return out



if __name__ == "__main__":
  arr = rx_pos_space_filling(-1,1,-1,1,-1,1,step=0.5)
  arr2 = rx_pos_random(-1,1,-1,1,-10,10, array_size=10)
  arr = rx_pos_space_filling(-1,1.1,-1,1.1,-10,10.1,step=0.5)  
