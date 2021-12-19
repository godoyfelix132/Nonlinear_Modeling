from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import numpy as np


class Optimization:
    @staticmethod
    def y_lambda(l, vgs):
        return l[3] - (l[0] * (1 + (l[1] * vgs)) * np.tanh(l[2] * vgs))

    @staticmethod
    def y_alfa(a, vgs):
        return a[0] + (a[1] * (np.exp(-(((vgs-a[2])/a[3])**2))))

    @staticmethod
    def fun_lambda(v_init, v_data, vgs_data):
        return Optimization.y_lambda(v_init, vgs_data) - v_data

    @staticmethod
    def fun_alfa(v_init, v_data, vgs_data):
        return Optimization.y_alfa(v_init, vgs_data) - v_data

    @staticmethod
    def lambda_vgs(vgs_data, lambda_data):
        vgs_data = np.array(vgs_data)
        lambda_data = np.array(lambda_data)

        l_init = [1, 1, 1, 1]
        res1 = least_squares(Optimization.fun_lambda, l_init, args=(lambda_data, vgs_data), verbose=0)

        lambda_test = Optimization.y_lambda(res1.x, vgs_data)

        plt.plot(vgs_data, lambda_data, 'o', markersize=4, label='Mediciones')
        plt.plot(vgs_data, lambda_test, label='Modelo')
        plt.xlabel("Vgs")
        plt.ylabel("Lambda (Vgs)")
        plt.legend(ncol=2)
        plt.show()
        return res1.x

    @staticmethod
    def alfa_vgs(vgs_data, alfa_data):
        vgs_data = np.array(vgs_data)
        alfa_data = np.array(alfa_data)
        a_init = [1, 1, 1, 1]
        res1 = least_squares(Optimization.fun_alfa, a_init, method='trf', ftol=1.49012e-8, xtol=1.49012e-8, max_nfev=400, args=(alfa_data, vgs_data), verbose=0)

        alfa_test = Optimization.y_alfa(res1.x, vgs_data)

        plt.plot(vgs_data, alfa_data, 'o', markersize=4, label='Mediciones')
        plt.plot(vgs_data, alfa_test, label='Modelo')
        plt.xlabel("Vgs")
        plt.ylabel("Alfa (Vgs)")
        plt.legend(ncol=2)
        plt.show()
        return res1.x

    @staticmethod
    def graph_lambda(values, lambda_data, vgs_data):
        vgs_data = np.array(vgs_data)
        lambda_data = np.array(lambda_data)
        lambda_test = Optimization.y_lambda(values, vgs_data)
        plt.plot(vgs_data, lambda_data, 'o', markersize=4, label='Mediciones')
        plt.plot(vgs_data, lambda_test, label='Modelo')
        plt.xlabel("Vgs")
        plt.ylabel("Lambda (Vgs)")
        plt.title = 'Comprobación de los datos optimizados'
        plt.legend(ncol=2)
        plt.show()

    @staticmethod
    def graph_alfa(values, alfa_data, vgs_data):
        vgs_data = np.array(vgs_data)
        alfa_data = np.array(alfa_data)
        alfa_test = Optimization.y_alfa(values, vgs_data)
        plt.plot(vgs_data, alfa_data, 'o', markersize=4, label='Mediciones')
        plt.plot(vgs_data, alfa_test, label='Modelo')
        plt.xlabel("Vgs")
        plt.ylabel("Alfa (Vgs)")
        plt.legend(ncol=2)
        plt.show()