import numpy as np
from scipy.special import erf
dictConst = {
    "a_1": 450.7,
    "b_1": 75.68,
    "c_1": 789,
    "a_2": 200.2,
    "b_2": 162.7,
    "c_2": 747.0
    }


def CheckArmour(Armoured):
    if Armoured is False:
        a = dictConst["a_1"]
        b = dictConst["b_1"]
        c = dictConst["c_1"]
    else:
        a = dictConst["a_2"]
        b = dictConst["b_2"]
        c = dictConst["c_2"]
    return a, b, c


# Example for test site, globally sets armour value
Armoured = True
a, b, c = CheckArmour(Armoured)


# Site pieces are given in the format [x_0,y_0,x_1,y_1,z_0].
# Full sites are simply lists with multiple pieces, like in the format below.
TestSite = [
    [-32, -32, 32, -16, 0],
    [16, -16, 32, 32, 0],
    [-32, 0, 0, 32, 500]
    ]


def getArea(Site):  # Returns the area of each piece of bombsite in order
    outList = []
    for T in Site:
        outList.append((T[2] - T[0]) * (T[3] - T[1]))
    return np.array(outList)


def getCentroid(Site, Area):  # Returns the centroid of the site
    x_c = 0                   # Uses input from getArea as Area
    y_c = 0
    z_c = 0
    A = np.sum(Area)
    for i in range(0, len(Area)):
        x_c = x_c + Area[i] * (Site[i][2] + Site[i][0])
        y_c = y_c + Area[i] * (Site[i][3] + Site[i][1])
        z_c = z_c + Area[i]*Site[i][4]
    x_c, y_c, z_c = x_c / (2 * A), y_c / (2 * A), z_c/A
    return np.array([x_c, y_c, z_c])


def getDist(arrayCentre, Position):  # Returns Euclidean norm
    return np.linalg.norm(arrayCentre - Position)


def getDistConst(R):  # Returns sigma and gamma constants
    gamma = b/R - 1
    return (gamma, gamma + 2)


def M_Const(R, gamma, sigma, Z_p, z_0):  # Returns M(Z_p)
    gamma_2 = gamma*gamma
    return ((np.pi * a * c * c / (4 * sigma))
            * np.exp((gamma_2 * R * R - sigma * (R - b) ** 2
                      - (sigma * z_0 + gamma * Z_p) ** 2)
            / (sigma * c * c)))


def phi_general(x_0, x_1, gamma, sigma, X_p):  # Returns phi(x_0,x_1;X_p)
    return (erf((gamma * X_p + sigma * x_1) / (c*np.sqrt(sigma)))
            - erf((gamma * X_p + sigma*x_0) / (c*np.sqrt(sigma))))


def CreateFieldFunction(Site):  # Produces a function from a site that
    A = getArea(Site)           # evaluates showpos coordinates
    arrayCentre = getCentroid(Site, A)

    def func(X_p, Y_p, Z_p):
        val = 0
        R = getDist(arrayCentre, [X_p, Y_p, Z_p])
        gam, sig = getDistConst(R)
        for T in Site:
            val += (M_Const(R, gam, sig, Z_p - arrayCentre[2], T[4]) *
                    phi_general(T[0], T[2], gam, sig, X_p - arrayCentre[0]) *
                    phi_general(T[1], T[3], gam, sig, Y_p - arrayCentre[1])
                    )
        return val/np.sum(A)
    return func
