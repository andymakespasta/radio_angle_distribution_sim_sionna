import os
import matplotlib.pyplot as plt
import numpy as np
import utils

# with N antenna elements in array, using numpy array shapes
# antenna_pos shape: [N,3]; channel_response shape: [N] of complex number
# center: output view is from the average position of antenna array. Otherwise uses first element.
# [azimuth_num, polar_num] is the output array shape.
def angle_dist_from_cr_bartlett(
        antenna_pos, # list of coordinates of antenna_positions
        channel_response,
        wavelength, # in [m], or same coordinate system as antenna_pos
        center = True,
        azimuth_num = 360, # divisions of azimuth angle. 0 towards x axis, going towards y axis. (phi in spherical coordinates)
        polar_num = 180, # divisions of polar angle from 0 (pointing up towards z) to 180 (towards negative z) (theta in sph)
    ):
    antenna_center = np.mean(antenna_pos, axis=0)
    angle_distribution = np.empty((azimuth_num, polar_num), dtype=np.float64)
    for azi in range(azimuth_num):
        for pol in range (polar_num):
            phi = (azi *2 *np.pi /azimuth_num)
            theta = (pol *np.pi /polar_num)
            a = utils.unit_sph_to_cart(theta, phi)
            # print(a)
            shift = np.inner(antenna_pos-antenna_center, a)
            # print(shift)
            theta = shift * np.pi*2/wavelength
            # print(theta)
            shifted_cr = channel_response * np.exp(1j * theta)
            # print(shifted_cr)
            total = np.sum(shifted_cr)
            # print(total)
            angle_distribution[azi, pol] = np.absolute(total)
    return antenna_center, angle_distribution

def draw_circular_z_positive(angle_distribution):
    return 0

if __name__ == "__main__":

    test_array_pos = [[0,0,0], [1,0,0], [2,0,0], [3,0,0],
                      [0,1,0], [1,1,0], [2,1,0], [3,1,0],
                      [0,2,0], [1,2,0], [2,2,0], [3,2,0],
                      [0,3,0], [1,3,0], [2,3,0], [3,3,0]]

    # wavelength = 2
    test1_cr_from_x =  [-1, 1, -1, 1,
                        -1, 1, -1, 1,
                        -1, 1, -1, 1,
                        -1, 1, -1, 1]

    test1_cr_from_y =  [1, 1, 1, 1,
                        -1, -1, -1, -1,
                        1, 1, 1, 1,
                        -1, -1, -1, -1]

    center, angle_dist = angle_dist_from_cr_bartlett(test_array_pos, test1_cr_from_x, 2)
    plt.imshow(angle_dist.swapaxes(0, 1), cmap='inferno')
    plt.show()

    center, angle_dist = angle_dist_from_cr_bartlett(test_array_pos, test1_cr_from_y, 2)
    plt.imshow(angle_dist.swapaxes(0, 1), cmap='inferno')
    plt.show()

    center, angle_dist = angle_dist_from_cr_bartlett(test_array_pos, np.add(test1_cr_from_x, test1_cr_from_y), 2)
    plt.imshow(angle_dist.swapaxes(0, 1), cmap='inferno')
    plt.show()

    # wavelength = 4
    test2_cr_from_x =  [1j, 1, -1j, -1,
                        1j, 1, -1j, -1,
                        1j, 1, -1j, -1,
                        1j, 1, -1j, -1]

    test2_cr_from_y =  [1j, 1j, 1j, 1j,
                        1, 1, 1, 1,
                        -1j, -1j, -1j, -1j,
                        -1, -1, -1, -1]

    center, angle_dist = angle_dist_from_cr_bartlett(test_array_pos, test2_cr_from_x, 4)
    plt.imshow(angle_dist.swapaxes(0, 1), cmap='inferno')
    plt.show()

    center, angle_dist = angle_dist_from_cr_bartlett(test_array_pos, test2_cr_from_y, 4)
    plt.imshow(angle_dist.swapaxes(0, 1), cmap='inferno')
    plt.show()

    center, angle_dist = angle_dist_from_cr_bartlett(test_array_pos, np.add(test2_cr_from_x, test2_cr_from_y), 4)
    plt.imshow(angle_dist.swapaxes(0, 1), cmap='inferno')
    plt.show()

    scene_name = "Empty_simple"
    save_directory = "output/"+scene_name

    real = np.load(save_directory+"/cr_real.npy")
    img = np.load(save_directory+"/cr_img.npy")
    pos = np.load(save_directory+"/rx_pos.npy")
    cr = real + 1j * img


    for n in range(27):
        center, angle_dist = angle_dist_from_cr_bartlett(pos[n,:,:], cr[n,:], 0.124914)
        # you can look up the positions of each antenna element using rx_pos.npy with pos[n,:,:]
        np.save(save_directory + f"/angle_dist_{n}", angle_dist)
        plt.imshow(angle_dist.swapaxes(0, 1), cmap='inferno')
        plt.savefig(save_directory + f"/{n}.png")
        plt.show()