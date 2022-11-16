import pyln


def main():
    pyln.utility.compile_numba()
    # create a scene and add a single cube
    scene = pyln.Scene()
    scene.add(pyln.Cube([-1, -1, -1], [1, 1, 1]))

    # define camera parameters
    eye = [4.0, 3.0, 2.0]  # camera position
    center = [0.0, 0.0, 0.0]  # camera looks at
    up = [0.0, 0.0, 1.0]  # up direction

    # define rendering parameters
    width = 1024  # rendered width
    height = 1024  # rendered height
    fovy = 50.0  # vertical field of view, degrees
    znear = 0.1  # near z plane
    zfar = 10.0  # far z plane
    step = 0.01  # how finely to chop the paths for visibility testing

    # compute 2D paths that depict the 3D scene
    paths = scene.render(eye, center, up, width, height, fovy, znear, zfar, step)
    # save results
    paths.write_to_svg(
        "examples/images/cube.svg", width, height, background_color="white"
    )


if __name__ == "__main__":
    main()
