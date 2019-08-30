###
### Copyright (C) 2019 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ..util import *
from .vpp import VppTest

spec = load_test_spec("vpp", "mirroring")

class default(VppTest):
  def before(self):
    vars(self).update(
      caps        = platform.get_caps("vpp", "mirroring"),
      metric      = dict(type = "md5"),
      vpp_element = "transpose",
    )
    super(default, self).before()

  @slash.requires(*platform.have_caps("vpp", "mirroring"))
  @slash.parametrize(*gen_vpp_mirroring_parameters(spec))
  def test(self, case, method):
    vars(self).update(spec[case].copy())
    vars(self).update(
      case      = case,
      degrees   = 0,
      direction = map_transpose_direction(0, method),
      method    = method,
    )

    if self.direction is None:
      slash.skip_test(
        "{method} mirroring unsupported".format(**vars(self)))

    self.vpp()

  def check_metrics(self):
    self.decoded = self.ofile
    check_metric(**vars(self))
