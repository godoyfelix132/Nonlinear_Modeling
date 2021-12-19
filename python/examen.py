import cmath

from src.curves import Curve
from src.functions import Function
from src.optimitation import Optimization
import matplotlib.pyplot as plt
from src.read import Read
import numpy as np
import math

plt.rcParams["figure.figsize"] = (8, 6)

data = Read('M_pulsado.cit')
all_measurements_ol = Function.get_objects(data.vds_list, data.ids_list, data.vgs_list)

ids_vds_curves_ol = Function.get_ids_vds_curves(data.vds_list, data.vgs_list, all_measurements_ol)
Function.plot_curves(ids_vds_curves_ol,  x_label='Vds', y_label='Ids')
plt.show()

ids_vgs_curves_ol = Function.get_ids_vgs_curves(data.vds_list, data.vgs_list, all_measurements_ol)
Function.plot_curves(ids_vgs_curves_ol,  x_label='Vgs', y_label='Ids')
plt.show()

#getting Lambda
curves_to_get_lambda_ol = Function.get_ids_vds_curves(data.vds_list, data.vgs_list, all_measurements_ol, vds_limit_l=0.9)
Function.plot_curves(curves_to_get_lambda_ol,  x_label='Vds', y_label='Ids')
plt.show()
x_points = []
y_points = []
for curve in curves_to_get_lambda_ol:
    m, b = Function.linear_regression(x_list=curve.x_list, y_list=curve.y_list)
    x_points.append(curve.value)
    y_points.append(m[0])
lambda_curve = Curve()
lambda_curve.x_list = x_points
lambda_curve.y_list = y_points
lambda_curve.name = 'lambda'
##############################Lambda_vgs0##########################
Function.plot_curve(lambda_curve, 'Vgs', 'Lambda')
for i in range(len(lambda_curve.x_list)):
    if float(lambda_curve.x_list[i]) == 0:
        Lambda_vgs0 = lambda_curve.y_list[i]
        break
print('Lambda con Vgs0 = ', Lambda_vgs0)
plt.plot(0, Lambda_vgs0, 'o')
plt.show()
####################################################################
Lambdas = Optimization.lambda_vgs(vgs_data=lambda_curve.x_list, lambda_data=lambda_curve.y_list)
L0 = Lambdas[0]
L1 = Lambdas[1]
L2 = Lambdas[2]
L3 = Lambdas[3]
print('Lambdas = ', Lambdas)

#getting VT
curves_to_get_vth_ol = Function.get_ids_vgs_curves(data.vds_list, data.vgs_list, all_measurements_ol, vgs_limit_l=-0.5, vds_limit_l=0.5)
Function.plot_curves(curves_to_get_vth_ol,  x_label='Vgs', y_label='Ids')
plt.show()
x_points = []
y_points = []
for curve in curves_to_get_vth_ol:
    m, b = Function.linear_regression(x_list=curve.x_list, y_list=curve.y_list)
    vth = -b / m[0]
    x_points.append(1/curve.value)
    y_points.append(vth)
vth_curve = Curve()
vth_curve.x_list = x_points
vth_curve.y_list = y_points
vth_curve.name = 'VT'
Function.plot_curve(vth_curve, '1/Vds', 'VT')
m, b = Function.linear_regression(x_list=vth_curve.x_list, y_list=vth_curve.y_list)
Vth = b
print('Vth = ', Vth)
x_points = np.array(x_points)
lin = (m[0]*x_points) + b
lin_curve = Curve()
lin_curve.x_list = x_points
lin_curve.y_list = lin
lin_curve.name = 'Regresión'
Function.plot_curve(lin_curve, '1/Vds', 'VT')
plt.show()

#getting B
for curve in ids_vds_curves_ol:
    if float(curve.value) == 0:
        break
Function.plot_curve(curve, 'Vds', 'Ids')
Vdss = 0
Idss = 0
for i in range(len(curve.x_list)):
    if float(curve.x_list[i]) > 0.6:
        Vdss = curve.x_list[i]
        Idss = curve.y_list[i]
        break
print('Vdss = ', Vdss)
print('Idss = ', Idss)
plt.plot(Vdss, Idss, 'o', label='Vdss - Idss')
plt.legend(ncol=2)
plt.show()
Beta = Idss/((Vth**2)*(1+(Lambda_vgs0*Vdss)))
print('Beta', Beta)

#getting alfa
curves_to_get_alfa_ol = Function.get_ids_vds_curves(data.vds_list, data.vgs_list, all_measurements_ol, vgs_limit_l=-0.8)
Function.plot_curves(curves_to_get_alfa_ol,  x_label='Vgs', y_label='Ids')
plt.show()
interaction = 0
alfa_points = []
vgs_points = []
for curve in curves_to_get_alfa_ol:
    Function.plot_curve(curve, 'Vds', 'Ids')
    Vds0 = 0
    Ids0 = 0
    for i in range(len(curve.x_list)):
        if float(curve.x_list[i]) > 0.1:
            Vds0 = curve.x_list[i]
            Ids0 = curve.y_list[i]
            break
    plt.plot(Vds0, Ids0, 'o', label='Vds0 - Ids0')
    alfa = (1/Vds0) * math.atanh(Ids0/(Beta * (Vth**2)))
    alfa_points.append(alfa)
    vgs_points.append(curve.value)
    interaction = interaction + 1
plt.xlabel('Vds')
plt.ylabel('Ids')
plt.legend(ncol=2)
plt.show()
alfa_curve = Curve()
alfa_curve.x_list = vgs_points
alfa_curve.y_list = alfa_points
Function.plot_curve(alfa_curve, 'Vgs', 'Alfa')
plt.show()
Alfas = Optimization.alfa_vgs(vgs_data=alfa_curve.x_list, alfa_data=alfa_curve.y_list)
A0 = Alfas[0]
A1 = Alfas[1]
A2 = Alfas[2]
A3 = Alfas[3]
print('Alfas = ', Alfas)

