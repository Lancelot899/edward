from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import edward as ed
import numpy as np
import tensorflow as tf

from edward.models import Normal, PointMass


class test_map_class(tf.test.TestCase):

  def test_normalnormal_run(self):
    with self.test_session() as sess:
      x_data = np.array([0.0] * 50, dtype=np.float32)

      mu = Normal(mu=0.0, sigma=1.0)
      x = Normal(mu=tf.ones(50) * mu, sigma=1.0)

      qmu = PointMass(params=tf.Variable(tf.ones([])))

      # analytic solution: N(mu=0.0, sigma=\sqrt{1/51}=0.140)
      inference = ed.MAP({mu: qmu}, data={x: x_data})
      inference.run(n_iter=1000)

      qmu_mean, qmu_var = tf.nn.moments(qmu.sample(100), axes=[0])

      self.assertAllClose(qmu_mean.eval(), 0)
      self.assertEqual(qmu_var.eval(), 0)  # delta function approx to posterior

if __name__ == '__main__':
  ed.set_seed(42)
  tf.test.main()