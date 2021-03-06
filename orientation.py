__author__ = 'Andrew'

from imusim.maths.quaternions import *
import imusim.algorithms.vector_observation as vector_observation

class GyroIntegrator():
    """
    An estimator that obtains its orientation using only gyroscope integration.
    """

    def __init__(self, initialRotation, **kwargs):
        self.qHat = initialRotation.copy()

    def update(self, gyro, dt):
        dotq = 0.5 * self.qHat * Quaternion(0, *gyro)
        self.qHat += dotq * dt
        self.qHat.normalise()
        return self.qHat


class OrientCF():
    """
    Implementation of the complementary filter used on the Orient IMU.

    See A. Young, M. Ling, and D. K. Arvind. "Orient-2: A Realtime Wireless
    Posture Tracking System using Local Orientation Estimation". in Proc.
    4th Workshop on Embedded Network Sensors, pp 53-57. ACM, 2007.

    @ivar vectorObservation: L{TimeSeries} of vector observation results.
    """

    def __init__(self, initialRotation, k, aT, **kwargs):
        """
        @param aT: acceleration threshold (float). The correction step will
            only be performed if the condition M{abs(norm(accel) - 1) <= aT}
            is met.
        """

        self._k = float(k)
        self._aT = float(aT)
        self.qHat = initialRotation.copy()
        self._vectorObservation = vector_observation.GramSchmidt()

    def update(self, accel, mag, gyro, dt, k=None, aT=None):
        dotq = 0.5 * self.qHat * Quaternion(0,*gyro)
        self.qHat += dotq * dt

        if aT is None:
            _aT = self._aT
        else:
            _aT = float(aT)

        if k is None:
            _k = self._k
        else:
            _k = float(k)

        if abs(vectors.norm(accel) - 1) < _aT:
        #if False:
            qMeas = self._vectorObservation(-accel, mag)
            if self.qHat.dot(qMeas) < 0:
                qMeas.negate()
            qError = qMeas - self.qHat
            self.qHat += (1/_k) * dt * qError
        #else:
            #print "hello"
            #qMeas = Quaternion.nan()

        self.qHat.normalise()
        return self.qHat