#getting Vth0
curves_to_get_vth0_ol = Function.get_ids_vgs_curves(data.vds_list, data.vgs_list, all_measurements_ol)
Function.plot_curves(curves_to_get_vth0_ol,  x_label='Vgs', y_label='Ids')
plt.show()
for curve in curves_to_get_vth0_ol:
    if float(curve.value) == 0.1:
        m, b = Function.linear_regression(x_list=curve.x_list, y_list=curve.y_list)
        Vth0 = -b / m[0]
        break
Function.plot_curve(curve, 'Vds', 'Ids')
plt.show()
print('Vth0 = ', Vth0)

#getting gamma
curves_to_get_gamma_ol = Function.get_ids_vgs_curves(data.vds_list, data.vgs_list, all_measurements_ol, vds_limit_l=0.55, vgs_limit_l=-0.7)
Function.plot_curves(curves_to_get_gamma_ol,  x_label='Vgs', y_label='Ids')
plt.show()
vth_points = []
vds_points = []
for curve in curves_to_get_gamma_ol:
    m, b = Function.linear_regression(x_list=curve.x_list, y_list=curve.y_list)
    vth = -b / m[0]
    vth_points.append(vth)
    vds_points.append(curve.value)
vth_gamma_curve = Curve()
vth_gamma_curve.x_list = vds_points
vth_gamma_curve.y_list = vth_points
vth_gamma_curve.name = 'Vth - Vds'
Function.plot_curve(vth_gamma_curve, 'Vds', 'VT (Vds)')
plt.show()
m, b = Function.linear_regression(x_list=vth_gamma_curve.x_list, y_list=vth_gamma_curve.y_list)
Gamma = m[0]
print('Gamma', Gamma)

#getting Ith
curves_to_get_Ith_ol = Function.get_ids_vds_curves(data.vds_list, data.vgs_list, all_measurements_ol)
Function.plot_curves(curves_to_get_Ith_ol,  x_label='Vgs', y_label='Ids')
plt.show()
x_point = 0
for curve in curves_to_get_Ith_ol:
    if float(curve.value) >= Vth0:
        for i in range(len(curve.x_list)):
            if float(curve.x_list[i]) >= 0.2:
                Ith = curve.y_list[i]
                x_point = curve.x_list[i]
                break
        break
print('Ith = ', Ith)
VST = Ith / math.log(2)
print('VST', VST)
Function.plot_curve(curve, 'Vds', 'Ids')
plt.plot(x_point, Ith, 'o', label='point')
plt.legend(ncol=2)
plt.show()

gmlin0 = 1.5
gmlnx = 0.01
VK0 = 0.05
VKsat = 5
Delta = 13

mcrit = 0.5
psat = 1

#checking Optimized values
o_L0 = 0.18872
o_VST = 0.09990
o_Vth0 = -0.78767
o_Gamma = -0.08985
o_L2 = 3.01552
o_B = 0.28539
o_A0 = -3.87772
o_A1 = 5.86748
o_A2 = -0.30809
o_A3 = 4.4549
o_L3 = 0.154634
o_L1 = 1.22309

o_gmlin0 = 2.56543
o_gmlnx = 0.01029
o_VK0 = 0.05991
o_VKsat = 11.6082
o_Delta = 6.35577

o_mcrit = 0.67093
o_psat = 1.31287
print()
print('L0', 'init =', round(L0, 4), 'opt =', o_L0)
print('L1', 'init =', round(L1, 4), 'opt =', o_L1)
print('L2', 'init =', round(L2, 4), 'opt =', o_L2)
print('L3', 'init =', round(L3, 4), 'opt =', o_L3)
print('A0', 'init =', round(A0, 4), 'opt =', o_A0)
print('A1', 'init =', round(A1, 4), 'opt =', o_A1)
print('A2', 'init =', round(A2, 4), 'opt =', o_A2)
print('A3', 'init =', round(A3, 4), 'opt =', o_A3)
print('B', 'init =', round(Beta, 4), 'opt =', o_B)
print('Vth0', 'init =', round(Vth0, 4), 'opt =', o_Vth0)
print('Gamma', 'init =', round(Gamma, 4), 'opt =', o_Gamma)
print('VST', 'init =', round(VST, 4), 'opt =', o_VST)
print()
print('gmlin0', 'init =', round(gmlin0, 4), 'opt =', o_gmlin0)
print('gmlinx', 'init =', round(gmlnx, 4), 'opt =', o_gmlnx)
print('VK0', 'init =', round(VK0, 4), 'opt =', o_VK0)
print('VKsat', 'init =', round(VKsat, 4), 'opt =', o_VKsat)
print('Delta', 'init =', round(Delta, 4), 'opt =', o_Delta)
print()
print('mcrit', 'init =', round(mcrit, 4), 'opt =', o_mcrit)
print('psat', 'init =', round(psat, 4), 'opt =', o_psat)

Optimization.graph_lambda([L0, L1, L2, L3], vgs_data=lambda_curve.x_list, lambda_data=lambda_curve.y_list)
Optimization.graph_alfa([A0, A1, A2, A3], vgs_data=alfa_curve.x_list, alfa_data=alfa_curve.y_list)

f = 2e9
w = 2*math.pi*f
cs = 1.2e-12

theta = 49.0524
theta_rad = math.radians(theta)
zin = cmath.rect((0.28015/(w*cs)), theta_rad)
print('Zin', zin)
