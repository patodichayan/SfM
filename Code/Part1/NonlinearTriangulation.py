import numpy as np
from scipy import optimize


def compute_reproj_err(pt_img1, M1, pt_img2, M2, X):

    # make X homogenous
    X = np.reshape(X, (3, 1))
    X = np.vstack((X, 1))

    reproj_err = 0
    # get the projected points
    # for cam 1
    pt_img1_proj = np.dot(M1, X)
    pt_img1_proj = pt_img1_proj/pt_img1_proj[2]

    # for cam 2
    pt_img2_proj = np.dot(M2, X)
    pt_img2_proj = pt_img2_proj/pt_img2_proj[2]

    # compute error for both cams and add
    # for cam 1
    reproj_err += ((pt_img1[0] - pt_img1_proj[0])**2) + ((pt_img1[1] - pt_img1_proj[1])**2)

    # for cam 2
    reproj_err += ((pt_img2[0] - pt_img2_proj[0])**2) + ((pt_img2[1] - pt_img2_proj[1])**2)

    return reproj_err


def optimize_params(x0, pt_img1, M1, pt_img2, M2):

    # x0 is the 3D point that we want to refine
    # calculate reprojection error
    reproj_err = compute_reproj_err(pt_img1, M1, pt_img2, M2, x0)
    return reproj_err


def nonlinear_triang(M1, M2, X_list, inliers, K):

    # extract image points
    pts_img1 = inliers[:, 0:2]
    pts_img2 = inliers[:, 2:4]

    X_list_ref = []

    for pt_img1, pt_img2, X in zip(pts_img1, pts_img2, X_list):
        X = X.reshape(X.shape[0],)
        result = optimize.least_squares(fun=optimize_params,x0=X, args=[pt_img1, M1, pt_img2, M2])
        X_ref = result.x
        X_ref = np.reshape(X, (3,))
        X_list_ref.append(X_ref)

    X_list_ref = np.array(X_list_ref)
    # print("shape of X after triang - {}".format(X_list_ref.shape))
    X_list_ref = X_list_ref.reshape((X_list_ref.shape[0], 3))

    return X_list_ref
