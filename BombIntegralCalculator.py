import mpmath as mp


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


def StandardDamageModel(X_p, Y_p, Z_p, Armoured):
    a, b, c = CheckArmour(Armoured)
    R = mp.sqrt(X_p*X_p + Y_p*Y_p + Z_p*Z_p)

    return a*mp.exp(-((R - b) / c)**2)


def phi_far(x_0, x_1, gamma, X_p, Armoured):
    a, b, c = CheckArmour(Armoured)
    return mp.erf((gamma * X_p + x_1) / c) - mp.erf((gamma * X_p + x_0) / c)


def const_N_far(z_0, Z_p, R, Armoured):
    a, b, c = CheckArmour(Armoured)
    gamma = b / R - 1
    gamma_2 = gamma*gamma
    return (mp.pi * a * c*c / 4) * mp.exp(
           (gamma_2*R*R - (R-b)**2 - (z_0 + gamma*Z_p)**2)/(c*c))


def Theta_far(x_0, y_0, x_1, y_1, z_0, X_p, Y_p, Z_p, Armoured):
    a, b, c = CheckArmour(Armoured)
    R = mp.sqrt(X_p*X_p + Y_p*Y_p + Z_p*Z_p)
    gamma = b/R - 1
    return (const_N_far(z_0, Z_p, R, Armoured)
            * phi_far(x_0, x_1, gamma, X_p, Armoured)
            * phi_far(y_0, y_1, gamma, Y_p, Armoured))


def phi_general(x_0, x_1, gamma, X_p, Armoured):
    a, b, c = CheckArmour(Armoured)
    sigma = gamma + 2
    return (mp.erf((gamma * X_p + sigma * x_1) / (c*mp.sqrt(sigma)))
            - mp.erf((gamma * X_p + sigma*x_0) / (c*mp.sqrt(sigma))))


def const_M_general(z_0, Z_p, R, Armoured):
    a, b, c = CheckArmour(Armoured)
    gamma = b / R - 1
    sigma = gamma + 2
    gamma_2 = gamma*gamma
    return ((mp.pi * a * c * c / (4 * sigma))
            * mp.exp((gamma_2 * R * R - sigma * (R - b) ** 2
                      - (sigma * z_0 + gamma * Z_p) ** 2)
            / (sigma * c * c)))


def Theta_general(x_0, y_0, x_1, y_1, z_0, X_p, Y_p, Z_p, Armoured):
    a, b, c = CheckArmour(Armoured)
    R = mp.sqrt(X_p*X_p + Y_p*Y_p + Z_p*Z_p)
    gamma = b/R - 1
    return (const_M_general(z_0, Z_p, R, Armoured)
            * phi_general(x_0, x_1, gamma, X_p, Armoured)
            * phi_general(y_0, y_1, gamma, Y_p, Armoured))
